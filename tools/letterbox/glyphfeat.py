"""P3 / H10f shared feature extraction (PREREG.md). One record per letter box.
python -I glyphfeat.py <voynich-letters repo> <out dir> <zl_parastart.json>   (WSL env: numpy, PIL, scipy, scikit-image)
Ink mask = Otsu ink in a window around the box, keeping only connected components that touch the box's central
40% x 40% core (box-edge placement does not move the mask). Unit U = local x-height (a/o/e/i boxes, linear fit along the line)."""
import csv, json, os, sys
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.feature import hog
from skimage.morphology import skeletonize
from skimage.transform import resize
Image.MAX_IMAGE_PIXELS = None
np.random.seed(5)
REPO, OUT, PS = Path(sys.argv[1]), Path(sys.argv[2]), json.load(open(sys.argv[3])); OUT.mkdir(parents=True, exist_ok=True)
EMB = REPO.parent / 'voynich-glyph-embeddings'
LIMIT = int(sys.argv[4]) if len(sys.argv) > 4 else 0      # smoke test: number of pages (0 = all)
IMGDIR = Path(sys.argv[5]) if len(sys.argv) > 5 else None  # box-render control: <IMGDIR>/<page>.png
COMP = [("cth", "T"), ("ckh", "K"), ("cph", "P"), ("cfh", "F"), ("ch", "C"), ("sh", "S")]
DEC = {b: a for a, b in COMP}
enc = lambda s: [s := s.replace(a, b) for a, b in COMP][-1]
LINES = {r['file'][:-4]: r for r in csv.DictReader(open(REPO / 'data/lines/lines.csv'))}
image_of = {r['page']: r['iipimage'] for r in csv.DictReader(open(EMB / 'data/word_boxes/aligned.csv')) if r['kept'] == '1'}
L = defaultdict(list)
for r in csv.DictReader(open(REPO / 'data/letters/letters.csv')): L[r['line']].append(r)
SMALL = {'a', 'o', 'e', 'i'}
WIN_W, WIN_UP, WIN_DN = 1.2, 2.0, 1.5         # window half-width, above band top, below band bottom (in U)
HOG_SHAPE = (56, 24)


def otsu(v):
    h, e = np.histogram(v, 128); c = (e[:-1] + e[1:]) / 2; w = np.cumsum(h); m = np.cumsum(h * c); wb = w[-1] - w; mb = m[-1] - m
    ok = (w > 0) & (wb > 0); var = np.where(ok, w * wb * ((m / np.maximum(w, 1)) - (mb / np.maximum(wb, 1))) ** 2, 0)
    return c[np.argmax(var)]


def band_fit(rec):
    pts = [((int(r['x0']) + int(r['x1'])) / 2, int(r['y0']), int(r['y1'])) for r in rec if r['x0'] and r['zl_letter'] in SMALL]
    if len(pts) < 3: return None
    x, t, b = map(np.array, zip(*pts)); U = float(np.median(b - t))
    if len(pts) >= 6 and np.ptp(x) > 5 * U:
        ft, fb = np.polyfit(x, t, 1), np.polyfit(x, b, 1)
        # robust: refit without points > 0.5 U off
        k = (np.abs(np.polyval(ft, x) - t) < 0.5 * U) & (np.abs(np.polyval(fb, x) - b) < 0.5 * U)
        if k.sum() >= 4: ft, fb = np.polyfit(x[k], t[k], 1), np.polyfit(x[k], b[k], 1)
        return U, (lambda X: float(np.polyval(ft, X))), (lambda X: float(np.polyval(fb, X)))
    mt, mb = float(np.median(t)), float(np.median(b)); return U, (lambda X: mt), (lambda X: mb)


GCLS = None


