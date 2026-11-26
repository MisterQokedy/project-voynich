"""Score published keys and a best-fitted key on held-out Voynich pages, with controls. Output ../claims.out
Held-out = TEST sheets of timm_generator/split.json, minus leaves each claim was built from."""
import sys, random, statistics as S, json
sys.path.insert(0, './work/decipherment_harness/code'); import harness as h
out = open(f'{h.H}/claims.out', 'w')
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
# ---------- 1. Bax 2014 (partial key, unassigned glyphs dropped). No target language claimed: scored against each.
I = held(BAX_SRC); T = texts(I); pr(f'=== Bax 2014 reconstructed partial key ({len(BAX)} units); held-out {len(I)} pages, {sum(len(l) for l in T["voynich"])} words')
for lang in ('latin', 'italian', 'spanish', 'portuguese', 'english'):
    S_ = {k: h.score(BAX, v, lang) for k, v in T.items()}; pr(f' [{lang}]'); [pr(row(k, v)) for k, v in S_.items()]
    pr(verdict(S_['voynich'], perm_controls(BAX, T['voynich'], lang), [v for k, v in S_.items() if k != 'voynich']))
# ---------- 2. Cheshire 2019: shape-identical core fixed; every other glyph given its most favourable value from his letter set, fitted on FIT pages
I = held(CH_SRC); F = fitpages(CH_SRC); T = texts(I); TF = texts(F)
pr(f'\n=== Cheshire 2019: core {CH_CORE}; other units fitted (most favourable) on {len(F)} FIT pages; held-out {len(I)} pages')
FREE = [u for u in INV if u not in CH_CORE]
for lang in ('latin', 'italian', 'spanish', 'portuguese'):
    pr(f' [{lang}]'); res = {}
    for k in T:
        key = h.fit_key(TF[k], lang, INV, CH_VALS, fixed=CH_CORE, iters=1500, seed=1); res[k] = h.score(key, T[k], lang); pr(row(k, res[k]))
        if k == 'voynich': pr('   fitted free units: ' + json.dumps({u: key[u] for u in FREE}))
    core_only = h.score(CH_CORE, T['voynich'], lang); pr(row('core only', core_only))
    ctrl = []
    for j in range(12):      # matched control: random permutation of the core's values, then the same fitting
        r = random.Random(100 + j); v = list(CH_CORE.values()); r.shuffle(v); rc = dict(zip(CH_CORE, v))
        ctrl.append(h.score(h.fit_key(TF['voynich'], lang, INV, CH_VALS, fixed=rc, iters=1500, seed=1), T['voynich'], lang))
    pr(f'   permuted-core + same fitting (12): M1 {S.mean(c["M1"] for c in ctrl):.2f} (min {min(c["M1"] for c in ctrl):.2f})  M2 {S.mean(c["M2"] for c in ctrl):.3f} (max {max(c["M2"] for c in ctrl):.3f})')
    pr(verdict(res['voynich'], ctrl, [v for k, v in res.items() if k != 'voynich']))
# ---------- 3. Bar: best fully fitted substitution key (any glyph -> any letter or ''), fitted on FIT pages, scored on all TEST pages
I = held(set()); F = fitpages(set()); T = texts(I); TF = texts(F); pr(f'\n=== Best fitted simple-substitution key, FIT -> TEST ({len(I)} pages)')
for lang in ('latin', 'italian'):
    pr(f' [{lang}]'); vals = sorted(set(''.join(h.CORP[lang][:20000]))) + ['']
    for k in ('voynich', 'shuf0', 'timm2001'):
        key = h.fit_key(TF[k], lang, INV, vals, iters=2500, seed=1); pr(row(k, h.score(key, T[k], lang)))
out.close()
