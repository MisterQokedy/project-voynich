"""Line/paragraph position statistics E1-E5 (see ../PREREG2.md)."""
import re, math, random, collections
import numpy as np
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.')
GAL = {'p', 'f', 't', 'k'}
def g(w): return GL.findall(w)
def js(a, b):
    k = set(a) | set(b); na, nb = sum(a.values()), sum(b.values()); d = 0
    for x in k:
        p, q = a[x] / na, b[x] / nb; m = (p + q) / 2
        d += (p * math.log2(p / m) if p else 0) + (q * math.log2(q / m) if q else 0)
    return d / 2
def E(pages):
    fi, fm, la, lm = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    li, lmid, lf = [], [], []; top, rest = [0, 0], [0, 0]
    for p in pages:
        for j, l in enumerate(p):
            if l:
                gal = sum(x in GAL for w in l for x in g(w)); t = top if j == 0 else rest; t[0] += gal; t[1] += len(l)
            if len(l) < 3: continue
            G = [g(w) or ['?'] for w in l]
            fi[G[0][0]] += 1; la[G[-1][-1]] += 1; li.append(len(G[0])); lf.append(len(G[-1]))
            for x in G[1:-1]: fm[x[0]] += 1; lm[x[-1]] += 1; lmid.append(len(x))
    return dict(E1=js(fi, fm), E2=js(la, lm), E3=np.mean(li) - np.mean(lmid), E4=np.mean(lf) - np.mean(lmid),
                E5=math.log2((top[0] / top[1] + 1e-9) / (rest[0] / rest[1] + 1e-9)))
def shuf_words(pages, r): return [[r.sample(l, len(l)) for l in p] for p in pages]
def shuf_lines(pages, r): return [r.sample(p, len(p)) for p in pages]
