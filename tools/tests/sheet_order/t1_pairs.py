"""T1/T2: page-pair relationships across all quires, stratified nulls, three metrics."""
import sys, json
from collections import defaultdict
import numpy as np
sys.path.insert(0, 'code'); from vlib import *
rng = np.random.default_rng(11)
P = load(); sheets, leafq = structure(P)
pg = {p['page']: p for p in P}
keys = [p['page'] for p in P if p['nwords'] >= 20]
ix = {k: i for i, k in enumerate(keys)}
stop = stopwords(P); print('stopwords', len(stop), sorted(stop))
vec, nd = lsa_space(P, stop=stop); print('LSA docs', nd)
SIMS = {m: page_sim(P, keys, m, stop=stop, lsa=vec) for m in ['tfidf', 'jaccard', 'lsa']}
def sheet_of(k): L = pg[k]['leaf']; q, b, f = leafq[L]; return (q, b)
def stratum(k): p = pg[k]; return (p.get('H'), p.get('L'), p.get('I'))
# pair types
types = defaultdict(list)
for (q, b), LL in sheets.items():
    if len(LL) != 2: continue
    X, Y = LL
    cand = {'confoliate': [('%dr' % X, '%dv' % X), ('%dr' % Y, '%dv' % Y)],
            'conj_inner': [('%dv' % X, '%dr' % Y)], 'conj_outer': [('%dv' % Y, '%dr' % X)],
            'sheet_dist2': [('%dr' % X, '%dr' % Y), ('%dv' % X, '%dv' % Y)]}
    for t, prs in cand.items():
        for a, c in prs:
            if a in ix and c in ix: types[t].append((a, c, q))
binding = [p['page'] for p in P]
for a, c in zip(binding, binding[1:]):
    if a.endswith('v') and c.endswith('r') and a in ix and c in ix and sheet_of(a) != sheet_of(c):
        types['facing_binding'].append((a, c, pg[a]['Q']))
# null pools: pairs of pages on different sheets, same quire, same strata pair
pools = defaultdict(list)
for i, a in enumerate(keys):
    for c in keys[i + 1:]:
        if pg[a]['Q'] != pg[c]['Q'] or sheet_of(a) == sheet_of(c): continue
        pools[(pg[a]['Q'],) + tuple(sorted([stratum(a), stratum(c)], key=str))].append((ix[a], ix[c]))
def pkey(a, c): return (pg[a]['Q'],) + tuple(sorted([stratum(a), stratum(c)], key=str))
def test(prs, S, nperm=4000):
    real, pl = [], []
    for a, c, q in prs:
        k = pkey(a, c)
        if len(pools.get(k, [])) >= 4:
            real.append(S[ix[a], ix[c]]); pl.append(np.array([S[i, j] for i, j in pools[k]]))
    if not real: return None
    real = np.array(real); obs = real.mean()
    null = np.array([np.mean([x[rng.integers(len(x))] for x in pl]) for _ in range(nperm)])
    z = np.array([(r - x.mean()) / (x.std() + 1e-9) for r, x in zip(real, pl)])
    return dict(n=len(real), obs=obs, null=null.mean(), z=(obs - null.mean()) / null.std(),
                p_hi=(1 + (null >= obs).sum()) / (nperm + 1), p_lo=(1 + (null <= obs).sum()) / (nperm + 1), zs=z)
out = {}
print('\n== T1 pooled, null = random different-sheet pairs, same quire + same hand/lang/illus for both pages')
for m, S in SIMS.items():
    for t in ['confoliate', 'conj_inner', 'conj_outer', 'sheet_dist2', 'facing_binding']:
        r = test(types[t], S)
        out[(m, t)] = r
        print(f'{m:8s} {t:15s} n={r["n"]:3d} obs={r["obs"]:.3f} null={r["null"]:.3f} z={r["z"]:+.2f} p_hi={r["p_hi"]:.4f} p_lo={r["p_lo"]:.4f}')
# per section
sec = {'A': 'herbal', 'B': 'herbal', 'C': 'herbal', 'D': 'herbal', 'E': 'herbal', 'F': 'herbal', 'G': 'herbal', 'H': 'herbal/misc',
       'I': 'astro', 'J': 'astro', 'K': 'astro', 'L': 'astro', 'M': 'balneo', 'N': 'rosettes', 'O': 'pharma', 'Q': 'pharma', 'S': 'pharma', 'T': 'stars'}
print('\n== T1 by section (tfidf / lsa z-scores)')
for s in ['herbal', 'herbal/misc', 'astro', 'balneo', 'pharma', 'stars']:
    row = []
    for t in ['confoliate', 'conj_inner', 'conj_outer', 'facing_binding']:
        for m in ['tfidf', 'lsa']:
            prs = [x for x in types[t] if sec[x[2]] == s]
            r = test(prs, SIMS[m], 2000) if prs else None
            row.append(f'{t[:10]}/{m}: ' + (f'n={r["n"]} z={r["z"]:+.1f}' if r else 'n=0'))
    print(s, ' | '.join(row))
# T2: inner vs outer conjoint, per-sheet paired
print('\n== T2 inner (Xv|Yr, reading-adjacent under singulion) vs outer (Yv|Xr) conjoint, paired by sheet')
for m, S in SIMS.items():
    zin = {}; zout = {}
    for t, d in [('conj_inner', zin), ('conj_outer', zout)]:
        r = test(types[t], S, 10)
        prs = [x for x in types[t] if len(pools.get(pkey(x[0], x[1]), [])) >= 4]
        for (a, c, q), z in zip(prs, r['zs']): d[sheet_of(a)] = z
    common = sorted(set(zin) & set(zout), key=str)
    d = np.array([zin[s] - zout[s] for s in common])
    flips = np.array([np.mean(d * rng.choice([-1, 1], len(d))) for _ in range(20000)])
    print(f'{m:8s} sheets={len(d)} mean diff={d.mean():+.3f} inner>outer {np.sum(d>0)}/{len(d)} p(one-sided sign-flip)={(1+np.sum(flips>=d.mean()))/20001:.4f}')
# T2b: adjacent-in-reading within sheet (confoliate+inner) vs distance-2 (Xr|Yr, Xv|Yv)
print('\n== Paper Table-10 style raw means (no strata) for reference')
for m, S in SIMS.items():
    print(m, {t: round(float(np.mean([S[ix[a], ix[c]] for a, c, q in types[t]])), 3) for t in types})
json.dump({'stop': sorted(stop)}, open('t1_meta.json', 'w'))
np.save('S_tfidf.npy', SIMS['tfidf']); np.save('S_lsa.npy', SIMS['lsa']); np.save('S_jacc.npy', SIMS['jaccard']); json.dump(keys, open('keys.json', 'w'))
