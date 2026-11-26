"""P3: paint offset ("ghost" transfer) between faces in contact.
Facing faces touch at the same leaf-frame position (verso mirrored). For each face pair (A,B):
offset score = corr(strong paint of A, faint green of B) on cells where B has no strong paint of its own, averaged both ways.
Contact in current binding: Xv faces next leaf's recto. Contact as a lone folded sheet (singulion): Xv faces Yr."""
import sys, re
import numpy as np
from scipy.ndimage import gaussian_filter, binary_dilation
sys.path.insert(0, 'code'); from seg import segment; from vlib import load, structure
rng = np.random.default_rng(9)
P = load(); sheets, leafq = structure(P)
lab = [l.rstrip('\n').split('\t') for l in open('canvases.tsv')]
GX, GY = 40, 54
M = {}
for i, l in enumerate(lab):
    m = re.fullmatch(r'(\d+)([rv])', l[1])
    if not m: continue
    side = m.group(2)
    (x0, y0, x1, y1), a = segment('small/%03d.jpg' % i, side)
    w, h = x1 - x0, y1 - y0
    s = a[y0 + int(.02*h):y1 - int(.02*h), x0 + int(.02*w):x1 - int(.02*w)]
    if side == 'v': s = s[:, ::-1]
    R, G, B = s[..., 0], s[..., 1], s[..., 2]
    mx = s.max(2); mn = s.min(2); sat = (mx - mn) / (mx + 1)
    strong = ((G > R + 4) | (B > R + 4)) & (sat > .18)
    faint = (G >= R - 6) & (sat > .04) & (sat <= .18) & ~strong   # pale greenish-grey, parchment is yellow-brown (R>G)
    def grid(mk):
        ys = np.array_split(np.arange(mk.shape[0]), GY); xs = np.array_split(np.arange(mk.shape[1]), GX)
        return np.array([[mk[np.ix_(yy, xx)].mean() for xx in xs] for yy in ys])
    M[l[1]] = (gaussian_filter(grid(strong), 1), gaussian_filter(grid(faint), 1), grid(strong))
def off(a, b):
    sa, fa, ra = M[a]; sb, fb, rb = M[b]
    vals = []
    for (s1, f2, r2) in [(sa, fb, rb), (sb, fa, ra)]:
        ok = ~binary_dilation(r2 > .05, iterations=2)
        if s1[ok].sum() < .5 or ok.sum() < 200: continue
        if f2[ok].std() > 0: vals.append(np.corrcoef(s1[ok], f2[ok])[0, 1])
    return np.mean(vals) if vals else None
facing, inner, central = [], [], []
for (q, b), LL in sheets.items():
    if len(LL) != 2: continue
    X, Y = LL
    if '%dv' % X in M and '%dr' % Y in M: (central if Y == X + 1 else inner).append(('%dv' % X, '%dr' % Y))
pages = sorted(M, key=lambda p: (int(p[:-1]), p[-1]))
for a, b in zip(pages, pages[1:]):
    if a[-1] == 'v' and b[-1] == 'r' and int(b[:-1]) == int(a[:-1]) + 1 and leafq.get(int(a[:-1]), (0, 0))[:2] != leafq.get(int(b[:-1]), (1, 1))[:2]:
        facing.append((a, b))
vs = [p for p in M if p[-1] == 'v']; rs = [p for p in M if p[-1] == 'r']
rand = []
for _ in range(60000):
    v, r = rng.choice(vs), rng.choice(rs)
    if leafq.get(int(v[:-1]),('?',))[0] != leafq.get(int(r[:-1]),('!',))[0]: continue
    if int(r[:-1]) not in (int(v[:-1]) + 1,): 
        o = off(v, r)
        if o is not None: rand.append(o)
rand = np.array(rand)
print(f'random SAME-QUIRE verso|recto (no contact) n={len(rand)} mean offset score {rand.mean():+.4f}')
for name, prs in [('binding facing (in contact now)', facing), ('central sheet (contact in both)', central), ('inner conjoint Xv|Yr (contact only as lone folded sheet)', inner)]:
    sc = [(p, off(*p)) for p in prs]; sc = [(p, s) for p, s in sc if s is not None]
    v = np.array([s for _, s in sc])
    null = np.array([rng.choice(rand, len(v)).mean() for _ in range(20000)])
    print(f'{name:58s} n={len(v):2d} mean {v.mean():+.4f}  p={(1+np.sum(null>=v.mean()))/20001:.4f}   top: ' + ', '.join(f'{a}|{b} {s:+.2f}' for (a, b), s in sorted(sc, key=lambda t: -t[1])[:6]))
