"""Wider random-search fit (PREREG2). Writes ../fit2.json"""
import sys, json, random
sys.path.insert(0, './work/timm_generator/code')
from common import *
from pos import E
from concurrent.futures import ProcessPoolExecutor
PL = [[L['w'] for L in p['lines'] if L['w'] and L['u'] == 'P'] for p in D]
TL = {L: st([VLINES[i] for i in idx(L, 'fit')]) for L in 'AB'}
TP = {L: E([PL[i] for i in idx(L, 'fit')]) for L in 'AB'}
def job(a):
    lang, prm, seed = a; gpg = run_timm(lang, prm, seed); it = iter(gpg); sl = {i: next(it) for i in idx(lang)}
    P = [sl[i] for i in idx(lang, 'fit')]; gs = st(P); ge = E(P)
    l1 = sum(abs(gs[k] - TL[lang][k]) / abs(TL[lang][k]) for k in STATS); l2 = sum(abs(ge[k] - TP[lang][k]) / abs(TP[lang][k]) for k in ge)
    return prm, l1, l1 + l2
def draw(r):
    return dict(same_pos=r.randint(0, 100), add_remove=r.randint(0, 80), combine_split=r.randint(0, 80), replace=r.randint(20, 100),
                reuse_last=r.randint(0, 20), sugg=r.randint(0, 100), max_rep=r.randint(1, 5), dismiss=r.randint(0, 100), chooser=r.choice(['page', 'position', 'random']),
                canfollow=r.choice(['curveline', 'statistic', 'percent']), err=r.randint(0, 10), finalsub=r.choice(['true', 'false']),
                sm=r.choice(['top', 'random', 'none']), ip=r.randint(0, 40), op=r.randint(0, 40), dp=r.randint(0, 40))
if __name__ == '__main__':
    r = random.Random(77); old = json.load(open('./work/timm_generator/fit.json')); res = {}
    with ProcessPoolExecutor(4) as ex:
        for L in 'AB':
            cands = [dict(DEFAULTS), dict(DEFAULTS, **old[L]['best'])] + [draw(r) for _ in range(150)]
            out = [x for x in ex.map(job, [(L, c, 101) for c in cands], timeout=None)]
            res[L] = {}
            for key, col in (('G1', 1), ('G2', 2)):
                top = sorted(out, key=lambda x: x[col])[:5]
                re_ = [(t[0], [x[col] for x in ex.map(job, [(L, t[0], s) for s in (202, 303, 404)])]) for t in top]
                b = min(re_, key=lambda x: sum(x[1])); res[L][key] = dict(best=b[0], losses=[round(v, 3) for v in b[1]])
                print(L, key, b[0], [round(v, 3) for v in b[1]], 'prev-best loss1 %.3f' % out[1][1], flush=True)
    json.dump(res, open('./work/timm_generator/fit2.json', 'w'), indent=1)
