"""Z2-b scoring of S27/S28 on held-out TEST pages. Band = p95 of |half1 - half2| over 200 random sheet half-splits of the real text (as s6t/s6ta).
argv: TAG [TAG ...] (s6y | z1b | ...). Controls: Timm+rules (5 texts), within-page shuffle (3)."""
import sys, json, random, collections
_ARGV = list(sys.argv)
sys.path.insert(0, './work/hidden_message/code')
from hm import VLINES
import numpy as np
V = './work/'
exec(open(V + 's6z/code/oneoff.py').read())
D = json.load(open(V + 'manuscript_wide/pages2.json')); SHEET = [p['Q'] + p['B'] for p in D]; SH = sorted(set(SHEET))
BF = V + 's6z/z2b/bands27.json'
try: BAND = json.load(open(BF))
except FileNotFoundError:
    dd = {'S27': [], 'S28': []}
    for s in range(200):
        r = random.Random(s); x = SH[:]; r.shuffle(x); a = set(x[:len(x) // 2])
        ha = oneoff([VLINES[i] for i in range(len(D)) if SHEET[i] in a]); hb = oneoff([VLINES[i] for i in range(len(D)) if SHEET[i] not in a])
        for k in dd: dd[k].append(abs(ha[k] - hb[k]))
    BAND = {k: float(np.percentile(v, 95)) for k, v in dd.items()}; json.dump(BAND, open(BF, 'w'))
print('bands', BAND)
TR = json.load(open(V + 'timm_rules/timm_rules_pages3_1.json'))
def path(tag, run, s): return V + (f's6y/out/{run}/gen_S6-Y_{s}.json' if tag == 's6y' else f's6z/out/{tag}/{run}/gen_{s}.json')
res = {}
for tag in _ARGV[1:]:
    res[tag] = {}; npass = 0
    for run in ('orig', 'swap', 'r0ab', 'r0ba', 'r1ab', 'r1ba'):
        sp = json.load(open(V + f's6y/splits/{run}.json')); TI_ = [i for i in range(len(D)) if SHEET[i] in set(sp['test'])]
        T = lambda P: [P[i] if not isinstance(P, dict) else P[str(i)] for i in TI_]
        ref = oneoff(T(VLINES)); rows = []
        for s in range(900, 905):
            try: P = json.load(open(path(tag, run, s)))
            except FileNotFoundError: continue
            if isinstance(P, dict): P = [P[str(i)] for i in range(len(D))]
            o = oneoff(T(P)); rows.append((o, all(abs(o[k] - ref[k]) <= BAND[k] for k in BAND)))
        tm = [oneoff(T(TR[s])) for s in list(TR)[:5]]
        sh = []
        for s in range(3):
            r = random.Random(100 + s); Q = []
            for i in TI_:
                w = [x for l in VLINES[i] for x in l]; r.shuffle(w); it = iter(w); Q.append([[next(it) for _ in l] for l in VLINES[i]])
            sh.append(oneoff(Q))
        ok = sum(p for _, p in rows) >= 3; npass += ok
        f = lambda L, k: ' '.join(f"{o[k]:.3f}" for o in L)
        print(f"{tag:6s} {run:5s} real S27 {ref['S27']:.3f} S28 {ref['S28']:.3f} | gen S27 {f([o for o, _ in rows], 'S27')} S28 {f([o for o, _ in rows], 'S28')} | both-in-band {sum(p for _, p in rows)}/{len(rows)} | Timm S27 {f(tm, 'S27')} S28 {f(tm, 'S28')} | shuf S28 {f(sh, 'S28')}", flush=True)
        res[tag][run] = dict(real=ref, gen=[o for o, _ in rows], inband=[p for _, p in rows], timm=tm, shuf=sh, dir_pass=bool(ok))
    print(f"{tag}: directions with S27+S28 in band on >=3/5 seeds: {npass}/6", flush=True)
json.dump(res, open(V + 's6z/z2b/score27_' + '_'.join(_ARGV[1:]) + '.json', 'w'), indent=1)
