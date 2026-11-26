"""Per-letter features from GS masks, in the glyphs.json / hog.npy format of P3 / H10f (glyphfeat.py), in window coordinates (U = 20 px).
python -I gsfeat.py <data dir> <masks.npy> <voynich-letters repo> <zl_parastart.json> <out dir> [clip]
clip = 'clip': mask columns beyond the centre of the previous / next same-line letter box are cleared (P3-c)."""
import csv, json, sys
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.feature import hog
from skimage.morphology import skeletonize
from skimage.transform import resize
D, MM, REPO, PS, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), json.load(open(sys.argv[4])), Path(sys.argv[5])
CLIP = len(sys.argv) > 6 and sys.argv[6] == 'clip'
OUT.mkdir(parents=True, exist_ok=True)
wins = np.load(D / 'wins.npy', mmap_mode='r'); meta = json.load(open(D / 'meta.json'))
masks = np.load(MM, mmap_mode='r'); pos = {i: k for k, i in enumerate(json.load(open(MM.replace('.npy', '_idx.json'))))}
H, W, U = 96, 64, 20.0
COMP = [("cth", "T"), ("ckh", "K"), ("cph", "P"), ("cfh", "F"), ("ch", "C"), ("sh", "S")]
DEC = {b: a for a, b in COMP}
enc = lambda s: [s := s.replace(a, b) for a, b in COMP][-1]
LINES = {r['file'][:-4]: r for r in csv.DictReader(open(REPO / 'data/lines/lines.csv'))}
NL = defaultdict(int)
for r in csv.DictReader(open(REPO / 'data/letters/letters.csv')): NL[r['line']] += 1
BY = {(m['line'], m['letter']): m for m in meta}
HOG_SHAPE = (56, 24)
np.random.seed(5)


def otsu(v):
    h, e = np.histogram(v, 128); c = (e[:-1] + e[1:]) / 2; w = np.cumsum(h); m = np.cumsum(h * c); wb = w[-1] - w; mb = m[-1] - m
    ok = (w > 0) & (wb > 0); var = np.where(ok, w * wb * ((m / np.maximum(w, 1)) - (mb / np.maximum(wb, 1))) ** 2, 0)
    return c[np.argmax(var)]


def feats(m):
    M = masks[pos[m['i']]].astype(bool).copy(); g = wins[m['i']].astype(float)
    x0, y0, x1, y1 = m['box']; cx = (x0 + x1) / 2; bt, bb = m['bt'], m['bb']
    if CLIP:
        same = [o for o in m['others'] if o[4] and abs((o[1] + o[3]) / 2 - (y0 + y1) / 2) < U]
        L = [o for o in same if (o[0] + o[2]) / 2 < cx]; R = [o for o in same if (o[0] + o[2]) / 2 > cx]
        if L: c = int(round(max((o[0] + o[2]) / 2 for o in L))); M[:, :max(0, min(W, c + 1))] = False
        if R: c = int(round(min((o[0] + o[2]) / 2 for o in R))); M[:, max(0, min(W, c)):] = False
    if M.sum() < 10: return None
    paper = np.percentile(g, 90); ink = paper - g; pv = ink[ink > 5]; thr = max(otsu(pv) if pv.size > 30 else 30, 25); B = ink > thr
    bsl = (slice(int(max(0, y0)), int(max(0, y1)) + 1), slice(int(max(0, x0)), int(max(0, x1)) + 1))
    complete = float((M[bsl] & B[bsl]).sum() / max(B[bsl].sum(), 1))
    ys, xs = np.nonzero(M); lab, ncomp = ndimage.label(M, structure=np.ones((3, 3)))
    area = M.sum(); sk = skeletonize(M).sum()
    top, bot, left, right = ys.min(), ys.max(), xs.min(), xs.max()
    f = dict(top_ext=(bt - top) / U, bot_ext=(bot - bb) / U, left_ext=(cx - left) / U, right_ext=(right - cx) / U,
             height=(bot - top + 1) / U, width=(right - left + 1) / U, aspect=(bot - top + 1) / (right - left + 1),
             dx=(xs.mean() - cx) / U, dy=(ys.mean() - (bt + bb) / 2) / U, area=area / U ** 2, ncomp=int(ncomp),
             thick=area / max(sk, 1) / U, clipL=int(left == 0), clipR=int(right == W - 1),
             tone=float(paper - np.median(g[M])), box_w=(x1 - x0) / U, box_h=(y1 - y0) / U,
             box_dy=((y0 + y1) / 2 - (bt + bb) / 2) / U, box_top=(bt - y0) / U, touch_top=int(top == 0), complete=complete)
    r0, r1 = int(bt - 0.25 * U), int(bt + 0.35 * U); best = 0
    for row in M[max(0, r0):max(0, r1)]:
        if row.any():
            d = np.diff(np.concatenate([[0], row.astype(int), [0]])); s, e = np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]
            best = max(best, int((e - s).max()))
    f['crossbar'] = best / U
    mid = int((bt + bb) / 2); up = xs[ys < mid]
    f['tail_right'] = (up.max() - cx) / U if up.size else 0.0
    f['tail_w'] = (up.max() - xs.min() + 1) / U if up.size else 0.0
    mx, my = xs.mean(), ys.mean()
    a0, a1 = int(mx - 0.75 * U), int(mx + 0.75 * U); b0, b1 = int(my - 1.75 * U), int(my + 1.75 * U)
    C = np.zeros((b1 - b0, a1 - a0), float)
    ya, yb, xa, xb = max(0, b0), min(H, b1), max(0, a0), min(W, a1)
    if yb > ya and xb > xa: C[ya - b0:yb - b0, xa - a0:xb - a0] = M[ya:yb, xa:xb]
    Hg = hog(resize(C, HOG_SHAPE, anti_aliasing=True), orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2))
    return f, Hg.astype(np.float32), C


