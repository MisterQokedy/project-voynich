import sys, itertools, re
from collections import defaultdict
import numpy as np
sys.path.insert(0, 'code'); exec(open('code/p1_stains.py').read().split("leaves = sorted")[0])
leaves = sorted({int(re.match(r'\d+', p).group()) for p in maps})
pos = {L: i for i, L in enumerate(leaves)}
for key, hp in [('P80', 6), ('B', 6)]:
    LM = {L: leafmap(L, key, hp) for L in leaves}
    sim = lambda a, b: np.corrcoef(LM[a].ravel(), LM[b].ravel())[0, 1]
    W = defaultdict(list); C = defaultdict(list)
    for a, b in itertools.combinations(leaves, 2):
        d = pos[b] - pos[a]
        if d > 4: continue
        (W if leafq[a][0] == leafq[b][0] else C)[d].append(sim(a, b))
    print(key, 'within-quire:', {d: (round(np.mean(v), 3), len(v)) for d, v in sorted(W.items())})
    print(key, 'cross-quire :', {d: (round(np.mean(v), 3), len(v)) for d, v in sorted(C.items())})
    w, c = np.array(W[1]), np.array(C[1]); allv = np.r_[w, c]; obs = w.mean() - c.mean()
    null = [ (lambda p: p[:len(w)].mean() - p[len(w):].mean())(rng.permutation(allv)) for _ in range(20000)]
    print(f'   d=1 within minus cross = {obs:.3f}, permutation p = {(1+np.sum(np.array(null)>=obs))/20001:.4f}')
    # also: cross-quire d=1 vs within-quire d=3/4 (if capture drift, d=1 cross should beat d=4 within)
    print(f'   cross d1 {c.mean():.3f} vs within d4 {np.mean(W[4]):.3f}')
