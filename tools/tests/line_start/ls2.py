"""Is the line-start rule a paragraph-capital habit? E1 and the p/t/y/s/f share for paragraph-initial lines vs other lines (raw IVTFF <%> marks), each vs within-line shuffle."""
import re, random, collections, math, numpy as np
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.')
def js(a, b):
    k = set(a) | set(b); na, nb = sum(a.values()), sum(b.values()); d = 0
    for x in k:
        p, q = a[x] / na, b[x] / nb; m = (p + q) / 2; d += (p * math.log2(p / m) if p else 0) + (q * math.log2(q / m) if q else 0)
    return d / 2
L = []
for line in open('./work/labels/ZL3b-n.txt', encoding='utf-8', errors='ignore'):
    m = re.match(r'<f\w+\.\d+,([@+=*])P\w*>\s+(.*)', line)
    if not m: continue
    t = m.group(2); par = t.startswith('<%>'); end = '<$>' in t
    t = re.sub(r'\[([^:\]]*):[^\]]*\]', r'\1', t); t = re.sub(r'<[^>]*>', '', t); t = re.sub(r'[{}]', '', t)
    w = [x for x in re.split(r'[.,]', t) if x and '?' not in x]
    if len(w) >= 3: L.append((w, 'par' if par else 'last' if end else 'mid'))
mid = collections.Counter(GL.findall(w)[0] for l, _ in L for w in l[1:-1])
r = random.Random(1); M = {'p', 't', 'y', 's', 'f', 'k'}
for kind in ('par', 'mid', 'last'):
    S = [l for l, k in L if k == kind]; fi = collections.Counter(GL.findall(l[0])[0] for l in S)
    sh = [js(collections.Counter(GL.findall(r.choice(l))[0] for l in S), mid) for _ in range(50)]
    share = {x: fi[x] / len(S) for x in ('p', 't', 'k', 'f', 'y', 's', 'q', 'o', 'ch', 'd')}
    print(f'{kind:5} n={len(S):5} E1 vs mid-line {js(fi, mid):.3f} (random word of same lines {np.mean(sh):.3f})  first-glyph shares: ' + ' '.join(f'{x} {v:.2f}' for x, v in share.items()))
print('mid-line first-glyph shares: ' + ' '.join(f'{x} {mid[x]/sum(mid.values()):.2f}' for x in ('p', 't', 'k', 'f', 'y', 's', 'q', 'o', 'ch', 'd')))
# Which mid-line opening does each line-initial opening (non-paragraph lines) stand in for? For X in y/s/d: share of line-initial X+rest words whose Y+rest is a common mid-line word, divided by the same share for mid-line X+rest words.
vocab = collections.Counter(w for l, _ in L for w in l[1:-1])
common = {w for w, c in vocab.items() if c >= 5}
for X in ('y', 's', 'd', 'o', 'q'):
    li = [w for l, k in L if k != 'par' for w in [l[0]] if GL.findall(w)[0] == X and len(GL.findall(w)) > 1]
    mi_ = [w for l, _ in L for w in l[1:-1] if GL.findall(w)[0] == X and len(GL.findall(w)) > 1]
    out = []
    for Y in ('', 'ch', 'sh', 'o', 'q', 'qo', 'd', 'y', 's', 'k', 't', 'l', 'a', 'e'):
        f = lambda ws: np.mean([(Y + ''.join(GL.findall(w)[1:])) in common for w in ws])
        a, b = f(li), f(mi_); out.append((a / max(b, 1e-3), Y, a, b))
    out.sort(reverse=True)
    print(f'line-initial {X}- (n={len(li)}): best stand-ins ' + ', '.join(f'{Y or "∅"} lift {lf:.2f} ({a:.2f} vs {b:.2f})' for lf, Y, a, b in out[:4]))
