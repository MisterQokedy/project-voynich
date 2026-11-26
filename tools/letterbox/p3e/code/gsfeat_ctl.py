"""P3-e: glyphs.json / hog.npy for p3.py from control windows. feats() copied from glyphseg/code/gsfeat.py unchanged.
python -I gsfeat_ctl.py <data dir> <masks.npy | box> <out dir> [clip]
'box' = box control: mask is a filled ellipse inscribed in the letter box."""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.feature import hog
from skimage.morphology import skeletonize
from skimage.transform import resize
D, MM, OUT = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
CLIP = len(sys.argv) > 4 and sys.argv[4] == 'clip'
OUT.mkdir(parents=True, exist_ok=True)
wins = np.load(D / 'wins.npy', mmap_mode='r'); meta = json.load(open(D / 'meta.json'))
H, W, U = 96, 64, 20.0
YY, XX = np.mgrid[0:H, 0:W]
if MM == 'box':
    masks = None; pos = {m['i']: m['i'] for m in meta}
else:
    masks = np.load(MM, mmap_mode='r'); pos = {i: k for k, i in enumerate(json.load(open(MM.replace('.npy', '_idx.json'))))}
HOG_SHAPE = (56, 24)
np.random.seed(5)


def otsu(v):
    h, e = np.histogram(v, 128); c = (e[:-1] + e[1:]) / 2; w = np.cumsum(h); m = np.cumsum(h * c); wb = w[-1] - w; mb = m[-1] - m
    ok = (w > 0) & (wb > 0); var = np.where(ok, w * wb * ((m / np.maximum(w, 1)) - (mb / np.maximum(wb, 1))) ** 2, 0)
    return c[np.argmax(var)]


def getmask(m):
    if masks is not None: return masks[pos[m['i']]].astype(bool).copy()
    x0, y0, x1, y1 = m['box']; cx, cy, rx, ry = (x0 + x1) / 2, (y0 + y1) / 2, max((x1 - x0) / 2, 1), max((y1 - y0) / 2, 1)
    return ((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2 <= 1


def feats(m):
    M = getmask(m); g = wins[m['i']].astype(float)
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


recs, hogs, samples = [], [], {}
for m in meta:
    if m['prob'] < 0.5 or m['i'] not in pos: continue
    res = feats(m)
    if res is None: continue
    f, Hg, C = res
    d = dict(page=m['page'], line=m['line'], zl_line=m['zl_line'], letter=m['letter'], g=m['g'], wi=m['wi'], nw=m['nw'], gi=m['gi'],
             wl=m['wl'], word=m['word'], nxt=m['nxt'], prv=m['prv'], pstart=m['pstart'], lang='A', scribe='1', U=U, wid=m['i'], **f)
    recs.append(d); hogs.append(Hg)
    wi, gi, nw = m['wi'], m['gi'], m['nw']
    key = (m['g'], 'L' if wi == 0 and gi == 0 else 'M' if gi == 0 and 2 <= wi <= nw - 2 else '')
    if key[1] and len(samples.setdefault(key, [])) < 40 and np.random.random() < 0.3: samples[key].append((resize(C, (60, 36)), m['i']))
json.dump(recs, open(OUT / 'glyphs.json', 'w')); np.save(OUT / 'hog.npy', np.array(hogs, dtype=np.float16))
# by-eye montage: real windows with mask in red, 24 L and 24 M (pooled over classes)
if masks is not None:
    L = [s for (g, k), v in samples.items() if k == 'L' for s in v]; Mm = [s for (g, k), v in samples.items() if k == 'M' for s in v]
    rng = np.random.default_rng(3); tiles = []
    for grp in (L, Mm):
        for j in rng.permutation(len(grp))[:24]:
            wid = grp[j][1]; g = wins[wid].astype(float) / 255; M = masks[pos[wid]].astype(bool)
            rgb = np.stack([g, g, g], -1); rgb[M] = rgb[M] * 0.35 + np.array([0.85, 0.1, 0.1]) * 0.65
            t = np.ones((H + 4, W + 4, 3)); t[2:-2, 2:-2] = rgb; tiles.append(t)
    while len(tiles) % 8: tiles.append(np.ones((H + 4, W + 4, 3)))
    img = np.vstack([np.hstack(tiles[k:k + 8]) for k in range(0, len(tiles), 8)])
    Image.fromarray((img * 255).astype(np.uint8)).resize((img.shape[1] * 2, img.shape[0] * 2), Image.NEAREST).save(OUT / 'montage_real_LM.png')
print('glyphs', len(recs))
