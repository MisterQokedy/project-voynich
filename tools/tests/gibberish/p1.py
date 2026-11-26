"""Step 1: gibberish vs Voynich fingerprint (see ../PREREG.md). Usage: p1.py GIBDIR MEANDIR > ../p1.out"""
import sys, os, re, glob, json, random, collections, math
import numpy as np
_pf = np.polyfit
def _safe(x, y, d):
    try: return _pf(x, y, d)
    except Exception: return np.array([np.nan, np.nan])
np.polyfit = _safe
sys.path.insert(0, './work/language_test/code'); sys.path.insert(0, './work/timm_generator/code')
from stats import stats
from common import VLINES, idx
import pos as P
sys.argv_g, sys.argv_m = sys.argv[1], sys.argv[2]
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.')
def m2(lines, r, nsh=20):
    end = lambda w: w[-2:]; toks = [w for l in lines for w in l]
    top = {e for e, _ in collections.Counter(map(end, toks)).most_common(15)}
    E = [[end(w) if end(w) in top else '~' for w in l] for l in lines]
    c = collections.Counter(e for l in E for e in l); N = sum(c.values()); H = -sum(v / N * math.log2(v / N) for v in c.values())
    def mi(PP):
        pairs = [(l[i], l[i + 1]) for l in PP for i in range(len(l) - 1) if l[i] != l[i + 1]]; n = len(pairs)
        if not n: return 0
        pc = collections.Counter(pairs); a = collections.Counter(x for x, _ in pairs); b = collections.Counter(y for _, y in pairs)
        return sum(v / n * math.log2(v * n / (a[x] * b[y])) for (x, y), v in pc.items())
    sh = np.mean([mi([r.sample(l, len(l)) for l in E]) for _ in range(nsh)])
    return (mi(E) - sh) / max(H, 1e-9)
def h2g(toks, eva):
    if not eva: return stats.__globals__['H2'](toks)
    return stats.__globals__['H2'](['|'.join(GL.findall(w)) for w in toks]) if False else stats.__globals__['H2'](toks)
