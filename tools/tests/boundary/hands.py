"""Is the boundary rule shared by all scribes? Boundary log-lift matrices (last glyph x next first glyph, top glyphs) per Davis hand; correlation between hands vs split-half within a hand."""
import json, re, random, math, collections, numpy as np
D = json.load(open('./work/manuscript_wide/pages2.json'))
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.'); g = lambda w: GL.findall(w) or ['?']
def pairs(pages): return [(g(a)[-1], g(b)[0]) for p in pages for L in p['lines'] if L['u'] != 'L' for a, b in zip(L['w'], L['w'][1:])]
LAST = ['y', 'n', 'l', 'r', 's', 'o', 'm', 'd']; FIRST = ['q', 'o', 'ch', 'd', 's', 'sh', 'k', 't', 'a', 'y', 'l', 'p', 'r', 'c']
def mat(P):
    c = collections.Counter(P); a = collections.Counter(x for x, _ in P); b = collections.Counter(y for _, y in P); N = len(P)
    return np.array([[math.log((c[(x, y)] + 1) * N / ((a[x] + 1) * (b[y] + 1))) for y in FIRST] for x in LAST]).ravel()
H = collections.defaultdict(list)
for p in D: H[p.get('H')].append(p)
hands = [h for h in H if h and len(pairs(H[h])) >= 1500]; r = random.Random(1)
print('hands with >=1500 boundary pairs:', {h: len(pairs(H[h])) for h in hands})
M = {h: mat(pairs(H[h])) for h in hands}
print('\nbetween-hand correlation of boundary log-lift matrices:')
for i, a in enumerate(hands):
    print('  ' + a + ': ' + ' '.join(f'{b}:{np.corrcoef(M[a], M[b])[0,1]:.2f}' for b in hands[i + 1:]))
print('\nwithin-hand split-half (pages split at random, 20 draws):')
for h in hands:
    rs = []
    for _ in range(20):
        P = H[h][:]; r.shuffle(P); k = len(P) // 2; rs.append(np.corrcoef(mat(pairs(P[:k])), mat(pairs(P[k:])))[0, 1])
    print(f'  hand {h}: {np.mean(rs):.2f}')
# null: matrix from within-line shuffled text of a hand correlated with real
for h in hands[:2]:
    sh = [(g(x)[-1], g(y)[0]) for p in H[h] for L in p['lines'] if L['u'] != 'L' for l in [r.sample(L['w'], len(L['w']))] for x, y in zip(l, l[1:])]
    print(f'  null (hand {h} real vs its shuffle): {np.corrcoef(M[h], mat(sh))[0,1]:.2f}')
