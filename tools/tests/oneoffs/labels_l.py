import sys; sys.path.insert(0, './work/oneoffs/code')
from oo import *
P = parse(V + 'transcriptions/ZL3b-n.txt'); rows, c, freq = classify(P)
for r in rows:
    p = P[r['pi']]; r['u'] = p['toks'][r['i']][1]; r['sec'] = p['meta'].get('I', '')
def S(set_):
    W = [r['word'] for r in set_]; pg = np.array([r['pi'] for r in set_])
    D = process.cdist(W, W, scorer=Levenshtein.normalized_distance, workers=-1)
    D[pg[:, None] == pg[None, :]] = 9
    return D.min(1).mean()
rng = np.random.default_rng(3)
pool = collections.defaultdict(list)
for r in rows:
    if r['u'] == 'P': pool[(len(r['word']), r['sec'])].append(r)
def draw(lab):
    out = []
    for r in lab:
        k = (len(r['word']), r['sec']); cand = pool.get(k) or [x for (L, s), v in pool.items() if L == len(r['word']) for x in v] or [x for (L, s), v in pool.items() if abs(L - len(r['word'])) <= 2 for x in v]
        out.append(cand[rng.integers(len(cand))])
    return out
for nm, lab in (('all label one-offs', [r for r in rows if r['u'] == 'L']), ('FREE label one-offs', [r for r in rows if r['u'] == 'L' and r['cls'] == 'FREE'])):
    o = S(lab); null = np.array([S(draw(lab)) for _ in range(1000)])
    print('%-22s n %3d  S %.3f  null %.3f [%.3f, %.3f]  p(lower) %.4f' % (nm, len(lab), o, null.mean(), *np.percentile(null, [2.5, 97.5]), (1 + np.sum(null <= o)) / 1001))
# second statistic
labtok = collections.Counter(t[0] for p in P for t in p['toks'] if t[1] == 'L')
lab = [r for r in rows if r['u'] == 'L']
src_lab = np.mean([labtok[r['src']] > 0 for r in lab]); par = [r for r in rows if r['u'] == 'P']
src_par = np.mean([labtok[r['src']] > 0 for r in par])
print('source word appears in a label: label one-offs %.3f vs paragraph one-offs %.3f' % (src_lab, src_par))
# examples: closest cross-page label one-off pairs
W = [r['word'] for r in lab]; pg = np.array([r['pi'] for r in lab]); D = process.cdist(W, W, scorer=Levenshtein.distance, workers=-1); D[pg[:, None] == pg[None, :]] = 99
pairs = sorted({(int(D[i, j]), W[i], P[lab[i]['pi']]['panel'], W[j], P[lab[j]['pi']]['panel']) for i in range(len(W)) for j in range(i) if D[i, j] <= 1})
print('label one-off pairs 1 edit apart on different pages:', len(pairs)); print(pairs[:20])
