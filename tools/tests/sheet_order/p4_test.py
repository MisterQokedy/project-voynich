import sys, json
import numpy as np
sys.path.insert(0, 'code'); from vlib import load, structure
rng = np.random.default_rng(8)
F = json.load(open('p4_feat.json')); P = load(); sheets, leafq = structure(P)
rows = []
for (q, b), LL in sheets.items():
    if len(LL) != 2: continue
    X, Y = LL; k = ['%dr' % X, '%dv' % X, '%dr' % Y, '%dv' % Y]
    if all(F.get(p) for p in k): rows.append((q, b, X, Y, k))
for feat in ['spots', 'tex', 'yellow']:
    dX = np.array([F[k[0]][feat] - F[k[1]][feat] for *_, k in rows]); dY = np.array([F[k[3]][feat] - F[k[2]][feat] for *_, k in rows])
    r = np.corrcoef(dX, dY)[0, 1]; null = [np.corrcoef(dX, rng.permutation(dY))[0, 1] for _ in range(10000)]
    agree = np.mean(np.sign(dX) == np.sign(dY))
    print(f'{feat:6s} sheets={len(rows)} corr(Xr-Xv, Yv-Yr)={r:+.3f} p={(1+np.sum(np.array(null)>=r))/10001:.4f} sign agreement {agree:.0%}')
# combined skin score per sheet: outer-face minus inner-face (z-scored spots + yellow)
# sheet orientation: outer faces (Xr,Yv) grainier than inner faces?  o = +1 means grainy (hair?) side out
orient = {}
for q, b, X, Y, k in rows:
    s = (F[k[0]]['spots'] + F[k[3]]['spots']) - (F[k[1]]['spots'] + F[k[2]]['spots'])
    dX = F[k[0]]['spots'] - F[k[1]]['spots']; dY = F[k[3]]['spots'] - F[k[2]]['spots']
    if np.sign(dX) == np.sign(dY): orient[(q, int(b))] = int(np.sign(s))
print('classified sheets', len(orient), 'grainy side out:', sum(v > 0 for v in orient.values()))
# Gregory: adjacent nested sheets (b, b+1) in same quire alternate
pairs = [(orient[(q, b)], orient[(q, b + 1)]) for (q, b) in orient if (q, b + 1) in orient]
alt = sum(a != c for a, c in pairs)
# null: shuffle orientations within quire
byq = {}
for (q, b), o in orient.items(): byq.setdefault(q, []).append(b)
nulls = []
for _ in range(10000):
    sh = {}
    for q, bs in byq.items():
        vals = rng.permutation([orient[(q, b)] for b in bs]); sh.update({(q, b): v for b, v in zip(bs, vals)})
    nulls.append(sum(sh[(q, b)] != sh[(q, b + 1)] for (q, b) in sh if (q, b + 1) in sh))
print(f'Gregory: {alt}/{len(pairs)} adjacent nested pairs alternate; within-quire shuffle null {np.mean(nulls):.1f}, p={(1+np.sum(np.array(nulls)>=alt))/10001:.3f}')
print({q: ''.join('O' if orient[(q, b)] > 0 else 'I' for b in sorted(bs)) for q, bs in byq.items()})
