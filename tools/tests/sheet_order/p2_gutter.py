"""P2: does painted/drawn content continue across the gutter? Compare inner conjoint spreads (Xv|Yr),
current binding spreads, and random verso|recto pairs from the same section."""
import sys, re, itertools
from collections import defaultdict
import numpy as np
from PIL import Image
sys.path.insert(0, 'code'); from seg import segment; from vlib import load, structure
rng = np.random.default_rng(4)
P = load(); sheets, leafq = structure(P); pg = {p['page']: p for p in P}
lab = [l.rstrip('\n').split('\t') for l in open('canvases.tsv')]
NB = 48
THR = float(sys.argv[1])
prof = {}
for i, l in enumerate(lab):
    m = re.fullmatch(r'(\d+)([rv])', l[1])
    if not m: continue
    side = m.group(2)
    (x0, y0, x1, y1), a = segment('small/%03d.jpg' % i, side)
    w = x1 - x0
    # gutter strip: 3%..14% of bbox width from gutter side (skip flyleaf/fold shadow)
    if side == 'r': sx = slice(x0 + int(.03 * w), x0 + int(.14 * w))
    else: sx = slice(x1 - int(.14 * w), x1 - int(.03 * w))
    s = a[y0:y1, sx]
    mx = s.max(2); mn = s.min(2); sat = (mx - mn) / (mx + 1)
    R, G, B = s[..., 0], s[..., 1], s[..., 2]
    green = (G > R + 4) & (sat > .18)            # green/blue paint (parchment is never G>R)
    blue = (B > R + 4) & (sat > .12)
    red = (R > G + 50) & (sat > .45)
    ink = mx < 110
    feats = {}
    for name, mk in [('paint', green | blue | red), ('ink', ink)]:
        rows = np.array_split(mk, NB, axis=0); feats[name] = np.array([r.mean() for r in rows])
    prof[l[1]] = feats
def score(v, r, f):
    a, b = prof[v][f], prof[r][f]
    if a.sum() < THR or b.sum() < THR or a.std() == 0 or b.std() == 0: return None
    return np.corrcoef(a, b)[0, 1]
def sec(p): return pg[p].get('I') if p in pg else None
inner, central, facing = [], [], []
for (q, b), LL in sheets.items():
    if len(LL) != 2: continue
    X, Y = LL; pair = ('%dv' % X, '%dr' % Y)
    if pair[0] in prof and pair[1] in prof: (central if Y == X + 1 else inner).append(pair)
order = sorted(prof, key=lambda p: (int(p[:-1]), p[-1]))
for a, b in zip(order, order[1:]):
    if a.endswith('v') and b.endswith('r') and int(b[:-1]) == int(a[:-1]) + 1:
        LA, LB = int(a[:-1]), int(b[:-1])
        if (leafq.get(LA, (0, 0))[:2] != leafq.get(LB, (1, 1))[:2]): facing.append((a, b))
vs = [p for p in prof if p.endswith('v')]; rs = [p for p in prof if p.endswith('r')]
for f in ['paint', 'ink']:
    print(f'== feature: {f} (row-profile correlation across gutter; pairs where both strips have some {f})')
    allrand = [score(v, r, f) for v in vs for r in rs if int(r[:-1]) != int(v[:-1]) + 1 and leafq.get(int(v[:-1]),('?',))[0]==leafq.get(int(r[:-1]),('!',))[0]]
    allrand = np.array([x for x in allrand if x is not None])
    for name, prs in [('inner conjoint (Xv|Yr, not facing now)', inner), ('central sheet (conjoint AND facing)', central), ('binding facing, different sheets', facing)]:
        sc = [(p, score(*p, f)) for p in prs]; sc = [(p, s) for p, s in sc if s is not None]
        if not sc: print('  ', name, 'n=0'); continue
        vals = np.array([s for _, s in sc])
        null = np.array([rng.choice(allrand, len(vals)).mean() for _ in range(10000)])
        print(f'  {name:42s} n={len(vals):2d} mean r={vals.mean():+.3f}  random v|r null {null.mean():+.3f}  p={(1+np.sum(null>=vals.mean()))/10001:.4f}')
        if f == 'paint':
            top = sorted(sc, key=lambda t: -t[1])[:6]
            print('     top:', ', '.join(f'{a}|{b} {s:+.2f}' for (a, b), s in top))
