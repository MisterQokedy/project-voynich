import sys; sys.path.insert(0, './work/oneoffs/code')
from oo import *
NP = 2000
P = parse(V + 'transcriptions/ZL3b-n.txt'); rows, c, freq = classify(P)
for r in rows:
    p = P[r['pi']]; t = p['toks'][r['i']]; r['u'] = t[1]; r['first'] = t[4] == 0; r['sec'] = p['meta'].get('I', ''); r['lang'] = p['meta'].get('L', '')
    r['len'] = len(r['word']); r['lb'] = min(max(r['len'], 4), 11)
isfree = np.array([r['cls'] == 'FREE' for r in rows])
def perm_test(sel_a, sel_b, strata, nperm=NP, seed=0):
    """free share in sel_a minus sel_b, class permuted among hapaxes within strata."""
    rr = np.random.default_rng(seed); obs = isfree[sel_a].mean() - isfree[sel_b].mean()
    idx = collections.defaultdict(list)
    for k, s in enumerate(strata): idx[s].append(k)
    null = []
    for _ in range(nperm):
        f = isfree.copy()
        for s, ks in idx.items(): f[ks] = rr.permutation(f[ks])
        null.append(f[sel_a].mean() - f[sel_b].mean())
    null = np.array(null); p = (1 + np.sum(np.abs(null - null.mean()) >= abs(obs - null.mean()))) / (nperm + 1)
    return obs, null.mean(), p
U = np.array([r['u'] for r in rows]); FIRST = np.array([r['first'] for r in rows])
SL = [(r['sec'], r['lang']) for r in rows]; SLL = [(r['sec'], r['lang'], r['lb']) for r in rows]
PG = [r['pi'] for r in rows]; PGL = [(r['pi'], r['lb']) for r in rows]
res = {}
print('hapax by unit:', collections.Counter(U), 'free share by unit:', {u: round(isfree[U == u].mean(), 3) for u in 'PLCR'})
print('mean length by unit:', {u: round(np.mean([r['len'] for r in rows if r['u'] == u]), 2) for u in 'PLCR'})
for nm, a, b, st, st2 in (('C1 labels vs P', U == 'L', U == 'P', SL, SLL), ('C2 circle+radial vs P', (U == 'C') | (U == 'R'), U == 'P', SL, SLL),
                          ('C3 line-first vs rest (P)', (U == 'P') & FIRST, (U == 'P') & ~FIRST, PG, PGL)):
    o, m, p = perm_test(a, b, st); o2, m2, p2 = perm_test(a, b, st2, seed=1)
    print('%-28s diff %+.3f (null %+.3f) p %.4f | length-stratified (exploratory) null %+.3f p %.4f' % (nm, o, m, p, m2, p2)); res[nm] = (o, m, p, m2, p2)
# partners
types = list(c); tix = {w: k for k, w in enumerate(types)}
hw = [r['word'] for r in rows]
D = process.cdist(hw, types, scorer=Levenshtein.distance, dtype=np.int32, workers=-1, score_cutoff=1)
pages_of = collections.defaultdict(set)
for pi, p in enumerate(P):
    for t in p['toks']: pages_of[t[0]].add(pi)
codes = {}
for l in open(V + 'plant_drawings/page_codes.txt'):
    if l.startswith('#'): continue
    f = l.split()
    if 'NA' not in f[1:]: codes['f' + f[0]] = np.array([int(x) for x in f[1:]])
cp = [pi for pi, p in enumerate(P) if p['panel'] in codes]; cpi = {pi: k for k, pi in enumerate(cp)}
C = np.array([codes[P[pi]['panel']] for pi in cp]); LANG = [P[pi]['meta'].get('L', '') for pi in cp]
def partners(k, maxc=None):
    js = np.nonzero(D[k] == 1)[0]; s = set()
    for j in js:
        w = types[j]
        if maxc is None or c[w] <= maxc: s |= pages_of[w]
    return s - {rows[k]['pi']}
