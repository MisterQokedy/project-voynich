"""Is the boundary coupling a transcription artefact of uncertain spaces? Raw ZL3b-n: '.' = certain space, ',' = uncertain space. Boundary MI excess (vs within-line shuffle of words keeping separator types fixed) for certain vs uncertain separators."""
import re, random, math, collections, numpy as np
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.'); g = lambda w: GL.findall(w) or ['?']
def mi(P):
    N = len(P); pc = collections.Counter(P); a = collections.Counter(x for x, _ in P); b = collections.Counter(y for _, y in P)
    return sum(c / N * math.log2(c * N / (a[x] * b[y])) for (x, y), c in pc.items())
lines = []
for line in open('./work/labels/ZL3b-n.txt', encoding='utf-8', errors='ignore'):
    m = re.match(r'<f\w+\.\d+,[@+=*]P\w*>\s+(.*)', line)
    if not m: continue
    t = m.group(1); t = re.sub(r'\[([^:\]]*):[^\]]*\]', r'\1', t); t = re.sub(r'<[^>]*>', '', t); t = re.sub(r'[{}]', '', t)
    toks = re.split(r'([.,])', t); words = toks[0::2]; seps = toks[1::2]
    if any('?' in w or not w for w in words): continue
    lines.append((words, seps))
r = random.Random(1)
def pairs(L, kind):
    return [(g(w[i])[-1], g(w[i + 1])[0]) for w, s in L for i in range(len(s)) if s[i] == kind]
def shuf(L): return [(r.sample(w, len(w)), s) for w, s in L]
for kind, name in (('.', 'certain space'), (',', 'uncertain space')):
    o = mi(pairs(lines, kind)); n = len(pairs(lines, kind)); sh = np.mean([mi(pairs(shuf(lines), kind)) for _ in range(10)])
    print(f'{name:16} n={n:6}  boundary MI {o:.3f}  shuffle {sh:.3f}  excess {o - sh:.3f}')
