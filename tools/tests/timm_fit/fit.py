"""Random-search fit of Timm generator parameters on FIT pages (see ../PREREG.md). Writes ../fit.json."""
import sys, json, random
sys.path.insert(0, './work/timm_generator/code')
from common import *
from concurrent.futures import ProcessPoolExecutor
def loss(lang, prm, seed):
    I = idx(lang, 'fit'); g = run_timm(lang, prm, seed)
    sl = {}; it = iter(g)
    for i in idx(lang): sl[i] = next(it)
    gs = st([sl[i] for i in I]); vs = TARGET[lang]
    return sum(abs(gs[k] - vs[k]) / abs(vs[k]) for k in STATS), gs
TARGET = {L: st([VLINES[i] for i in idx(L, 'fit')]) for L in 'AB'}
def draw(r):
    return dict(same_pos=r.randint(0, 60), add_remove=r.randint(0, 50), combine_split=r.randint(0, 60), replace=r.randint(20, 80),
                reuse_last=r.randint(0, 20), sugg=r.randint(0, 80), max_rep=r.randint(1, 5), dismiss=r.randint(0, 100), chooser=r.choice(['page', 'position']))
def job(a): lang, prm, seed = a; return lang, prm, seed, *loss(lang, prm, seed)
if __name__ == '__main__':
    r = random.Random(7); res = {}
    with ProcessPoolExecutor(8) as ex:
        for L in 'AB':
            cands = [DEFAULTS] + [draw(r) for _ in range(40)]
            out = list(ex.map(job, [(L, c, 101) for c in cands]))
            top = sorted(out, key=lambda x: x[3])[:3]
            re = [(t[1], [x[3] for x in ex.map(job, [(L, t[1], s) for s in (202, 303, 404)])]) for t in top]
            best = min(re, key=lambda x: sum(x[1]))
            dl = next(x[3] for x in out if x[1] is DEFAULTS or x[1] == DEFAULTS)
            res[L] = dict(best=best[0], best_losses=best[1], default_loss=dl, target=TARGET[L],
                          top3=[(t[1], round(t[3], 3)) for t in top])
            print(L, 'default loss %.3f' % dl, 'best', best[0], [round(x, 3) for x in best[1]], flush=True)
    json.dump(res, open('./work/timm_generator/fit.json', 'w'), indent=1)
