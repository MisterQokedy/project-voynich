"""S6-Y scoring: S6-T-c rule on 6 directions + page drift on TEST pages, S6-V alongside."""
import sys, json, random, io, contextlib, collections
sys.path.insert(0, './work/hidden_message/code')
from hm import *
V = './work/'
import numpy as np
GL_ = ['d', 'q', 't', 'l', 'a']
def _lineft(l):
    w = l[1:]
    if not w: return None
    G = [x for v in w for x in gg(v)]; c = collections.Counter(G); n = max(len(G), 1); f = [c[g] / n for g in GL_]
    return f[3] + f[4] - f[0] - f[1] - f[2]
_rk = lambda a: np.argsort(np.argsort(a, kind='stable')).astype(float)
def delta(pages):
    out = []
    for pg in pages:
        F = [_lineft(l) for l in pg if l]; F = [f for f in F if f is not None]
        if len(F) >= 8:
            c = np.corrcoef(_rk(np.arange(len(F))), _rk(np.array(F)))[0, 1]
            if c == c: out.append(c)
    return float(np.mean(out)) if out else 0.0
D = json.load(open(V + 'manuscript_wide/pages2.json')); SHEET = [p['Q'] + p['B'] for p in D]
BAND = {k: v['rand_p95'] for k, v in json.load(open(V + 's6t/s6ta.json')).items() if k in KEYS}
TR = json.load(open(V + 'timm_rules/timm_rules_pages3_1.json')); PREV = json.load(open(V + 's6v/s6vc.json'))
def score(h, ref): ok = {k: abs(h[k] - ref[k]) <= BAND[k] for k in KEYS}; return int(sum(ok.values())), [k for k in KEYS if not ok[k]]
out = {}; MISS = collections.Counter()
for run in ('orig', 'swap', 'r0ab', 'r0ba', 'r1ab', 'r1ba'):
    sp = json.load(open(V + f's6y/splits/{run}.json'))
    TI_ = [i for i in range(len(D)) if SHEET[i] in set(sp['test'])]; FI_ = [i for i in range(len(D)) if SHEET[i] in set(sp['fit'])]
    T = lambda P: [P[i] for i in TI_]
    ref = full(T(VLINES)); reff = full([VLINES[i] for i in FI_]); dreal = delta(T(VLINES)); gs = []; ins = []; dg = []
    for s in range(900, 905):
        try: P = json.load(open(V + f's6y/out/{run}/gen_S6-Y_{s}.json'))
        except FileNotFoundError: continue
        gs.append(score(full(T(P)), ref)); ins.append(score(full([P[i] for i in FI_]), reff)[0]); dg.append(round(delta(T(P)), 3))
    if not gs: print(run, 'no texts yet', flush=True); continue
    dv = [round(delta(T(json.load(open(V + f's6v/out/{run}/gen_S6-V_{s}.json')))), 3) for s in (900, 901, 902)]
    tm = [score(full(T(TR[s])), ref)[0] for s in list(TR)[:5]]; sh = []
    for s in range(3):
        r = random.Random(100 + s); Q = []
        for i in TI_:
            w = [x for l in VLINES[i] for x in l]; r.shuffle(w); it = iter(w); Q.append([[next(it) for _ in l] for l in VLINES[i]])
        sh.append(score(full(Q), ref)[0])
    ok = sum(n >= 20 for n, _ in gs) >= 3 and min(n for n, _ in gs) > max(tm + sh); d25 = sum(abs(x - dreal) <= 0.06 for x in dg) >= 3
    for _, m in gs: MISS.update(m)
    out[run] = dict(gen=[n for n, _ in gs], gen_miss=[m for _, m in gs], insample=ins, s6v=PREV[run]['gen'], timm=tm, shuffle=sh, generalises=bool(ok), delta_gen=dg, delta_real=dreal, delta_s6v=dv, delta_ok=bool(d25))
    print(f"{run:5s} S6-Y TEST {[n for n, _ in gs]} (S6-V {PREV[run]['gen']}) in-sample {ins} | drift {dg} real {dreal:+.3f} S6-V {dv} ok {d25} | Timm {tm} shuf {sh} | generalises {ok}", flush=True)
n_ok = sum(v['generalises'] for v in out.values()); nd = sum(v['delta_ok'] for v in out.values())
print('\nmisses:', MISS.most_common()); print('directions generalised:', n_ok, '/', len(out), '| drift ok', nd, '/', len(out), '| S6-Y', 'PASS' if n_ok >= 5 and len(out) == 6 else 'FAIL' if len(out) == 6 else 'INCOMPLETE')
out['_summary'] = dict(n_ok=n_ok, n=len(out), delta_ok=nd); json.dump(out, open(V + 's6y/s6yc.json', 'w'), indent=1)
