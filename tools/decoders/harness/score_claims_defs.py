"""Score published keys and a best-fitted key on held-out Voynich pages, with controls. Output ../claims.out
Held-out = TEST sheets of timm_generator/split.json, minus leaves each claim was built from."""
import sys, random, statistics as S, json
sys.path.insert(0, './work/decipherment_harness/code'); import harness as h
out = open('/dev/null', 'w')
def pr(*a): print(*a, flush=True); print(*a, file=out, flush=True)
ALL = h.lines_of(h.VL, range(len(h.D))); INV = h.inventory(ALL, 20)
# --- reconstructed keys (see ../KEYS.md for how each value was derived)
BAX = {'k': 'k', 'y': 'n', 'd': 't', 'a': 'a', 'o': 'a', 'i': 'u', 'n': 'r', 'r': 'r', 'm': 'r', 'e': 'o', 'sh': 'ch', 's': 's'}
BAX_SRC = {2, 3, 15, 16, 27, 29, 31, 41, 68, 116}
CH_CORE = {'o': 'o', 'a': 'a', 'y': 'a', 'd': 'd', 'l': 'l', 'r': 'r', 's': 's', 'n': 'n', 'i': 'i', 'e': 'e'}
CH_VALS = ['a', 'e', 'i', 'o', 'u', 'ae', 'd', 'l', 'm', 'n', 'p', 'qu', 'r', 's', 't', 'sa', 'ta', '']
CH_SRC = {n for s in (1, 2, 3, 10, 11, 34, 37, 50, 53, 67, 70, 75, 76, 77, 78, 79, 80, 83, 84, 85, 88, 94, 99, 100) for n in (s - 1, s)}
def held(src): return [i for i in range(len(h.D)) if h.HALF[i] == 'test' and h.leaf(i) not in src]
def fitpages(src): return [i for i in range(len(h.D)) if h.HALF[i] == 'fit' and h.leaf(i) not in src]
def texts(idx):
    T = {'voynich': h.lines_of(h.VL, idx)}
    for k in range(3): T[f'shuf{k}'] = h.wshuffle(T['voynich'], 10 + k)
    for s, P in h.TIMM.items(): T[f'timm{s}'] = h.lines_of(P, idx)
    return T
def row(name, sc): return f'  {name:10s} M1 {sc["M1"]:6.2f}  M2 {sc["M2"]:.3f}  M4 {sc["M4"]:.3f} (pairs {sc["npairs"]})'
def perm_controls(key, lines, lang, n=300, seed=1):
    r = random.Random(seed); us = list(key); res = []
    for _ in range(n):
        v = [key[u] for u in us]; r.shuffle(v); res.append(h.score(dict(zip(us, v)), lines, lang))
    return res
def verdict(sc, ctrl, others):
    p1 = sum(c['M1'] <= sc['M1'] for c in ctrl) / len(ctrl); p2 = sum(c['M2'] >= sc['M2'] for c in ctrl) / len(ctrl)
    beat = all(sc['M1'] < o['M1'] and sc['M2'] > o['M2'] for o in others)
    return f'  vs matched random keys: p(M1) {p1:.3f}  p(M2) {p2:.3f}; beats all shuffled+Timm on M1 and M2: {beat}  -> {"PASS" if p1 < .05 and p2 < .05 and beat else "FAIL"}'
