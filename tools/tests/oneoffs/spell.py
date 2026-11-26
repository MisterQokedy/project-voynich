import sys; sys.path.insert(0, './work/oneoffs/code')
from oo import *
import nouns_lib as NL
rng = random.Random(5)
U = lambda w: GL.findall(w)
def p1(w): return int(any(w[i:i+L] in w[i+L:] for L in (2, 3, 4) for i in range(len(w) - 2 * L + 1)))
def p2(w): u = U(w); return [a for a, b in zip(u, u[1:]) if a == b]
def mk(freq):
    F = set(freq); B = collections.defaultdict(list)
    for f in freq: B[len(f)].append(f)
    def p3(w): return int(any(w[:i] in F and w[i:] in F for i in range(2, len(w) - 1)))
    def near(x): return x in F or any(Levenshtein.distance(x, f) <= 1 for L in (len(x) - 1, len(x), len(x) + 1) for f in B.get(L, ()))
    def p3b(w): return int(any(near(w[:i]) and near(w[i:]) for i in range(3, len(w) - 2)))
    return p3, p3b
GALL = set('ktpf'); RG = set('pfmgx')
def feats(w, p3, p3b):
    u = U(w); g = sum(ch in GALL for ch in w)
    return dict(P1=p1(w), P2=int(bool(p2(w))), P3=p3(w), P3b=p3b(w), P5n=g, P5two=int(g >= 2))
def wmean(ws, fs, key, lens):
    t = W = 0
    for L, n in lens.items():
        v = [f[key] for w, f in zip(ws, fs) if len(w) == L]
        if v: t += n * np.mean(v); W += n
    return t / W
def wboot(ws, fs, key, lens, n=300):
    r = np.random.default_rng(0); idx = np.arange(len(ws)); out = []
    for _ in range(n):
        s = r.choice(idx, len(idx)); out.append(wmean([ws[i] for i in s], [fs[i] for i in s], key, lens))
    return np.percentile(out, [2.5, 97.5])
P = parse(V + 'transcriptions/ZL3b-n.txt'); rows, c, freq = classify(P)
fr = [r['word'] for r in rows if r['cls'] == 'FREE' and 6 <= len(r['word']) <= 11]; lens = collections.Counter(len(w) for w in fr)
e2 = [r['word'] for r in rows if r['cls'] == 'EDIT2']
def shuf(w): u = U(w); rng.shuffle(u); return ''.join(u)
sh = [shuf(w) for w in fr]
p3, p3b = mk(freq)
G = {'real FREE': (fr, p3, p3b), 'real EDIT2': (e2, p3, p3b), 'unit-shuffled FREE': (sh, p3, p3b)}
gw = []
for s in range(900, 905):
    gp = gen_pages(s); gr, gc, gf = classify(gp); q3, q3b = mk(gf)
    gw += [(r['word'], q3, q3b) for r in gr if r['cls'] == 'FREE']
out = {}
KEYS = ['P1', 'P2', 'P3', 'P3b', 'P5n', 'P5two']
for nm, (ws, a, b) in G.items():
    fs = [feats(w, a, b) for w in ws]; out[nm] = (ws, fs)
out['GEN FREE'] = ([w for w, _, _ in gw], [feats(w, a, b) for w, a, b in gw])
# German
de = []
for pat in NL.WORKS:
    Pd = NL.fixfirst(NL.load_work(pat)); N = sum(len(p['toks']) for p in Pd); rd, cd, fd = NL.classify_n(Pd, N); d3, d3b = mk(fd)
    de += [(r['word'], d3, d3b) for r in rd if r['cls'] == 'FREE']
dl = collections.Counter(len(w) for w, _, _ in de)
out['German FREE (own lengths)'] = ([w for w, _, _ in de], [feats(w, a, b) for w, a, b in de])
print('Length-weighted to real FREE lengths 6-11 (German: unweighted, own lengths, mean %.1f chars)' % np.mean([len(w) for w, _, _ in de]))
print('%-26s %6s ' % ('group', 'n') + ' '.join('%-19s' % k for k in KEYS))
for nm, (ws, fs) in out.items():
    if nm.startswith('German'):
        vals = [(np.mean([f[k] for f in fs]), np.nan, np.nan) for k in KEYS]
    else:
        vals = [(wmean(ws, fs, k, lens), *wboot(ws, fs, k, lens)) for k in KEYS]
    print('%-26s %6d ' % (nm, len(ws)) + ' '.join('%-19s' % ('%.3f [%.2f,%.2f]' % v) for v in vals))
# P2 which doubles
for nm in ('real FREE', 'real EDIT2', 'GEN FREE'):
    ws = out[nm][0]; cc = collections.Counter(d for w in ws for d in p2(w)); n = len(ws)
    print('doubles per 100 words, %s:' % nm, {k: round(100 * v / n, 1) for k, v in cc.most_common(8)})
# P4 rare glyph position
def pos(ws):
    cc = collections.Counter()
    for w in ws:
        u = U(w)
        for i, x in enumerate(u):
            for ch in RG:
                if ch in x: cc[(ch, 'first' if i == 0 else ('last' if i == len(u) - 1 else 'inside'))] += 1
    return cc
alltok = [t[0] for p in P for t in p['toks']]
for nm, ws in (('real FREE', fr), ('real EDIT2', e2), ('all tokens', alltok), ('GEN FREE', out['GEN FREE'][0])):
    cc = pos(ws)
    print('rare-glyph position, %-10s ' % nm + '  '.join('%s: first %.2f inside %.2f (n %d)' % (ch, cc[(ch, 'first')] / max(1, sum(cc[(ch, x)] for x in ('first', 'inside', 'last'))), cc[(ch, 'inside')] / max(1, sum(cc[(ch, x)] for x in ('first', 'inside', 'last'))), sum(cc[(ch, x)] for x in ('first', 'inside', 'last'))) for ch in 'pfmg'))
# P6 bigram enrichment
def bg(ws):
    cc = collections.Counter(); 
    for w in ws:
        u = ['^'] + U(w) + ['$']; cc.update(zip(u, u[1:]))
    n = sum(cc.values()); return {k: v / n for k, v in cc.items()}
A, T, Gf = bg(fr), bg(alltok), bg(out['GEN FREE'][0])
en = sorted([k for k in A if A[k] * len(fr) * 9 >= 30], key=lambda k: -A[k] / T.get(k, 1e-6))[:12]
print('\nmost over-represented glyph pairs in real FREE (ratio to all tokens | GEN FREE ratio to its own...):')
print('  ' + '  '.join('%s%s %.1fx (GEN %.1fx)' % (a, b, A[(a, b)] / T.get((a, b), 1e-6), Gf.get((a, b), 0) / T.get((a, b), 1e-6)) for a, b in en))
