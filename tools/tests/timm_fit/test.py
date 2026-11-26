"""Held-out comparison and pre-registered key test (see ../PREREG.md). Output: ../results.out"""
import sys, json, random, collections
import numpy as np
sys.path.insert(0, './work/timm_generator/code'); sys.path.insert(0, './work/word_families/code')
from common import *
import wf
from concurrent.futures import ProcessPoolExecutor
FIT = json.load(open('./work/timm_generator/fit.json'))
SEEDS = list(range(1001, 1011))
TEST = idx(None, 'test'); TA = idx('A', 'test'); TB = idx('B', 'test')
def gen(seed): return to_slots(run_timm('A', FIT['A']['best'], seed), run_timm('B', FIT['B']['best'], seed))
def flat(P): return [[w for l in p for w in l] for p in P]
def R_only(pages, I, f, splits=20, sd=5):
    rng = random.Random(sd); S = sorted({SHEET[i] for i in I}); out = []
    for _ in range(splits):
        rng.shuffle(S); h = set(S[:len(S) // 2])
        A = [pages[i] for i in I if SHEET[i] in h]; B = [pages[i] for i in I if SHEET[i] not in h]
        c = wf.profile([w for p in A for w in p], f); ct = wf.profile([w for p in B for w in p], f)
        fams = [x for x in c if c[x] >= 10 and ct[x] >= 3]
        if len(fams) >= 5: out.append(np.corrcoef(wf.assoc(A, f, fams), wf.assoc(B, f, fams))[0, 1])
    return float(np.mean(out))
def t3(pages, I, f): return wf.t3(pages, SHEET, I, f, random.Random(5))
def seedjob(seed):
    G = gen(seed); P = flat(G); o = {'stats_all': st([G[i] for i in TEST]), 'stats_A': st([G[i] for i in TA]), 'stats_B': st([G[i] for i in TB])}
    for nm, I in (('all', TEST), ('A', TA), ('B', TB)):
        o['F1_' + nm] = R_only(P, I, wf.F1); o['W_' + nm] = R_only(P, I, wf.W)
    o['t3F1_all'] = t3(P, TEST, wf.F1)
    return o
def randfam(k):
    r = random.Random(k); types = sorted({w for i in TEST for w in VP[i]}); bysize = collections.Counter(wf.F1(w) for w in types)
    sizes = list(bysize.values()); r.shuffle(types); m, j = {}, 0
    for n, s in enumerate(sizes):
        for w in types[j:j + s]: m[w] = n
        j += s
    return R_only(VP, TEST, lambda w: m[w]), R_only(VP, TA, lambda w: m[w]), R_only(VP, TB, lambda w: m[w])
VP = flat(VLINES)
if __name__ == '__main__':
    out = open('./work/timm_generator/results.out', 'w')
    def pr(*a): print(*a, flush=True); print(*a, file=out, flush=True)
    pr('fit:', json.dumps({L: dict(best=FIT[L]['best'], default_loss=round(FIT[L]['default_loss'], 3), best_losses=[round(x, 3) for x in FIT[L]['best_losses']]) for L in 'AB'}))
    with ProcessPoolExecutor(4) as ex:
        GS = list(ex.map(seedjob, SEEDS)); RF = list(ex.map(randfam, range(200)))
    # 1. language statistics on TEST
    ch = [c for c in wf_chunks] if False else None
    T = [w for i in TEST for w in VP[i]]
    chunks, cur = [], []
    for i in TEST:
        cur.append(VLINES[i])
        if sum(len(l) for p in cur for l in p) >= 5000: chunks.append(cur); cur = []
    CS = [st(c) for c in chunks]
    for nm, I in (('all', TEST), ('A', TA), ('B', TB)):
        V = st([VLINES[i] for i in I]); nmatch = 0; rows = []
        for k in STATS:
            g = np.array([o['stats_' + nm][k] for o in GS]); sdc = np.std([c[k] for c in CS]) if nm == 'all' else 0.0
            z = (V[k] - g.mean()) / np.sqrt(g.std() ** 2 + sdc ** 2 + 1e-12); nmatch += abs(z) < 2
            rows.append(f'  {k:12s} voy {V[k]:8.3f}  gen {g.mean():8.3f} ± {g.std():.3f}  z {z:6.1f}')
        pr(f'== TEST stats, {nm} pages (match |z|<2: {nmatch}/{len(STATS)}; chunk sd used: {nm == "all"}, {len(CS)} chunks)'); [pr(r) for r in rows]
    # 2/3. key test
    vt = t3(VP, TEST, wf.F1); pr('== Voynich TEST T3 F1 (full, with z):', vt)
    pr('   generator TEST T3 F1 (seed 1001):', GS[0]['t3F1_all'])
    shuf = wf.shuffle_pages(VP, random.Random(9))
    for nm, I, j in (('all', TEST, 0), ('A', TA, 1), ('B', TB, 2)):
        f1, w = R_only(VP, I, wf.F1), R_only(VP, I, wf.W); G = f1 - w
        gG = np.array([o['F1_' + nm] - o['W_' + nm] for o in GS]); gF = np.array([o['F1_' + nm] for o in GS]); gW = np.array([o['W_' + nm] for o in GS])
        rf = np.array([x[j] for x in RF]); rfG = rf - w
        pr(f'== Key test [{nm}]  Voynich R_F1 {f1:.3f}  R_W {w:.3f}  G {G:.3f}  ratio {f1 / w:.2f}')
        pr(f'   fitted Timm (10 seeds): R_F1 {gF.mean():.3f}±{gF.std():.3f}  R_W {gW.mean():.3f}±{gW.std():.3f}  G {gG.mean():.3f}±{gG.std():.3f} (max {gG.max():.3f})  Voynich G > all seeds: {bool(G > gG.max())}')
        pr(f'   random families (200): R {rf.mean():.3f}±{rf.std():.3f}  G_rand 95th pct {np.percentile(rfG, 95):.3f}  Voynich G > 95th: {bool(G > np.percentile(rfG, 95))}  p = {((rfG >= G).sum() + 1) / 201:.3f}')
        pr(f'   shuffled Voynich: R_F1 {R_only(shuf, I, wf.F1):.3f}  R_W {R_only(shuf, I, wf.W):.3f}')
