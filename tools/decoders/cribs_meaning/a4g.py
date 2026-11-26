# A4-G: add an onset-alternation habit or a pair copy (x y x') to the hybrid on Currier B pages; does it reproduce A4? See ../PREREG2.md
import sys, json, random, collections
ARGV = list(sys.argv)
sys.path.insert(0, './work/meaning_procedure/code')
from hybrid import *
import numpy as np
P0 = json.load(open('./work/hybrid_gen/final_test.json'))['params']
for k in INTS: P0[k] = int(round(P0[k]))
META = json.load(open('./work/manuscript_wide/pages2.json'))
BF = [META[i].get('L') == 'B' for i in FI]; BT = [META[i].get('L') == 'B' for i in TI]
def gen_a(shapes, isB, prm, seed, mech, a):
    r = random.Random(seed); out = []; hist = []
    for pi, p in enumerate(shapes):
        q = []; page = list(hist[-prm['carry']:]) if prm['carry'] else []; pend = [split3(x)[2] for x in page]
        for li, l in enumerate(p):
            words = []
            for k in range(len(l)):
                def step():
                    if k == 0: return draw(dist(PGw if li == 0 else LIw, prm['tauL'], ('L', li == 0)), r)
                    prev = words[-1]; pd = onset_probs(prev, prm); src = page[-prm['W']:]
                    if prev in WBI and r.random() < prm['pw']:
                        w = draw(dist(WBI[prev], prm['tauw'], ('wb', prev)), r)
                        if r.random() < prm['mu'] * prm['mw']: w = mutate(w, r, prm)
                    elif src and r.random() < prm['pc']:
                        cand = [src[r.randrange(len(src))] for _ in range(prm['K'])]
                        wt = [(pd.get(gg(c)[0], 0) + 1e-4) ** prm['beta'] for c in cand]
                        w = r.choices(cand, wt)[0]
                        if r.random() < prm['mu']: w = mutate(w, r, prm)
                        if r.random() < 1 - prm['keepE']:
                            f, b_, e = split3(w); w = f + b_ + new_ending(b_, f, split3(prev)[2], r, prm)
                    else:
                        f = draw((list(pd), list(pd.values())), r); w = fresh(f, prev, page, pend, r, prm)
                    return w or prev
                if isB[pi] and k >= 2 and a > 0 and r.random() < a:
                    two = words[-2]
                    if mech == 'pair': w = mutate(two, r, prm) if r.random() < 0.7 else two
                    else:
                        want = gg(two)[0]; w = None
                        for _ in range(60):
                            x = step()
                            if gg(x)[0] == want: w = x; break
                        if w is None: w = fresh(want, words[-1], page, pend, r, prm) or two
                else: w = step()
                words.append(w); page.append(w); pend.append(split3(w)[2])
            q.append(words)
        hist = page
        out.append(rule([q], prm['q'], r)[0] if prm['q'] > 0 else q)
    return out
# ---- A4 measures (same as code/d3b_d2a.py)
_s = open('./work/meaning_procedure/code/d3b_d2a.py').read()
exec(_s[_s.index("def slot_seqs("):_s.index("def d2a(")])
import re as _re
ENDR = _re.compile(r'(aiin|ain|iin|eedy|edy|dy|eey|ey|ol|or|ar|al|am|y|s|r|l|n|m)$')
def v_end(w):
    g = gg(w); rest = ''.join(g[1:]); m = ENDR.search(rest); return m.group(1) if m else ('-' + (g[-1] if len(g) == 1 else ''))
def A4(F, T, rng, nsh=20):
    F = [[l for l in p if l] for p in F]; T = [[l for l in p if l] for p in T]
    voc = {'on': {}, 'en': {}}; FS, TS = Seq(slot_seqs(F, gg, v_end), voc), Seq(slot_seqs(T, gg, v_end), voc); nx = len(voc['on'])
    g = dep_gain(FS, TS, 2, 'on', 'on', nx, nx); sh = np.mean([dep_gain(FS.shuffled(rng), TS.shuffled(rng), 2, 'on', 'on', nx, nx) for _ in range(nsh)]); return float(g - sh)