PART = [partners(k) for k in range(len(rows))]; PART3 = [partners(k, 3) for k in range(len(rows))]
def c4(sel, C):
    S = (C[:, None, :] == C[None, :, :]).mean(2); vals = []
    for k in np.nonzero(sel)[0]:
        pi = rows[k]['pi']
        if pi not in cpi: continue
        q = [cpi[x] for x in PART[k] if x in cpi]
        if not q: continue
        a = cpi[pi]; base = (S[a].sum() - 1) / (len(cp) - 1)
        vals.append(S[a, q].mean() - base)
    return np.mean(vals), len(vals)
byl = collections.defaultdict(list)
for k, l in enumerate(LANG): byl[l].append(k)
def c4test(sel, seed=0):
    rr = np.random.default_rng(seed); o, n = c4(sel, C); null = []
    for _ in range(NP):
        Cp = C.copy()
        for l, ks in byl.items(): Cp[ks] = C[rr.permutation(ks)]
        null.append(c4(sel, Cp)[0])
    null = np.array(null); return o, n, null.mean(), (1 + np.sum(null >= o)) / (NP + 1)
for nm, sel in (('FREE', isfree), ('EDIT', ~isfree)):
    o, n, m, p = c4test(sel); print('C4 plant-drawing sim of partner pages, %s: %+.4f over %d hapaxes (null %+.4f) p %.4f (one-sided)' % (nm, o, n, m, p)); res['C4_' + nm] = (o, n, m, p)
# C5 shared section
SEC = np.array([p['meta'].get('I', '') for p in P]); PL = [p['meta'].get('L', '') for p in P]
bylp = collections.defaultdict(list)
for k, l in enumerate(PL): bylp[l].append(k)
def c5(sel, SEC, PART3):
    v = []
    for k in np.nonzero(sel)[0]:
        q = list(PART3[k])
        if q: v.append(np.mean(SEC[q] == SEC[rows[k]['pi']]))
    return np.mean(v), len(v)
def c5test(sel, seed=0):
    rr = np.random.default_rng(seed); o, n = c5(sel, SEC, PART3); null = []
    for _ in range(500):
        Sp = SEC.copy()
        for l, ks in bylp.items(): Sp[ks] = SEC[rr.permutation(ks)]
        null.append(c5(sel, Sp, PART3)[0])
    null = np.array(null); return o, n, null.mean(), (1 + np.sum(null >= o)) / (len(null) + 1)
for nm, sel in (('FREE', isfree), ('EDIT', ~isfree)):
    o, n, m, p = c5test(sel); print('C5 same-section share of rare partner pages, %s: %.3f over %d (null %.3f) p %.4f; excess %.3f' % (nm, o, n, m, p, o - m)); res['C5_' + nm] = (o, n, m, p)
# length-matched FREE vs EDIT2 on C5 (exploratory)
for L in (7, 8, 9):
    a = isfree & (np.array([r['len'] for r in rows]) == L); b = ~isfree & (np.array([r['len'] for r in rows]) == L)
    print('  len %d: C5 FREE %.3f (n %d)  EDIT %.3f (n %d)' % (L, *c5(a, SEC, PART3), *c5(b, SEC, PART3)))
# GEN C5 (sections carried by slot)
for s in (900, 901):
    G = gen_pages(s); gr, gc, gf = classify(G); gt = list(gc)
    gpo = collections.defaultdict(set)
    for pi, p in enumerate(G):
        for t in p['toks']: gpo[t[0]].add(pi)
    GD = process.cdist([r['word'] for r in gr], gt, scorer=Levenshtein.distance, dtype=np.int32, workers=-1, score_cutoff=1)
    GS = np.array([p['meta'].get('I', '') for p in G]); out = {}
    for nm in ('FREE', 'EDIT'):
        v = []
        for k, r in enumerate(gr):
            if (r['cls'] == 'FREE') != (nm == 'FREE'): continue
            q = set()
            for j in np.nonzero(GD[k] == 1)[0]:
                if gc[gt[j]] <= 3: q |= gpo[gt[j]]
            q -= {r['pi']}
            if q: v.append(np.mean(GS[list(q)] == GS[r['pi']]))
        out[nm] = (round(np.mean(v), 3), len(v))
    print('GEN %d C5 same-section share:' % s, out)
json.dump(res, open(OUT + 'cluster.json', 'w'), indent=1, default=float)
