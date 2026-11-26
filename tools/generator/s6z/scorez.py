"""S6-Z scoring (rule as S6-Y) + A-B gap fidelity. argv: TAG [REFTAG(optional, s6y)]"""
import sys, json, random, collections
_ARGV = list(sys.argv)
sys.path.insert(0, './work/hidden_message/code')
from hm import *
import numpy as np
V = './work/'; TAG = _ARGV[1]
D = json.load(open(V + 'manuscript_wide/pages2.json')); SHEET = [p['Q'] + p['B'] for p in D]; LANGA = [p.get('L') == 'A' for p in D]
BAND = {k: v['rand_p95'] for k, v in json.load(open(V + 's6t/s6ta.json')).items() if k in KEYS}
TR = json.load(open(V + 'timm_rules/timm_rules_pages3_1.json'))
def score(h, ref): ok = {k: abs(h[k] - ref[k]) <= BAND[k] for k in KEYS}; return int(sum(ok.values())), [k for k in KEYS if not ok[k]]
def path(tag, run, s): return V + (f's6y/out/{run}/gen_S6-Y_{s}.json' if tag == 's6y' else f's6z/out/{tag}/{run}/gen_{s}.json')
out = {}; MISS = collections.Counter(); GAP = []; allg = []
for run in ('orig', 'swap', 'r0ab', 'r0ba', 'r1ab', 'r1ba'):
    sp = json.load(open(V + f's6y/splits/{run}.json'))
    TI_ = [i for i in range(len(D)) if SHEET[i] in set(sp['test'])]
    TA = [i for i in TI_ if LANGA[i]]; TB = [i for i in TI_ if not LANGA[i]]
    T = lambda P, I=TI_: [P[i] for i in I]
    ref = full(T(VLINES)); gs = []; rA, rB = full(T(VLINES, TA)), full(T(VLINES, TB)); dreal = {k: (rA[k] - rB[k]) / BAND[k] for k in KEYS}
    for s in range(900, 905):
        try: P = json.load(open(path(TAG, run, s)))
        except FileNotFoundError: continue
        gs.append(score(full(T(P)), ref)); gA, gB = full(T(P, TA)), full(T(P, TB))
        GAP += [(dreal[k], (gA[k] - gB[k]) / BAND[k]) for k in KEYS]
    if not gs: print(run, 'no texts yet', flush=True); continue
    tm = [score(full(T(TR[s])), ref)[0] for s in list(TR)[:5]]; sh = []
    for s in range(3):
        r = random.Random(100 + s); Q = []
        for i in TI_:
            w = [x for l in VLINES[i] for x in l]; r.shuffle(w); it = iter(w); Q.append([[next(it) for _ in l] for l in VLINES[i]])
        sh.append(score(full(Q), ref)[0])
    ok = sum(n >= 20 for n, _ in gs) >= 3 and min(n for n, _ in gs) > max(tm + sh)
    for n, m in gs: MISS.update(m); allg.append(n)
    out[run] = dict(gen=[n for n, _ in gs], gen_miss=[m for _, m in gs], timm=tm, shuffle=sh, generalises=bool(ok))
    print(f"{run:5s} TEST {[n for n, _ in gs]} | Timm {tm} shuf {sh} | generalises {ok}", flush=True)
GAP = [(a, b) for a, b in GAP if np.isfinite(a) and np.isfinite(b)]; x = np.array([a for a, _ in GAP]); y = np.array([b for _, b in GAP]); slope = float((x * y).sum() / (x * x).sum()) if len(x) else float('nan')
n_ok = sum(v['generalises'] for v in out.values())
print('\nmisses:', MISS.most_common()); print(f'mean TEST {np.mean(allg):.2f} over {len(allg)} texts | directions generalised {n_ok}/{len(out)} | A-B gap slope {slope:.3f} | ' + ('PASS' if n_ok >= 5 and len(out) == 6 else 'FAIL' if len(out) == 6 else 'INCOMPLETE'))
out['_summary'] = dict(n_ok=n_ok, n=len(out), mean=float(np.mean(allg)), gap_slope=slope, misses=MISS.most_common())
json.dump(out, open(V + f's6z/score_{TAG}.json', 'w'), indent=1)