def rep2x(P, rng):
    L = [l for p in P for l in p if l]
    def f(L):
        n = c = 0
        for l in L:
            for i in range(len(l) - 2):
                n += 1; c += (l[i] != l[i + 2] and gg(l[i])[0] == gg(l[i + 2])[0])
        return c / max(n, 1)
    return f(L) - np.mean([f([list(rng.permutation(l)) for l in L]) for _ in range(5)])
def internal(P):
    A = [p for i, p in enumerate(P) if (i // 4) % 2 == 0]; B = [p for i, p in enumerate(P) if (i // 4) % 2 == 1]; return A, B
def a4_report(F, T, Fb, Tb, rng):
    out = dict(A4=A4(F, T, rng), rep2x=rep2x(T, rng))
    out['A4_A'] = A4([p for p, b in zip(F, Fb) if not b], [p for p, b in zip(T, Tb) if not b], rng)
    out['A4_B'] = A4([p for p, b in zip(F, Fb) if b], [p for p, b in zip(T, Tb) if b], rng)
    return out
def zsum(g, ref): return sum(abs(g[k] - ref[k]) / SD[k] for k in KEYS)
def fitrun(arg):
    mech, a = arg; rng = np.random.default_rng(1)
    F = gen_a(FITSH, BF, P0, 11, mech, a); g, ok, loss = score_on(F, FITREF); fa, fb = internal(F)
    return dict(mech=mech, a=a, n=int(sum(ok.values())), z=zsum(g, FITREF), A4_int=A4(fa, fb, rng), misses=[k for k in ok if not ok[k]])
if __name__ == '__main__':
    import multiprocessing as mp
    rng = np.random.default_rng(1)
    va, vb = internal(FITSH); V_int = A4(va, vb, rng); VT = a4_report(FITSH, TESTSH, BF, BT, rng)
    print('Voynich FIT-internal A4', round(V_int, 4), '| Voynich TEST', {k: round(v, 4) for k, v in VT.items()}, flush=True)
    grid = [(m, a) for m in ('onset', 'pair') for a in (0, 0.05, 0.10, 0.15, 0.20, 0.30)]
    with mp.Pool(int(ARGV[1]) if len(ARGV) > 1 else 3) as pool: rows = pool.map(fitrun, grid)
    for x in rows: print(f"FIT {x['mech']:5} a {x['a']:.2f}: {x['n']}/24 |z| {x['z']:.1f} A4_int {x['A4_int']:+.4f} misses {x['misses']}", flush=True)
    OUT = dict(voynich_fit_internal=V_int, voynich_test=VT, grid=rows, test={})
    for mech in ('onset', 'pair'):
        ok_rows = [x for x in rows if x['mech'] == mech and x['n'] >= 20] or [x for x in rows if x['mech'] == mech]
        best = min(ok_rows, key=lambda x: (abs(x['A4_int'] - V_int), x['z'])); print('chosen', mech, best['a'], flush=True)
        for a in sorted({best['a'], 0}):
            res = []; npass = 0
            for sd in range(900, 905):
                F = gen_a(FITSH, BF, P0, sd + 1000, mech, a); T = gen_a(TESTSH, BT, P0, sd, mech, a); g, ok, loss = score_on(T, REF)
                rep = a4_report(F, T, BF, BT, np.random.default_rng(sd)); n = int(sum(ok.values()))
                p_ = n >= 20 and ok['R'] and ok['d1d2'] and 0.0054 <= rep['A4'] <= 0.0162 and rep['A4_A'] <= 0.003 and rep['A4_B'] >= 0.006; npass += p_
                res.append(dict(seed=sd, n=n, R_ok=bool(ok['R']), d1d2_ok=bool(ok['d1d2']), misses=[k for k in ok if not ok[k]], **rep, passed=bool(p_)))
                print(f"TEST {mech} a {a}: seed {sd} {n}/24 A4 {rep['A4']:+.4f} A {rep['A4_A']:+.4f} B {rep['A4_B']:+.4f} rep2x {rep['rep2x']:+.4f} pass {p_} misses {[k for k in ok if not ok[k]]}", flush=True)
            OUT['test'][f'{mech}_{a}'] = dict(runs=res, npass=npass); print(f'{mech} a {a}: {npass}/5 ->', 'PASS' if npass >= 3 else 'FAIL', flush=True)
            json.dump(OUT, open('./work/meaning_procedure/a4g.json', 'w'), indent=1)
