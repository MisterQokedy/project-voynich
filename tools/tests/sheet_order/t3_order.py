"""T3: within-sheet page sequence fit; T4: sheet-order recovery in every quire vs shuffled-page null;
T5: positive control = within-page chunk continuity and pseudo-sheet order recovery on known-order text."""
import sys, json, itertools
from collections import defaultdict, Counter
import numpy as np
sys.path.insert(0, 'code'); from vlib import *
rng = np.random.default_rng(5)
P = load(); sheets, leafq = structure(P); pg = {p['page']: p for p in P}
keys = json.load(open('keys.json')); ix = {k: i for i, k in enumerate(keys)}
SIM = {'tfidf': np.load('S_tfidf.npy'), 'lsa': np.load('S_lsa.npy'), 'jaccard': np.load('S_jacc.npy')}
def stratum(k): p = pg[k]; return (p.get('H'), p.get('L'), p.get('I'))
def sheet_of(k): q, b, f = leafq[pg[k]['leaf']]; return (q, b)
# pool z-normalisation: residual vs same-quire different-sheet pairs with same strata
def zmat(S):
    pools = defaultdict(list)
    for i, a in enumerate(keys):
        for c in keys[i+1:]:
            if pg[a]['Q'] == pg[c]['Q'] and sheet_of(a) != sheet_of(c):
                pools[(pg[a]['Q'],) + tuple(sorted([stratum(a), stratum(c)], key=str))].append(S[ix[a], ix[c]])
    st = {k: (np.mean(v), np.std(v) + 1e-9) for k, v in pools.items() if len(v) >= 4}
    def z(a, c):
        k = (pg[a]['Q'],) + tuple(sorted([stratum(a), stratum(c)], key=str))
        if k not in st: return None
        return (S[ix[a], ix[c]] - st[k][0]) / st[k][1]
    return z
print('== T3 which within-sheet page sequence best explains same-sheet similarity?')
print('   (fit = Spearman-like: mean z of pairs at distance 1 minus distance 3 under each order; 12 orders up to reversal)')
for m, S in SIM.items():
    z = zmat(S); rows = []
    for (q, b), LL in sheets.items():
        if len(LL) != 2: continue
        X, Y = LL; pgs = ['%dr' % X, '%dv' % X, '%dr' % Y, '%dv' % Y]
        if not all(p in ix for p in pgs): continue
        Z = {}
        for i, j in itertools.combinations(range(4), 2):
            v = z(pgs[i], pgs[j]);
            if v is None: break
            Z[(i, j)] = v
        else: rows.append(Z)
    names = ['Xr', 'Xv', 'Yr', 'Yv']; res = []
    for o in itertools.permutations(range(4)):
        if o[0] > o[-1]: continue
        pos = {p: k for k, p in enumerate(o)}
        def fit(R, pos=pos):
            vals = defaultdict(list)
            for Z in R:
                for (i, j), v in Z.items(): vals[abs(pos[i] - pos[j])].append(v)
            x = [d for d in vals for _ in vals[d]]; y = [v for d in vals for v in vals[d]]
            return -np.corrcoef(x, y)[0, 1]
        res.append((fit(rows), '→'.join(names[i] for i in o), fit))
    res.sort(reverse=True)
    # bootstrap over sheets: how often is each order best
    wins = Counter()
    for _ in range(500):
        R = [rows[i] for i in rng.integers(len(rows), size=len(rows))]
        wins[max(res, key=lambda r: r[2](R))[1]] += 1
    print(f' {m}: sheets={len(rows)}; ' + '; '.join(f'{n} {f:+.3f}' for f, n, _ in res[:4]) + f' ... worst {res[-1][1]} {res[-1][0]:+.3f}')
    print('    bootstrap wins:', ', '.join(f'{n} {c/5:.0f}%' for n, c in wins.most_common(4)))

print('\n== T4 sheet-order recovery, every quire with >=3 complete sheets (singulion model, Xr..Yv per sheet)')
def last_page(L):
    k = '%dv' % L
    return k if k in ix else '%dr' % L
def quire_sheets(q):
    sh = [(b, LL) for (qq, b), LL in sheets.items() if qq == q and len(LL) == 2 and '%dr' % LL[0] in ix and last_page(LL[1]) in ix]
    return [LL for b, LL in sorted(sh, key=lambda t: t[1][0])]
