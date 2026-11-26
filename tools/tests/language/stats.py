import math, random, collections
import numpy as np
def chunks(pages, n=5000):
    out, cur, c = [], [], 0
    for p in pages:
        cur.append(p); c += sum(len(l) for l in p)
        if c >= n: out.append(cur); cur, c = [], 0
    return out
def H2(toks):
    s = ' ' + ' '.join(toks) + ' '; big = collections.Counter(zip(s, s[1:])); uni = collections.Counter(s[:-1]); N = len(s) - 1
    return -sum(c / N * math.log2(c / uni[a]) for (a, b), c in big.items())
def MI(seq):
    pairs = list(zip(seq, seq[1:])); N = len(pairs); pc = collections.Counter(pairs)
    a = collections.Counter(x for x, _ in pairs); b = collections.Counter(y for _, y in pairs)
    return sum(c / N * math.log2(c * N / (a[x] * b[y])) for (x, y), c in pc.items())
def ed1(a, b):
    if a == b or abs(len(a) - len(b)) > 1: return False
    if len(a) == len(b): return sum(x != y for x, y in zip(a, b)) == 1
    if len(a) > len(b): a, b = b, a
    i = 0
    while i < len(a) and a[i] == b[i]: i += 1
    return a[i:] == b[i + 1:]
def stats(ch, r):
    P = [[w for l in p for w in l] for p in ch]; T = [w for p in P for w in p]
    L = np.array([len(w) for w in T]); f = np.array(sorted(collections.Counter(T).values(), reverse=True)[:100], float)
    zipf = np.polyfit(np.log(np.arange(1, len(f) + 1)), np.log(f), 1)[0]
    types = len(set(T[:5000]))
    seq = lambda pp: [w for p in pp for w in p + ['#']]
    def shuf_pages(pp): return [r.sample(p, len(p)) for p in pp]
    s6 = MI(seq(P)) - np.mean([MI(seq(shuf_pages(P))) for _ in range(5)])
    def disp(pp):
        cnt = collections.Counter(T); fw = [w for w, c in cnt.items() if c >= 10]
        M = np.array([[collections.Counter(p)[w] for p in pp] for w in fw], float) if fw else np.zeros((1, 1))
        v = M.var(1); m = M.mean(1); ok = v > 0
        return np.mean(np.log(v[ok] / m[ok]))
    sizes = [len(p) for p in P]
    def cross():
        a = r.sample(T, len(T)); out, i = [], 0
        for s in sizes: out.append(a[i:i + s]); i += s
        return out
    s7 = disp(P) - np.mean([disp(cross()) for _ in range(3)])
    def local(match):
        hit, base, n = 0, 0, 0
        for pi, p in enumerate(P):
            for i in range(20, len(p)):
                w = p[i]; prev = p[i - 20:i]
                other = P[r.randrange(len(P))]
                while other is p and len(P) > 1: other = P[r.randrange(len(P))]
                rnd = [other[r.randrange(len(other))] for _ in range(20)]
                hit += any(match(w, x) for x in prev); base += any(match(w, x) for x in rnd); n += 1
        return (hit / n) / max(base / n, 1e-3)
    s8 = local(ed1); s9 = local(lambda a, b: a == b)
    rep = lambda pp: np.mean([p[i] == p[i - 1] for p in pp for i in range(1, len(p))])
    s10 = rep(P) / max(np.mean([rep(shuf_pages(P)) for _ in range(5)]), 1e-4)
    return dict(S1_h2=H2(T), S2_meanlen=L.mean(), S3_sdlen=L.std(), S4_zipf=zipf, S5_types=types, S6_orderMI=s6,
                S7_burst=s7, S8_nearcopy=s8, S9_localrep=s9, S10_immrep=s10)
