"""Boundary coupling relative to within-word glyph coupling: MI(last glyph, next word's first glyph) / MI(adjacent glyphs inside words), both as excess over a shuffle that keeps the units."""
import sys, json, random, re, math, collections, glob, numpy as np
exec(open('./work/word_order/code/wo.py').read().split("V = [l for i in TI")[0])
gv = g
def within(lines, gf):
    P = [(G[i], G[i + 1]) for l in lines for w in l for G in [gf(w)] for i in range(len(G) - 1)]
    # null: shuffle glyphs inside each word
    S = [mi([(G[i], G[i + 1]) for l in lines for w in l for G in [r.sample(gf(w), len(gf(w)))] for i in range(len(G) - 1)]) for _ in range(5)]
    return mi(P) - np.mean(S)
def boundary(lines, gf):
    o = mi([(gf(a)[-1], gf(b)[0]) for l in lines for a, b in zip(l, l[1:])])
    S = [mi([(gf(a)[-1], gf(b)[0]) for l in lines for a, b in zip(*[r.sample(l, len(l))] * 2)]) for _ in range(5)]
    S = [mi([(gf(a)[-1], gf(b)[0]) for l in (r.sample(x, len(x)) for x in lines) for a, b in zip(l, l[1:])]) for _ in range(5)]
    return o - np.mean(S)
rows = {}
V = [l for i in TI for l in VLINES[i] if len(l) >= 2]; rows['Voynich TEST'] = (within(V, gv), boundary(V, gv))
for s in TP: rows[f'Timm {s}'] = (lambda L: (within(L, gv), boundary(L, gv)))([l for i in TI for l in TP[s][i] if len(l) >= 2])
X = '/tmp/claude-0/-home-user/18d6effa-14be-52f6-88bb-dce5a4bed879/scratchpad/ext'
nb = open(X + '/naibbe/encrypted/nathist_output_ciphertext.txt').read().split(); NBL = [nb[i:i + 9] for i in range(0, 30000, 9)]
rows['Naibbe Latin'] = (within(NBL, gv), boundary(NBL, gv))
C = json.load(open('./work/decipherment_harness/corpora.json')); tok = lambda t: re.findall(r'[a-z]+', t.lower()); gl = lambda w: list(w) or ['?']
Ls = {k: C[k][:20000] for k in ('latin', 'italian', 'english')}; Ls['german_herb'] = tok(open(X + '/mean/texts/Historical - German - Technical - German Herbarium.txt', encoding='utf-8', errors='ignore').read())[:20000]
for k, T in Ls.items():
    lines = [T[i:i + 9] for i in range(0, len(T), 9)]; rows[k] = (within(lines, gl), boundary(lines, gl))
    # respaced control: remove spaces, re-cut into tokens of Voynich-like lengths at random
    s = ''.join(T); lens = [len(w) for l in V for w in l]; toks, i = [], 0
    while i < len(s): n = r.choice(lens); toks.append(s[i:i + n]); i += n
    RL = [toks[j:j + 9] for j in range(0, len(toks), 9)]; rows[k + ' respaced'] = (within(RL, gl), boundary(RL, gl))
G = []
for f in sorted(glob.glob(X + '/gib/*.txt')): G += [tok(l) for l in open(f, encoding='utf-8', errors='ignore') if len(tok(l)) >= 2]
rows['gibberish'] = (within(G, gl), boundary(G, gl))
print(f'{"":22}{"within-word":>12}{"boundary":>10}{"ratio":>8}')
for n, (a, b) in rows.items(): print(f'{n:22}{a:12.3f}{b:10.3f}{b / a:8.2f}')
