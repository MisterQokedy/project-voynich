"""Profile of every meaningful text in the Gaskell & Bowern set: boundary coupling, ending agreement, word-identity order (excess over within-line shuffle, 9-word lines, first 15k tokens). Distance to the Voynich TEST profile."""
import sys, json, random, re, math, collections, glob, unicodedata, numpy as np
exec(open('./work/word_order/code/wo.py').read().split("V = [l for i in TI")[0])
X = '/tmp/claude-0/-home-user/18d6effa-14be-52f6-88bb-dce5a4bed879/scratchpad/ext'
def tok(t):
    t = unicodedata.normalize('NFKD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c)); return re.findall(r'[^\W\d_]+', t)
V = [l for i in TI for l in VLINES[i] if len(l) >= 2]; ev = excess(V, 5)
rows = []
for f in sorted(glob.glob(X + '/mean/texts/*.txt')):
    T = tok(open(f, encoding='utf-8', errors='ignore').read())[:15000]
    if len(T) < 3000: continue
    g = lambda w: list(w) or ['?']; globals()['g'] = g
    e = excess([T[i:i + 9] for i in range(0, len(T), 9)], 5); rows.append((f.split('/')[-1][:-4], e))
globals()['g'] = lambda w: GL.findall(w) or ['?']
K = ['edge', 'last_last', 'word200']
d = lambda e: math.sqrt(sum(((e[k] - ev[k]) / max(ev[k], 0.02)) ** 2 for k in K))
print('Voynich TEST  ' + '  '.join(f'{k} {ev[k]:.3f}' for k in K))
for n, e in sorted(rows, key=lambda x: d(x[1])): print(f'{d(e):6.2f}  {n[:55]:55} ' + '  '.join(f'{k} {e[k]:.3f}' for k in K))
