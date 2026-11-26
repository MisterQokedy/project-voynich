"""Z5 scoring: the 24-statistic rule (scorez.py) plus A4 as statistic 25, on held-out TEST pages, per direction.
A4(gen) = A4(gen FIT pages -> gen TEST pages); real = A4(real FIT -> real TEST); band = real ± 2·max(sd, 0.1·|real|), sd from 200 bootstrap
resamples of TEST sheets (as meaning_procedure A4-P). Generalises (25) = ≥ 3/5 seeds with ≥ 21/25 and every seed above all controls.
argv: TAG [TAG ...]; needs score_<TAG>.json from scorez.py."""
import sys, json, random, collections
_ARGV = list(sys.argv)
sys.path.insert(0, './work/hidden_message/code')
from hm import *
import numpy as np
V = './work/'
exec(open(V + 's6z/code/a4lib.py').read())
D = json.load(open(V + 'manuscript_wide/pages2.json')); SHEET = [p['Q'] + p['B'] for p in D]
BAND = {k: v['rand_p95'] for k, v in json.load(open(V + 's6t/s6ta.json')).items() if k in KEYS}
TR = json.load(open(V + 'timm_rules/timm_rules_pages3_1.json'))
def path(tag, run, s): return V + (f's6y/out/{run}/gen_S6-Y_{s}.json' if tag == 's6y' else f's6z/out/{tag}/{run}/gen_{s}.json')
BF = V + 's6z/z5/a4bands.json'
try: AB = json.load(open(BF))
except FileNotFoundError: AB = {}
res = {}
for tag in _ARGV[1:]:
    S24 = json.load(open(V + f's6z/score_{tag}.json')); res[tag] = {}; allg = []; nok = 0
    for run in ('orig', 'swap', 'r0ab', 'r0ba', 'r1ab', 'r1ba'):
        sp = json.load(open(V + f's6y/splits/{run}.json')); TI_ = [i for i in range(len(D)) if SHEET[i] in set(sp['test'])]; FI_ = [i for i in range(len(D)) if i not in set(TI_)]
        F = [VLINES[i] for i in FI_]; T = [VLINES[i] for i in TI_]
        if run not in AB:
            v = A4(F, T, np.random.default_rng(5)); rng = np.random.default_rng(6); sh = collections.defaultdict(list)
            for j, i in enumerate(TI_): sh[SHEET[i]].append(j)
            keys = list(sh); bs = [A4(F, [T[j] for k in rng.choice(len(keys), len(keys)) for j in sh[keys[k]]], rng, nsh=5) for _ in range(200)]
            sd = max(float(np.std(bs)), 0.1 * abs(v)); AB[run] = dict(real=v, sd=sd, band=[v - 2 * sd, v + 2 * sd]); json.dump(AB, open(BF, 'w'), indent=1)
        lo, hi = AB[run]['band']; n24 = S24[run]['gen']; g25 = []; a4s = []
        for s, n in zip(range(900, 905), n24):
            P = json.load(open(path(tag, run, s))); a = A4([P[i] for i in FI_], [P[i] for i in TI_], np.random.default_rng(1)); a4s.append(a); g25.append(n + int(lo <= a <= hi))
        ctl = []
        for n, s in zip(S24[run]['timm'], list(TR)[:5]):
            P = TR[s]; a = A4([P[i] for i in FI_], [P[i] for i in TI_], np.random.default_rng(1)); ctl.append(n + int(lo <= a <= hi))
        for n, s in zip(S24[run]['shuffle'], range(3)):
            r = random.Random(100 + s); Q = []
            for i in TI_:
                w = [x for l in VLINES[i] for x in l]; r.shuffle(w); it = iter(w); Q.append([[next(it) for _ in l] for l in VLINES[i]])
            a = A4(F, Q, np.random.default_rng(1)); ctl.append(n + int(lo <= a <= hi))
        ok = sum(x >= 21 for x in g25) >= 3 and min(g25) > max(ctl); nok += ok; allg += g25
        res[tag][run] = dict(n25=g25, A4=a4s, A4_in=[lo <= a <= hi for a in a4s], controls25=ctl, generalises25=bool(ok))
        print(f"{tag:5s} {run:5s} 25-stat {g25} | A4 {' '.join(f'{a:+.4f}' for a in a4s)} band [{lo:+.4f}, {hi:+.4f}] in {sum(lo <= a <= hi for a in a4s)}/5 | controls {ctl} | generalises {ok}", flush=True)
    res[tag]['_summary'] = dict(mean25=float(np.mean(allg)), n_ok=nok, mean24=S24['_summary']['mean'])
    print(f"{tag}: mean TEST 25-stat {np.mean(allg):.2f} | 24-stat {S24['_summary']['mean']:.2f} | directions generalising (25) {nok}/6", flush=True)
json.dump(res, open(V + 's6z/z5/score25_' + '_'.join(_ARGV[1:]) + '.json', 'w'), indent=1)
