"""P1: do leaves share stain/discolouration patterns with their neighbours, and which stacking order explains it?
Leaf map = mean of recto map and mirrored verso map (stains pass through parchment).
Features: high-passed parchment brightness (80th pct L per cell) and yellowness, ink-heavy cells down-weighted."""
import sys, json, itertools, re
from collections import defaultdict
import numpy as np
from scipy.ndimage import gaussian_filter
sys.path.insert(0, 'code'); from vlib import load, structure
rng = np.random.default_rng(2)
maps = np.load('phys_maps.npy', allow_pickle=True).item()
P = load(); sheets, leafq = structure(P)
def prep(m, key, hp):
    x = m[key].copy()
    lo = gaussian_filter(x, 1.0); bg = gaussian_filter(x, hp)
    z = lo - bg
    return (z - z.mean()) / (z.std() + 1e-9)
def leafmap(L, key, hp):
    ms = [prep(maps[p], key, hp) for p in ('%dr' % L, '%dv' % L) if p in maps]
    return np.mean(ms, 0) if ms else None
leaves = sorted({int(re.match(r'\d+', p).group()) for p in maps})
out = {}
for key in ['P80', 'B']:
  for hp in [6, 15]:
    LM = {L: leafmap(L, key, hp) for L in leaves}
    def sim(a, b): return np.corrcoef(LM[a].ravel(), LM[b].ravel())[0, 1]
    # binding distance decay (within quire and across)
    pos = {L: i for i, L in enumerate(leaves)}
    byd = defaultdict(list)
    for a, b in itertools.combinations(leaves, 2):
        d = abs(pos[a] - pos[b])
        if d <= 12: byd[d].append(sim(a, b))
    s = ' '.join(f'd{d}:{np.mean(byd[d]):.3f}' for d in [1, 2, 3, 4, 6, 8, 12])
    print(f'[{key} hp={hp}] mean leaf-map correlation by binding distance: {s}')
    # same-face neighbor (direct contact) vs leaf distance 1 is the same thing in leaf frame; quire boundary check
    qb, qi = [], []
    for a, b in zip(leaves, leaves[1:]):
        (qb if leafq[a][0] != leafq[b][0] else qi).append(sim(a, b))
    print(f'    adjacent leaves within quire {np.mean(qi):.3f} (n={len(qi)}) vs across quire boundary {np.mean(qb):.3f} (n={len(qb)})')
    # order test inside each quire: current nesting vs all alternative nestings and singulion stacks
    res = []
    for q in sorted({leafq[L][0] for L in leafq}):
        sh = sorted([LL for (qq, b), LL in sheets.items() if qq == q and len(LL) == 2 and all(x in LM and LM[x] is not None for x in LL)], key=lambda t: t[0])
        n = len(sh)
        if n < 3: continue
        def score(stack):  # sum of similarity of physically adjacent leaves in a stack
            return sum(sim(stack[i], stack[i+1]) for i in range(len(stack)-1))
        def nest(o): return [sh[i][0] for i in o] + [sh[i][1] for i in reversed(o)]
        def singl(o): return [x for i in o for x in sh[i]]
        perms = list(itertools.permutations(range(n)))
        nest_sc = np.array([score(nest(o)) for o in perms]); sing_sc = np.array([score(singl(o)) for o in perms])
        cur = nest_sc[0]
        rank = (nest_sc > cur).sum() + 1
        res.append((q, n, rank, len(perms), cur, nest_sc.mean(), sing_sc.max(), sing_sc.mean()))
        print(f'    Q{q}: current nesting rank {rank}/{len(perms)} among nestings (score {cur:.2f}, mean {nest_sc.mean():.2f}); best singulion stack {sing_sc.max():.2f}, mean singulion {sing_sc.mean():.2f}')
    pr = np.array([(r[2] - 0.5) / r[3] for r in res])
    # combined: mean percentile of current nesting; null uniform
    null = np.array([np.mean([(rng.integers(1, r[3]+1) - 0.5) / r[3] for r in res]) for _ in range(20000)])
    print(f'    mean percentile of current nesting across {len(res)} quires = {pr.mean():.3f} (0=best); p={(1+np.sum(null<=pr.mean()))/20001:.4f}')
