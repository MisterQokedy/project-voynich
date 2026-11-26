"""Exploratory: add a boundary rule to fitted Timm + line rule. Within each line, words are re-ordered greedily so that P(first glyph | previous last glyph) follows the FIT-page boundary model with strength beta (fitted on FIT slots to match FIT edge MI). Scored on TEST slots with the 14-statistic fingerprint."""
import sys, json, re, random, math, collections, numpy as np
sys.argv = ['x']; exec(open('./work/naibbe_test/code/nb.py').read().split("tok = open(X")[0])
GLs = re.compile(r'cth|ckh|cph|cfh|ch|sh|.'); gg = lambda w: GLs.findall(w) or ['?']
FIp = [VLINES[i] for i in idx(None, 'fit')]
P = [(gg(a)[-1], gg(b)[0]) for p in FIp for l in p for a, b in zip(l, l[1:])]; c = collections.Counter(P); la = collections.Counter(x for x, _ in P); fb = collections.Counter(y for _, y in P); N = len(P)
lift = lambda a, b: (c[(a, b)] + 1) * N / ((la[a] + 1) * (fb[b] + 1))
def reorder(pages, beta, rr):
    out = []
    for p in pages:
        q = []
        for l in p:
            if len(l) < 3: q.append(l); continue
            rest = l[1:]; o = [l[0]]
            while rest:
                w = [lift(gg(o[-1])[-1], gg(x)[0]) ** beta for x in rest]; k = rr.choices(range(len(rest)), w)[0]; o.append(rest.pop(k))
            q.append(o)
        out.append(q)
    return out
def edge(pages):
    PP = [(gg(a)[-1], gg(b)[0]) for p in pages for l in p for a, b in zip(l, l[1:])]; n = len(PP)
    pc = collections.Counter(PP); A = collections.Counter(x for x, _ in PP); B = collections.Counter(y for _, y in PP)
    return sum(v / n * math.log2(v * n / (A[x] * B[y])) for (x, y), v in pc.items())
TP = json.load(open('./work/decipherment_harness/timm_pages.json')); FI = idx(None, 'fit'); TI = idx(None, 'test')
etarget = edge(FIp); rr = random.Random(3)
base = add_rule([TP['2001'][i] for i in FI]); best = min((abs(edge(reorder(base, b, rr)) - etarget), b) for b in (0.5, 1, 1.5, 2, 3, 4))
print(f'FIT edge MI target {etarget:.3f}; beta chosen {best[1]} (|diff| {best[0]:.3f})')
K = None
for s in TP:
    pages = reorder(add_rule([TP[s][i] for i in TI]), best[1], random.Random(int(s)))
    prof = profile(pages); K = K or list(prof[0]); m = {k: np.mean([d[k] for d in prof]) for k in K}; ok = {k: abs(m[k] - vm[k]) < 2 * vs[k] for k in K}
    print(f'Timm {s} + line + edge  ' + ' '.join(f'{k[:6]} {m[k]:.3f}{"*" if ok[k] else " "}' for k in K) + f'  matches {sum(ok.values())}/14')
print('Voynich TEST            ' + ' '.join(f'{k[:6]} {vm[k]:.3f} ' for k in K))