def glyph(G, box, U, bt, bb, cx, lim_l=None, lim_r=None):
    x0, y0, x1, y1 = box
    X0, X1 = int(max(0, cx - WIN_W * U)), int(min(G.shape[1], cx + WIN_W * U))
    Y0, Y1 = int(max(0, min(bt - WIN_UP * U, y0))), int(min(G.shape[0], max(bb + WIN_DN * U, y1)))
    g = G[Y0:Y1, X0:X1]
    if g.size < 50: return None
    paper = np.percentile(g, 90); ink = paper - g; pos = ink[ink > 5]
    thr = max(otsu(pos) if pos.size > 30 else 30, 25); B = ink > thr
    # neighbouring words never merge in: cut at the previous word's last box / next word's first box
    if lim_l is not None and lim_l - X0 > 0: B[:, :min(B.shape[1], int(lim_l - X0))] = False
    if lim_r is not None and lim_r - X0 < B.shape[1]: B[:, max(0, int(lim_r - X0)):] = False
    lab, n = ndimage.label(B, structure=np.ones((3, 3)))
    w, h = x1 - x0, y1 - y0
    cx0, cx1 = int(x0 + 0.3 * w) - X0, int(x1 - 0.3 * w) - X0 + 1
    cy0, cy1 = int(y0 + 0.3 * h) - Y0, int(y1 - 0.3 * h) - Y0 + 1
    core = lab[max(0, cy0):max(0, cy1), max(0, cx0):max(0, cx1)]
    keep = set(np.unique(core)) - {0}
    if not keep:
        core = lab[max(0, y0 - Y0):max(0, y1 - Y0), max(0, x0 - X0):max(0, x1 - X0)]; keep = set(np.unique(core)) - {0}
    if not keep: return None
    M = np.isin(lab, list(keep))
    # P3-b mask cleaning: ink above the glyph's own reach is line-above ink. Rows above bt - REACH*U are cleared
    # (REACH 1.8 for gallows k t p f, else 1.3), then only components touching the box core are kept again.
    reach = 1.8 if GCLS in ('k', 't', 'p', 'f') else 1.3
    cut = int(bt - reach * U) - Y0
    if cut > 0 and not os.environ.get('P3B_NOCLEAN'):
        M[:cut] = False
        lab2, n2 = ndimage.label(M, structure=np.ones((3, 3)))
        core2 = lab2[max(0, cy0):max(0, cy1), max(0, cx0):max(0, cx1)]
        keep2 = set(np.unique(core2)) - {0}
        if not keep2: return None
        M = np.isin(lab2, list(keep2)); keep = keep2
    ys, xs = np.nonzero(M)
    area = M.sum(); sk = skeletonize(M).sum()
    top, bot, left, right = ys.min() + Y0, ys.max() + Y0, xs.min() + X0, xs.max() + X0
    f = dict(top_ext=(bt - top) / U, bot_ext=(bot - bb) / U, left_ext=(cx - left) / U, right_ext=(right - cx) / U,
             height=(bot - top + 1) / U, width=(right - left + 1) / U, aspect=(bot - top + 1) / (right - left + 1),
             dx=(xs.mean() + X0 - cx) / U, dy=(ys.mean() + Y0 - (bt + bb) / 2) / U,
             area=area / U ** 2, ncomp=len(keep), thick=area / max(sk, 1) / U,
             clipL=int(xs.min() == 0), clipR=int(xs.max() == M.shape[1] - 1),
             tone=float(paper - np.median(g[M])), box_w=w / U, box_h=h / U,
             box_dy=((y0 + y1) / 2 - (bt + bb) / 2) / U, box_top=(bt - y0) / U, touch_top=int(ys.min() == 0))
    # gallows crossbar: longest horizontal ink run in rows bt-0.25U .. bt+0.35U
    r0, r1 = int(bt - 0.25 * U) - Y0, int(bt + 0.35 * U) - Y0
    best = 0
    for row in M[max(0, r0):max(0, r1)]:
        if row.any():
            d = np.diff(np.concatenate([[0], row.astype(int), [0]])); s, e = np.nonzero(d == 1)[0], np.nonzero(d == -1)[0]
            best = max(best, int((e - s).max()))
    f['crossbar'] = best / U
    # n tail: right-most ink in the rows above the band middle (final stroke curling up/right)
    mid = int((bt + bb) / 2) - Y0
    up = xs[ys < mid]; f['tail_right'] = ((up.max() + X0) - cx) / U if up.size else 0.0
    f['tail_w'] = (up.max() - xs.min() + 1) / U if up.size else 0.0      # upper-half extent from the glyph's own left edge
    # shape-only mask crop for HOG, centred on the mask's centre of mass: 1.5U wide, 3.5U tall (placement removed)
    mx, my = xs.mean(), ys.mean()
    a0, a1 = int(mx - 0.75 * U), int(mx + 0.75 * U); b0, b1 = int(my - 1.75 * U), int(my + 1.75 * U)
    C = np.zeros((max(1, b1 - b0), max(1, a1 - a0)), float)
    ya, yb, xa, xb = max(0, b0), min(M.shape[0], b1), max(0, a0), min(M.shape[1], a1)
    if yb > ya and xb > xa: C[ya - b0:yb - b0, xa - a0:xb - a0] = M[ya:yb, xa:xb]
    Hg = hog(resize(C, HOG_SHAPE, anti_aliasing=True), orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2))
    return f, Hg.astype(np.float32), C


