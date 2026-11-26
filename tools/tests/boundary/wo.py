"""Where does the Voynich word order live? Decompose adjacent-word MI into edge coupling (last glyph of w_i x first glyph of w_i+1) vs the rest. TEST pages vs fitted Timm (3 seeds) vs within-line shuffle."""
import sys, json, re, random, math, collections, numpy as np
sys.path.insert(0, './work/timm_generator/code')
from common import VLINES, idx
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.'); g = lambda w: GL.findall(w) or ['?']
TI = idx(None, 'test'); TP = json.load(open('./work/decipherment_harness/timm_pages.json'))
def mi(pairs):
    N = len(pairs); pc = collections.Counter(pairs); a = collections.Counter(x for x, _ in pairs); b = collections.Counter(y for _, y in pairs)
    return sum(c / N * math.log2(c * N / (a[x] * b[y])) for (x, y), c in pc.items())
def feats(lines):
    P = [(l[i], l[i + 1]) for l in lines for i in range(len(l) - 1)]
    top = {w for w, _ in collections.Counter(w for l in lines for w in l).most_common(200)}
    W = lambda w: w if w in top else '~'
    return dict(edge=mi([(g(a)[-1], g(b)[0]) for a, b in P]), last2_first2=mi([(''.join(g(a)[-2:]), ''.join(g(b)[:2])) for a, b in P]),
                first_first=mi([(g(a)[0], g(b)[0]) for a, b in P]), last_last=mi([(g(a)[-1], g(b)[-1]) for a, b in P]), word200=mi([(W(a), W(b)) for a, b in P]))
r = random.Random(1)
def excess(lines, n=10):
    o = feats(lines); S = [feats([r.sample(l, len(l)) for l in lines]) for _ in range(n)]
    return {k: o[k] - np.mean([s[k] for s in S]) for k in o}
V = [l for i in TI for l in VLINES[i] if len(l) >= 2]
rows = {'Voynich TEST': excess(V)}
for s in TP: rows[f'Timm {s}'] = excess([l for i in TI for l in TP[s][i] if len(l) >= 2])
K = list(rows['Voynich TEST']); print('excess MI over within-line shuffle (bits)'); print(f'{"":14}' + ''.join(f'{k:>14}' for k in K))
for n, d in rows.items(): print(f'{n:14}' + ''.join(f'{d[k]:14.4f}' for k in K))
# which boundary pairs carry it? top over-represented last-glyph -> first-glyph pairs in Voynich
P = [(g(a)[-1], g(b)[0]) for l in V for a, b in zip(l, l[1:])]; c = collections.Counter(P); la = collections.Counter(x for x, _ in P); fb = collections.Counter(y for _, y in P); N = len(P)
lift = sorted(((c[k] * N / (la[k[0]] * fb[k[1]]), k, c[k]) for k in c if c[k] >= 40), reverse=True)
print('\nmost over-represented boundaries (last|first, lift, n):', ', '.join(f'{a}|{b} {l:.2f} ({n})' for l, (a, b), n in lift[:8]))
print('most under-represented:', ', '.join(f'{a}|{b} {l:.2f} ({n})' for l, (a, b), n in lift[-6:]))
# Robustness: only pairs where both words have >= 3 glyphs (removes split-word artefacts like 's aiin', 'o r')
def edge3(lines):
    P = [(g(a)[-1], g(b)[0]) for l in lines for a, b in zip(l, l[1:]) if len(g(a)) >= 3 and len(g(b)) >= 3]; return mi(P), len(P)
def ex3(lines, n=10):
    o, N = edge3(lines); return o - np.mean([edge3([r.sample(l, len(l)) for l in lines])[0] for _ in range(n)]), N
print('\nedge MI excess, both words >= 3 glyphs: Voynich %.4f (n=%d)' % ex3(V), ' | '.join('Timm %s %.4f' % (s, ex3([l for i in TI for l in TP[s][i] if len(l) >= 2])[0]) for s in TP))
# Currier A vs B separately
for L in 'AB':
    VL = [l for i in idx(L, 'test') for l in VLINES[i] if len(l) >= 2]; print(f'Currier {L}: edge excess {excess(VL)["edge"]:.4f}, >=3 glyphs {ex3(VL)[0]:.4f}')
