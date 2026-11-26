import sys, os; sys.path.insert(0, './work/oneoffs/code')
from oo import *
D = json.load(open(V + 'manuscript_wide/pages2.json')); SHEET = [p['Q'] + p['B'] for p in D]
from_lines = lambda p: [w for l in p for w in l]
real = [from_lines([l['w'] for l in p['lines'] if l['u'] == 'P']) for p in D]
def curve(pages, idx):
    T = [w for i in idx for w in pages[i]]; c = collections.Counter(T)
    return {L: np.mean([c[w] == 1 for w in T if len(w) == L]) for L in (8, 10)}
log = {}
for run in ('orig', 'swap', 'r0ab', 'r0ba', 'r1ab', 'r1ba'):
    sp = json.load(open(V + f's6y/splits/{run}.json')); FI = [i for i in range(len(D)) if SHEET[i] in set(sp['fit'])]; TI = [i for i in range(len(D)) if SHEET[i] in set(sp['test'])]
    c = collections.Counter(w for i in FI for w in real[i]); hp = [w for i in FI for w in real[i] if c[w] == 1 and len(w) >= 7]
    ON = [onset(w) for w in hp]; EN = [w[-2:] for w in hp]; MID = collections.defaultdict(list)
    for w in hp: MID[len(w) - len(onset(w)) - 2].append(w[len(onset(w)):-2])
    tgtF = curve(real, FI); tgtT = curve(real, TI); best = None
    for q in (0.3, 0.5, 0.7, 0.9):
        outs = []
        for s in range(900, 905):
            G = json.load(open(V + f's6z/out/S6Z_reference/{run}/gen_{s}.json')); rng = random.Random(s * 10 + int(q * 10)); seen = set(w for p in G for l in p for w in l); used = set()
            H = []
            for p in G:
                Q = []
                for l in p:
                    L2 = []
                    for w in l:
                        if len(w) >= 7 and w in used and rng.random() < q:
                            for _ in range(20):
                                o = rng.choice(ON); e = rng.choice(EN); m = MID.get(len(w) - len(o) - 2)
                                if not m: continue
                                nw = o + rng.choice(m) + e
                                if nw not in seen: w = nw; seen.add(nw); break
                        used.add(w); L2.append(w)
                    Q.append(L2)
                H.append(Q)
            outs.append(H)
        gF = [curve([from_lines(p) for p in H], FI) for H in outs]; err = np.mean([abs(g[L] - tgtF[L]) for g in gF for L in (8, 10)])
        if best is None or err < best[0]: best = (err, q, outs)
    err, q, outs = best; os.makedirs(V + f's6z/out/oog/{run}', exist_ok=True)
    for s, H in zip(range(900, 905), outs): json.dump(H, open(V + f's6z/out/oog/{run}/gen_{s}.json', 'w'))
    gT = [curve([from_lines(p) for p in H], TI) for H in outs]; base = [curve([from_lines(p) for p in json.load(open(V + f's6z/out/S6Z_reference/{run}/gen_{s}.json'))], TI) for s in range(900, 905)]
    ok = all(abs(np.mean([g[L] for g in gT]) - tgtT[L]) <= 0.10 for L in (8, 10))
    log[run] = dict(q=q, real_test=tgtT, oog_test={L: float(np.mean([g[L] for g in gT])) for L in (8, 10)}, ref_test={L: float(np.mean([g[L] for g in base])) for L in (8, 10)}, within=ok)
    print(run, log[run], flush=True)
print('hapax-by-length within 0.10 on', sum(v['within'] for v in log.values()), '/6 directions')
json.dump(log, open(OUT + 'oog.json', 'w'), indent=1, default=float)
