"""Step 1b: line-start effect (E1, E3) in pooled gibberish vs size-matched Voynich, each against its own within-line shuffle."""
import sys, glob, random, collections, numpy as np
sys.argv = sys.argv[:3]; exec(open('./work/gibberish/code/p1.py').read().split("r = random.Random(7)")[0])
def e13(lines, gfun):
    fi, fm = collections.Counter(), collections.Counter(); li, lm = [], []
    for l in lines:
        if len(l) < 3: continue
        G = [gfun(w) for w in l]; fi[G[0][0]] += 1; li.append(len(G[0]))
        for q in G[1:-1]: fm[q[0]] += 1; lm.append(len(q))
    return P.js(fi, fm), np.mean(li) - np.mean(lm)
def test(lines, gfun, r, n=300):
    o = e13(lines, gfun); S = np.array([e13([r.sample(l, len(l)) for l in lines], gfun) for _ in range(n)])
    return o, S.mean(0), S.std(0), (np.array(o) - S.mean(0)) / S.std(0)
r = random.Random(3)
G = []; per = []
for f in sorted(glob.glob(sys.argv_g + '/*.txt')):
    L = readlines(f); G += L; per.append(test(L, list, r, 100))
N = sum(map(len, G)); print('pooled gibberish lines', len(G), 'words', N)
o, m, s, z = test(G, list, r); print(f'GIB   E1 {o[0]:.3f} shuffle {m[0]:.3f}±{s[0]:.3f} excess {o[0]-m[0]:+.3f} z {z[0]:+.1f} | E3 {o[1]:+.2f} shuffle {m[1]:+.2f} z {z[1]:+.1f}')
ex = []
for k in range(5):
    s0 = r.randrange(len(TL)); V, c = [], 0
    while c < N: V.append(TL[s0 % len(TL)]); c += len(TL[s0 % len(TL)]); s0 += 1
    o, m, s, z = test(V, lambda w: GL.findall(w), r, 100); ex.append(o[0] - m[0])
    print(f'VOY#{k} E1 {o[0]:.3f} shuffle {m[0]:.3f}±{s[0]:.3f} excess {o[0]-m[0]:+.3f} z {z[0]:+.1f} | E3 {o[1]:+.2f} z {z[1]:+.1f}')
zs = np.array([p[3][0] for p in per]); print(f'per-writer E1 z: median {np.median(zs):+.1f}, share z>2: {np.mean(zs>2):.0%}, Stouffer {zs.sum()/np.sqrt(len(zs)):+.1f}')
ex1 = np.array([p[0][0] - p[1][0] for p in per]); print(f'per-writer E1 excess median {np.median(ex1):+.3f}  (n={len(per)})')