recs, hogs = [], []
bypage = defaultdict(list)
for stem in L: bypage[stem.rsplit('_', 1)[0]].append(stem)
pages = sorted(bypage)[:LIMIT] if LIMIT else sorted(bypage)
samples = {}
strokes = {'k': [], 'n': []}
for page in pages:
    src = (IMGDIR / f'{page}.png') if IMGDIR else (EMB / 'data/raw/digipal_project/images' / image_of[page]) if page in image_of else None
    if src is None or not src.exists(): print('no image', page); continue
    G = np.asarray(Image.open(src).convert('L'), dtype=float)
    for stem in bypage[page]:
        if stem not in LINES: continue
        ln = LINES[stem]; ws = [enc(w) for w in ln['label'].split()]
        rec = sorted(L[stem], key=lambda r: int(r['letter']))
        if sum(len(w) for w in ws) != len(rec): continue
        bf = band_fit(rec)
        if bf is None: continue
        U, ftop, fbot = bf; i = 0
        pstart = PS.get(f"{page}_{ln['zl_line']}", False)
        starts = []
        for w in ws: starts.append(i); i += len(w)
        i = 0
        bx = lambda r: tuple(int(r[k]) for k in ('x0', 'y0', 'x1', 'y1')) if r['x0'] else None
        for wi, w in enumerate(ws):
            g = rec[i:i + len(w)]; i += len(w)
            prevb = bx(rec[starts[wi] - 1]) if wi > 0 else None
            nextb = bx(rec[starts[wi + 1]]) if wi + 1 < len(ws) else None
            for gi, r in enumerate(g):
                if not r['x0'] or float(r['zl_prob']) < 0.5: continue
                box = tuple(int(r[k]) for k in ('x0', 'y0', 'x1', 'y1')); cx = (box[0] + box[2]) / 2
                GCLS = r['zl_letter']
                res = glyph(G, box, U, ftop(cx), fbot(cx), cx, prevb[2] if prevb else None, nextb[0] if nextb else None)
                if res is None: continue
                f, Hg, C = res
                word = ''.join(DEC.get(c, c) for c in w)
                d = dict(page=page, line=stem, zl_line=int(ln['zl_line']), letter=int(r['letter']), g=r['zl_letter'],
                         wi=wi, nw=len(ws), gi=gi, wl=len(w), word=word,
                         nxt=DEC.get(w[gi + 1], w[gi + 1]) if gi + 1 < len(w) else '#',
                         prv=DEC.get(w[gi - 1], w[gi - 1]) if gi > 0 else '#',
                         pstart=bool(pstart), lang=ln['language'], scribe=ln['davis_hand'], U=U, **f)
                recs.append(d); hogs.append(Hg)
                key = (r['zl_letter'], 'L' if wi == 0 and gi == 0 else 'M' if gi == 0 and 2 <= wi <= len(ws) - 2 else '')
                if key[1] and len(samples.setdefault(key, [])) < 40 and np.random.random() < 0.2:
                    samples[key].append(resize(C, (60, 36)))
                kd = 'k' if r['zl_letter'] == 'k' else 'n' if (r['zl_letter'] == 'n' and gi == len(w) - 1) else None
                if kd and np.random.random() < 0.05 and len(strokes[kd]) < 400:
                    strokes[kd].append((f['crossbar'] if kd == 'k' else f['tail_w'], resize(C, (60, 36))))
    print(page, len(recs), flush=True)
json.dump(recs, open(OUT / 'glyphs.json', 'w'))
np.save(OUT / 'hog.npy', np.array(hogs, dtype=np.float16))
# montage of masks (L row then M row per glyph), for the by-eye check
rows = []
for gl in ['y', 's', 'd', 'o', 'q', 'ch', 'sh', 'k', 't']:
    for grp in 'LM':
        s = samples.get((gl, grp), [])[:16]
        s = s + [np.zeros((60, 36))] * (16 - len(s))
        rows.append(np.hstack([np.pad(x, 2, constant_values=0.5) for x in s]))
if rows:
    Image.fromarray((255 * (1 - np.vstack(rows))).astype(np.uint8)).save(OUT / 'montage_LM.png')
for kd, v in strokes.items():   # by-eye check of the stroke measures: lowest 16 (top row) vs highest 16 (bottom row)
    v.sort(key=lambda t: t[0])
    if len(v) >= 32:
        rr = [np.hstack([np.pad(c, 2, constant_values=0.5) for _, c in part]) for part in (v[:16], v[-16:])]
        Image.fromarray((255 * (1 - np.vstack(rr))).astype(np.uint8)).save(OUT / f'montage_{kd}_measure.png')
        json.dump([round(x, 3) for x, _ in v[:16] + v[-16:]], open(OUT / f'montage_{kd}_values.json', 'w'))
print('glyphs', len(recs))