def fp(lines, r, eva):
    lines = [l for l in lines if l]
    n = sum(map(len, lines)); k = max(2, n // 100); pages, cur, c = [], [], 0
    for l in lines:
        cur.append(l); c += len(l)
        if c >= n / k and len(pages) < k - 1: pages.append(cur); cur, c = [], 0
    pages.append(cur); pages = [q for q in pages if q]
    while len(pages) > 2 and sum(map(len, pages[-1])) < 30: pages[-2] += pages.pop()
    s = stats(pages, r); T = [w for l in lines for w in l]
    if not eva: P.g = lambda w: list(w)
    else: P.g = lambda w: GL.findall(w)
    fi, fm, la, lm = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter(); li, lmid = [], []
    for l in lines:
        if len(l) < 3: continue
        G = [P.g(w) or ['?'] for w in l]; fi[G[0][0]] += 1; la[G[-1][-1]] += 1; li.append(len(G[0]))
        for q in G[1:-1]: fm[q[0]] += 1; lm[q[-1]] += 1; lmid.append(len(q))
    e = dict(E1=P.js(fi, fm), E2=P.js(la, lm), E3=np.mean(li) - np.mean(lmid))
    return dict(h2=s['S1_h2'], mlen=s['S2_meanlen'], sdlen=s['S3_sdlen'], ttr=len(set(T)) / len(T), orderMI=s['S6_orderMI'],
                near=s['S8_nearcopy'], lrep=s['S9_localrep'], imm=s['S10_immrep'], E1=e['E1'], E2=e['E2'], E3=e['E3'], M2=m2(lines, r))
KEYS = ['h2', 'mlen', 'sdlen', 'ttr', 'orderMI', 'near', 'lrep', 'imm', 'E1', 'E2', 'E3', 'M2']
clean = lambda s: [w for w in re.sub(r"[^a-zà-ÿ\s]", " ", s.lower()).split() if w]
def readlines(f, art=False):
    txt = open(f, encoding='utf-8', errors='ignore').read()
    L = [clean(l) for l in txt.splitlines()]; L = [l for l in L if l]
    if art or (L and np.mean([len(l) for l in L]) > 25):
        T = [w for l in L for w in l]; L = [T[k:k + 9] for k in range(0, len(T), 9)]
    return L
def cut(L, n):
    out, cur, c = [], [], 0
    for l in L:
        cur.append(l); c += len(l)
        if c >= n: out.append(cur); cur, c = [], 0
    return out
TL = [l for i in idx(None, 'test') for l in VLINES[i] if l]
def vwin(n, r):
    s = r.randrange(len(TL)); out, c = [], 0
    while c < n: l = TL[s % len(TL)]; out.append(l); c += len(l); s += 1
    return out
r = random.Random(7)
samples = []
for f in sorted(glob.glob(sys.argv_g + '/*.txt')):
    L = readlines(f); n = sum(map(len, L))
    if n > 2000: samples += [('gib', os.path.basename(f) + f'#{k}', x, True) for k, x in enumerate(cut(L, 300))]
    elif n >= 80: samples.append(('gib', os.path.basename(f), L, False))
for f in sorted(glob.glob(sys.argv_m + '/texts/*.txt')):
    L = readlines(f); n = sum(map(len, L))
    if n >= 300: samples.append(('mean', os.path.basename(f), cut(L, 300)[0], False))
    rr = random.Random(hash(f) % 1000)
    if n >= 300 and rr.random() < 0: pass
cache = {}
rows = []
for kind, name, L, big in samples:
    n = sum(map(len, L)); b = int(round(n / 50) * 50) or 50
    if b not in cache: cache[b] = np.array([[fp(vwin(b, r), r, True)[k] for k in KEYS] for _ in range(200)])
    V = cache[b]; x = fp(L, r, False); xv = np.array([x[k] for k in KEYS])
    z = (xv - V.mean(0)) / (V.std(0) + 1e-12); ok = np.abs(z) < 2
    rows.append(dict(kind=kind, name=name, n=n, big=big, z=z.tolist(), ok=ok.tolist(), nm=int(ok.sum()), vlike=bool(ok.sum() >= 8 and ok[KEYS.index('E1')]), x=x))
json.dump(rows, open('./work/gibberish/p1_rows.json', 'w'), default=float)
def fisher_exact(t, alt):
    (a, b), (c, d) = t; n1, n2, k = a + b, c + d, a + c; C = math.comb
    return sum(C(n1, x) * C(n2, k - x) for x in range(a, min(n1, k) + 1)) / C(n1 + n2, k)
for kind in ('gib', 'mean'):
    R = [x for x in rows if x['kind'] == kind]
    print(f"\n== {kind}: {len(R)} samples, Voynich-like {sum(x['vlike'] for x in R)} ({100*np.mean([x['vlike'] for x in R]):.0f}%), median matches {np.median([x['nm'] for x in R])}/12")
    print('  share matching per stat: ' + ' '.join(f"{k} {100*np.mean([x['ok'][i] for x in R]):.0f}%" for i, k in enumerate(KEYS)))
    print('  median z per stat:       ' + ' '.join(f"{k} {np.median([x['z'][i] for x in R]):+.1f}" for i, k in enumerate(KEYS)))
g = [x['vlike'] for x in rows if x['kind'] == 'gib']; m = [x['vlike'] for x in rows if x['kind'] == 'mean']
print('\nFisher one-sided gib > mean:', fisher_exact([[sum(g), len(g) - sum(g)], [sum(m), len(m) - sum(m)]], 'greater'))
print('\nBig gibberish sample pieces:', sum(x['vlike'] for x in rows if x['big']), 'of', sum(x['big'] for x in rows), 'Voynich-like')
print('\nVoynich 300-word windows, mean (sd):', ' '.join(f"{k} {cache[300][:,i].mean():.3f}({cache[300][:,i].std():.3f})" for i, k in enumerate(KEYS)))
print('\nPer-sample (kind name n matches vlike | E1 value z):')
for x in rows: print(f"  {x['kind']:4} {x['name'][:45]:45} {x['n']:5} {x['nm']:2} {'Y' if x['vlike'] else '.'} | E1 {x['x']['E1']:.3f} z{x['z'][8]:+.1f} orderMI z{x['z'][4]:+.1f} h2 z{x['z'][0]:+.1f}")