def stat(firsts, lasts, S):
    n = len(firsts)
    T = np.array([[S[ix[lasts[a]], ix[firsts[b]]] for b in range(n)] for a in range(n)])
    sc = np.array([sum(T[o[i], o[i+1]] for i in range(n-1)) for o in itertools.permutations(range(n))])
    return sc
summary = defaultdict(list)
for q in sorted({leafq[L][0] for L in leafq}):
    sh = quire_sheets(q)
    if len(sh) < 3: continue
    firsts = ['%dr' % X for X, Y in sh]; lasts = [last_page(Y) for X, Y in sh]
    line = f' Q{q} ({len(sh)} sheets, {np.math.factorial(len(sh)) if hasattr(np,"math") else ""})'
    for m, S in SIM.items():
        sc = stat(firsts, lasts, S); obs = sc.max() - np.median(sc)
        cur = sc[0]  # identity permutation = binding order of first leaves
        cur_rank = (sc > cur).sum() + 1
        slots = firsts + lasts; null = []
        for _ in range(400):
            pm = list(rng.permutation(slots)); n = len(sh)
            s2 = stat(pm[:n], pm[n:], S); null.append(s2.max() - np.median(s2))
        p = (1 + np.sum(np.array(null) >= obs)) / 401
        summary[m].append(p)
        line += f' | {m}: gap={obs:.3f} p={p:.2f} binding rank {cur_rank}/{len(sc)}'
    print(line)
from math import log
from scipy.stats import chi2
for m, ps in summary.items():
    X2 = -2 * sum(log(p) for p in ps)
    print(f' Fisher combined over {len(ps)} quires [{m}]: p = {chi2.sf(X2, 2*len(ps)):.3f}')

print('\n== T5 positive control: does Voynich text carry sequential signal at all? (known order inside pages)')
CH = 30
chunks = []  # (page, idx, words)
for p in P:
    ws = [w for l in p['lines'] if l['u'] == 'P' for w in l['w']]
    n = len(ws) // CH
    for i in range(n): chunks.append((p['page'], i, ws[i*CH:(i+1)*CH]))
M, *_ = tfidf_matrix([c[2] for c in chunks]); C = cos_sim(M)
bypage = defaultdict(list)
for i, c in enumerate(chunks): bypage[c[0]].append(i)
dist = defaultdict(list)
for pgk, ids in bypage.items():
    for a, b in itertools.combinations(ids, 2):
        dist[min(abs(chunks[a][1]-chunks[b][1]), 6)].append(C[a, b])
# baseline: chunks from different pages, same quire & strata
base = []
pl = list(bypage)
for _ in range(20000):
    a, b = rng.choice(len(chunks), 2)
    pa, pb = chunks[a][0], chunks[b][0]
    if pa != pb and pg[pa]['Q'] == pg[pb]['Q'] and stratum(pa) == stratum(pb) and sheet_of(pa) != sheet_of(pb): base.append(C[a, b])
print(f' chunk={CH} words; different-sheet same-quire/strata baseline mean {np.mean(base):.4f} (n={len(base)})')
for d in sorted(dist): print(f'  same page, distance {d}{"+" if d==6 else ""}: mean {np.mean(dist[d]):.4f}  n={len(dist[d])}')
# pseudo-sheet order recovery: pages with >= 8 chunks -> 4 pseudo-sheets of 2 consecutive chunks; known true order
ranks = []; nullranks = []
for pgk, ids in bypage.items():
    if len(ids) < 8: continue
    for start in range(0, len(ids) - 7, 8):
        sel = ids[start:start+8]
        F = [sel[0], sel[2], sel[4], sel[6]]; Lc = [sel[1], sel[3], sel[5], sel[7]]
        T = np.array([[C[Lc[a], F[b]] for b in range(4)] for a in range(4)])
        perms = list(itertools.permutations(range(4)))
        sc = np.array([sum(T[o[i], o[i+1]] for i in range(3)) for o in perms])
        true = sc[0]
        ranks.append(((sc > true).sum() + 0.5 * ((sc == true).sum() - 1)) / (len(sc) - 1))
print(f' pseudo-sheets from known-order text: {len(ranks)} quartets; mean percentile of TRUE order = {np.mean(ranks):.3f} (0=best, 0.5=chance); true order ranked #1 in {np.mean(np.array(ranks)==0):.1%} (chance 4.2%)')
r = np.array(ranks); null = np.array([rng.random(len(r)).mean() for _ in range(20000)])
print(f'  p(mean percentile this low by chance) ~ {(1+np.sum(null<=r.mean()))/20001:.4f}')
