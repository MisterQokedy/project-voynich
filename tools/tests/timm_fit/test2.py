"""Held-out position tests + language stats for wider-fit winners G1, G2 (PREREG2). Output ../results2.out"""
import sys, json, random
import numpy as np
sys.path.insert(0, './work/timm_generator/code')
from common import *
from pos import E, shuf_words, shuf_lines
from concurrent.futures import ProcessPoolExecutor
F2 = json.load(open('./work/timm_generator/fit2.json'))
PL = [[L['w'] for L in p['lines'] if L['w'] and L['u'] == 'P'] for p in D]
TEST = idx(None, 'test'); SEEDS = range(1001, 1011); K = ['E1', 'E2', 'E3', 'E4', 'E5']
def job(a):
    key, seed = a; G = to_slots(run_timm('A', F2['A'][key]['best'], seed), run_timm('B', F2['B'][key]['best'], seed))
    o = {}
    for nm in ('all', 'A', 'B'):
        I = TEST if nm == 'all' else idx(nm, 'test'); o[nm] = (E([G[i] for i in I]), st([G[i] for i in I]))
    return key, o
def boot(I, r):
    sh = sorted({SHEET[i] for i in I}); out = []
    for _ in range(200):
        pick = [r.choice(sh) for _ in sh]; out.append(E([PL[i] for s in pick for i in I if SHEET[i] == s]))
    return {k: np.std([x[k] for x in out]) for k in K}
if __name__ == '__main__':
    f = open('./work/timm_generator/results2.out', 'w')
    def pr(*a): print(*a, flush=True); print(*a, file=f, flush=True)
    with ProcessPoolExecutor(4) as ex: R = list(ex.map(job, [(k, s) for k in ('G1', 'G2') for s in SEEDS]))
    r = random.Random(3)
    for nm in ('all', 'A', 'B'):
        I = TEST if nm == 'all' else idx(nm, 'test'); V = E([PL[i] for i in I]); se = boot(I, r)
        nw = [E(shuf_words([PL[i] for i in I], r)) for _ in range(100)]; nl = [E(shuf_lines([PL[i] for i in I], r)) for _ in range(100)]
        pr(f'== Position effects, TEST {nm} pages')
        for k in K:
            null = np.array([x[k] for x in (nl if k == 'E5' else nw)]); real = V[k] > np.percentile(null, 99)
            row = f'  {k}: voy {V[k]:7.3f} (se {se[k]:.3f}; null 99th {np.percentile(null, 99):.3f}; real {real})'
            for key in ('G1', 'G2'):
                gv = np.array([o[nm][0][k] for kk, o in R if kk == key]); z = (V[k] - gv.mean()) / np.sqrt(gv.std() ** 2 + se[k] ** 2)
                row += f' | {key} {gv.mean():7.3f}±{gv.std():.3f} z {z:5.1f}'
            pr(row)
    if True:
        P = [p for p in D]; para = [[L['w'] for L in p['lines'] if L['w'] and L['u'] == 'P'] for p in D]
        # descriptive: Voynich paragraph-initial (@) lines vs other P lines, gallows per word
        a = b = na = nb = 0
        import pos
        for i in TEST:
            for L in D[i]['lines']:
                if L['u'] != 'P' or not L['w']: continue
                gal = sum(x in pos.GAL for w in L['w'] for x in pos.g(w))
                if L.get('mark') == '@': a += gal; na += len(L['w'])
                else: b += gal; nb += len(L['w'])
        pr(f'  descriptive: Voynich TEST paragraph-initial lines gallows/word {a/na:.3f} vs other lines {b/nb:.3f}')
    pr('== Language stats on TEST (all pages): Voynich vs G1 / G2')
    V = st([VLINES[i] for i in TEST])
    for k in STATS:
        row = f'  {k:12s} voy {V[k]:8.3f}'
        for key in ('G1', 'G2'):
            gv = np.array([o['all'][1][k] for kk, o in R if kk == key]); row += f' | {key} {gv.mean():8.3f}±{gv.std():.3f}'
        pr(row)
