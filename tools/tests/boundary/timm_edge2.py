"""Exploratory: boundary rule applied while words are written. For each non-initial word of fitted Timm + line rule text, the scribe may swap the word's opening (first glyph, or an added/dropped initial q/o) for a variant seen in the FIT vocabulary. The choice is weighted by lift(prev last glyph, new first glyph)^beta x variant frequency. beta and the swap rate are fitted on FIT slots to match FIT edge MI and word order; scored on TEST slots."""
import sys, json, re, random, math, collections, numpy as np
src = open('./work/word_order/code/timm_edge.py').read().split("TP = json.load")[0]; exec(src)
VOC = collections.Counter(w for p in FIp for l in p for w in l)
byrest = collections.defaultdict(list)
for w, n in VOC.items():
    G = gg(w)
    for k in (1, 2):
        if len(G) > k: byrest[''.join(G[k:])].append((w, n))
    byrest[w].append((w, n))
def variants(w):
    G = gg(w); keys = {w, ''.join(G[1:])} | ({''.join(G[2:])} if len(G) > 2 else set()); out = {}
    for k in keys:
        for v, n in byrest.get(k, []): out[v] = n
    return out
def apply_rule(pages, beta, pr, rr):
    out = []
    for p in pages:
        q = []
        for l in p:
            nl = [l[0]] if l else []
            for w in l[1:]:
                if rr.random() < pr:
                    V = variants(w)
                    if V:
                        cand = list(V); wt = [lift(gg(nl[-1])[-1], gg(v)[0]) ** beta * V[v] ** 0.5 for v in cand]; w = rr.choices(cand, wt)[0]
                nl.append(w)
            q.append(nl)
        out.append(q)
    return out
TP = json.load(open('./work/decipherment_harness/timm_pages.json')); FI = idx(None, 'fit'); TI = idx(None, 'test')
et = edge(FIp); base = add_rule([TP['2001'][i] for i in FI]); rr = random.Random(5)
grid = [(abs(edge(apply_rule(base, b, pr, rr)) - et), b, pr) for b in (1, 2, 3) for pr in (0.3, 0.6, 0.9)]
best = min(grid); print(f'FIT edge target {et:.3f}; best beta {best[1]} rate {best[2]} (|diff| {best[0]:.3f})')
K = None
for s in TP:
    pages = apply_rule(add_rule([TP[s][i] for i in TI]), best[1], best[2], random.Random(int(s)))
    prof = profile(pages); K = K or list(prof[0]); m = {k: np.mean([d[k] for d in prof]) for k in K}; ok = {k: abs(m[k] - vm[k]) < 2 * vs[k] for k in K}
    print(f'Timm {s}+line+boundary ' + ' '.join(f'{k[:6]} {m[k]:.3f}{"*" if ok[k] else " "}' for k in K) + f'  matches {sum(ok.values())}/14  edge {edge(pages):.3f}')
print('Voynich TEST           ' + ' '.join(f'{k[:6]} {vm[k]:.3f} ' for k in K) + f'  edge {edge([VLINES[i] for i in TI]):.3f}')
