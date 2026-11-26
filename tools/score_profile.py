"""Score any generated text against the Voynich 24-statistic target profile.
Usage: python3 score.py pages.json   (a list of pages, each a list of lines, each a list of EVA words, laid out in the 202 manuscript slots; TEST slots are scored)
Without an argument, it prints the Voynich FIT and TEST reference values."""
import sys, json, numpy as np
ARG = sys.argv[1:]
exec(open('./work/glyph_ngram/code/ng.py').read().split("def train(")[0])
VT = [VLINES[i] for i in TI]
V1 = cstats(VT); ch1 = [cstats(c) for c in chunks5(VT)]; sd1 = {x: max(np.std([c[x] for c in ch1]), 0.1 * abs(V1[x])) for x in V1}
V2 = c2(VT); ch2 = [c2(c) for c in chunks5(VT)]; sd2 = {x: max(np.std([c[x] for c in ch2]), 0.1 * abs(V2[x])) for x in V2}
def full(pages):
    pr = profile(pages); m = {x: np.mean([d[x] for d in pr]) for x in vm}; return {**m, **cstats(pages), **c2(pages)}
REF = {**vm, **V1, **V2}; SD = {**vs, **sd1, **sd2}
if not ARG:
    F = full(FIp)
    print('| Statistic | Voynich TEST | 2-sd band | Voynich FIT |\n|---|---|---|---|')
    for k in REF: print(f'| {k} | {REF[k]:.4f} | ±{2*SD[k]:.4f} | {F[k]:.4f} |')
else:
    P = json.load(open(ARG[0])); g = full([P[i] for i in TI]); n = 0
    for k in REF:
        ok = abs(g[k] - REF[k]) < 2 * SD[k]; n += ok; print(f'{k:12} {g[k]:9.4f}  target {REF[k]:9.4f} ±{2*SD[k]:.4f}  {"ok" if ok else "MISS"}')
    print(f'matches {n}/{len(REF)}')