recs, hogs = [], []
samples, strokes = {}, {'k': [], 'n': [], 't': []}
for stem, ln in LINES.items():
    if NL.get(stem, 0) == 0: continue
    ws = [enc(w) for w in ln['label'].split()]
    if sum(len(w) for w in ws) != NL[stem]: continue
    i = 0
    for wi, w in enumerate(ws):
        for gi in range(len(w)):
            m = BY.get((stem, i + gi));
            if m is None or m['prob'] < 0.5 or m['i'] not in pos: continue
            res = feats(m)
            if res is None: continue
            f, Hg, C = res
            d = dict(page=m['page'], line=stem, zl_line=int(ln['zl_line']), letter=i + gi, g=m['g'], wi=wi, nw=len(ws), gi=gi, wl=len(w),
                     word=''.join(DEC.get(c, c) for c in w), nxt=DEC.get(w[gi + 1], w[gi + 1]) if gi + 1 < len(w) else '#',
                     prv=DEC.get(w[gi - 1], w[gi - 1]) if gi > 0 else '#', pstart=bool(PS.get(f"{m['page']}_{ln['zl_line']}", False)),
                     lang=ln['language'], scribe=ln['davis_hand'], U=U, wid=m['i'], **f)
            recs.append(d); hogs.append(Hg)
            key = (m['g'], 'L' if wi == 0 and gi == 0 else 'M' if gi == 0 and 2 <= wi <= len(ws) - 2 else '')
            if key[1] and len(samples.setdefault(key, [])) < 40 and np.random.random() < 0.2: samples[key].append(resize(C, (60, 36)))
            kd = 'k' if m['g'] == 'k' else 't' if m['g'] == 't' else 'n' if (m['g'] == 'n' and gi == len(w) - 1 and d['prv'] == 'i') else None
            if kd and f['complete'] >= 0.75 and not (f['clipL'] or f['clipR']) and np.random.random() < 0.08 and len(strokes[kd]) < 400:
                strokes[kd].append((f['tail_w'] if kd == 'n' else f['crossbar'], m['i']))
        i += len(w)
json.dump(recs, open(OUT / 'glyphs.json', 'w'))
np.save(OUT / 'hog.npy', np.array(hogs, dtype=np.float16))
rows = []
for gl in ['y', 's', 'd', 'o', 'q', 'ch', 'sh', 'k', 't']:
    for grp in 'LM':
        s = samples.get((gl, grp), [])[:16]; s = s + [np.zeros((60, 36))] * (16 - len(s))
        rows.append(np.hstack([np.pad(x, 2, constant_values=0.5) for x in s]))
Image.fromarray((255 * (1 - np.vstack(rows))).astype(np.uint8)).save(OUT / 'montage_LM.png')
# stroke-measure montages on the real windows with the mask in red: lowest 16 (top two rows) vs highest 16 (bottom two rows)
for kd, v in strokes.items():
    v.sort(key=lambda t: t[0])
    if len(v) < 32: continue
    tiles = []
    for val, wid in v[:16] + v[-16:]:
        g = wins[wid].astype(float) / 255; M = masks[pos[wid]].astype(bool)
        rgb = np.stack([g, g, g], -1); rgb[M] = rgb[M] * 0.35 + np.array([0.85, 0.1, 0.1]) * 0.65
        t = np.ones((H + 4, W + 4, 3)); t[2:-2, 2:-2] = rgb; tiles.append(t)
    img = np.vstack([np.hstack(tiles[k:k + 8]) for k in range(0, 32, 8)])
    Image.fromarray((img * 255).astype(np.uint8)).resize((img.shape[1] * 2, img.shape[0] * 2), Image.NEAREST).save(OUT / f'montage_{kd}_measure.png')
    json.dump([round(x, 3) for x, _ in v[:16] + v[-16:]], open(OUT / f'montage_{kd}_values.json', 'w'))
print('glyphs', len(recs))
