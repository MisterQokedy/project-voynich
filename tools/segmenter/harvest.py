"""Glyph segmenter, step 1: cut a normalised window around every P2-W letter box and harvest clean exemplars.
python -I harvest.py <voynich-letters repo> <out dir> [limit_pages]
Window: letter box centre +-1.6 U wide, band top - 2.2 U .. band bottom + 1.6 U, resized so U = 20 px -> 96 x 64 (H x W).
Clean exemplar = Otsu ink components touching the box core lie >= 80 % inside the box (grown by 0.2 U), no other box holds
> 15 % of their ink, they cover >= 95 % of the ink inside the box, mask not clipped by the window, mask height >= 0.6 U."""
import csv, json, sys
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.transform import resize
Image.MAX_IMAGE_PIXELS = None
REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 0
EMB = REPO.parent / 'voynich-glyph-embeddings'
image_of = {r['page']: r['iipimage'] for r in csv.DictReader(open(EMB / 'data/word_boxes/aligned.csv')) if r['kept'] == '1'}
lab = {r['page']: r for r in csv.DictReader(open(EMB / 'config/zl_page_labels.csv'))}
LINES = {r['file'][:-4]: r for r in csv.DictReader(open(REPO / 'data/lines/lines.csv'))}
L = defaultdict(list)
for r in csv.DictReader(open(REPO / 'data/letters/letters.csv')): L[r['line']].append(r)
SMALL = {'a', 'o', 'e', 'i'}
UPX, H, W = 20, 96, 64
WL, WU, WD = 1.6, 2.2, 1.6


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
        k = (np.abs(np.polyval(ft, x) - t) < 0.5 * U) & (np.abs(np.polyval(fb, x) - b) < 0.5 * U)
        if k.sum() >= 4: ft, fb = np.polyfit(x[k], t[k], 1), np.polyfit(x[k], b[k], 1)
        return U, (lambda X: float(np.polyval(ft, X))), (lambda X: float(np.polyval(fb, X)))
    mt, mb = float(np.median(t)), float(np.median(b)); return U, (lambda X: mt), (lambda X: mb)


sheets = sorted({f"{v['quire']}-{v['bifolium']}" for v in lab.values()})
perm = np.random.RandomState(0).permutation(len(sheets)); FOLD = {s: int(perm[i] % 2) for i, s in enumerate(sheets)}
bypage = defaultdict(list)
for stem in L: bypage[stem.rsplit('_', 1)[0]].append(stem)
pages = sorted(bypage)[:LIMIT] if LIMIT else sorted(bypage)
wins, meta = [], []
nclean = defaultdict(int)
for page in pages:
    if page not in image_of: print('no image', page); continue
    src = EMB / 'data/raw/digipal_project/images' / image_of[page]
    if not src.exists(): print('missing', src); continue
    G = np.asarray(Image.open(src).convert('L'), dtype=np.float32)
    allb = []   # every letter box on the page: (x0,y0,x1,y1, line, idx)
    for stem in bypage[page]:
        for r in L[stem]:
            if r['x0']: allb.append((int(r['x0']), int(r['y0']), int(r['x1']), int(r['y1']), stem, int(r['letter']), r['zl_letter']))
    AB = np.array([b[:4] for b in allb], float) if allb else np.zeros((0, 4))
    sh = f"{lab[page]['quire']}-{lab[page]['bifolium']}" if page in lab else '?'
    fold = FOLD.get(sh, 0)
    for stem in bypage[page]:
        rec = sorted(L[stem], key=lambda r: int(r['letter']))
        bf = band_fit(rec)
        if bf is None: continue
        U, ftop, fbot = bf; s = UPX / U
        for r in rec:
            if not r['x0']: continue
            x0, y0, x1, y1 = (int(r[k]) for k in ('x0', 'y0', 'x1', 'y1')); cx = (x0 + x1) / 2
            bt, bb = ftop(cx), fbot(cx)
            X0, Y0 = cx - WL * U, bt - WU * U       # window origin (page coords); size W/s x H/s
            Xa, Ya, Xb, Yb = int(round(X0)), int(round(Y0)), int(round(X0 + W / s)), int(round(Y0 + H / s))
            if Xa < 0 or Ya < 0 or Xb > G.shape[1] or Yb > G.shape[0]:   # pad with paper
                pad = np.full((Yb - Ya, Xb - Xa), np.percentile(G, 90), np.float32)
                ya, yb, xa, xb = max(0, Ya), min(G.shape[0], Yb), max(0, Xa), min(G.shape[1], Xb)
                if yb <= ya or xb <= xa: continue
                pad[ya - Ya:yb - Ya, xa - Xa:xb - Xa] = G[ya:yb, xa:xb]; crop = pad
            else:
                crop = G[Ya:Yb, Xa:Xb]
            g = resize(crop, (H, W), anti_aliasing=True, preserve_range=True)
            sx, sy = W / (Xb - Xa), H / (Yb - Ya)
            tb = [(x0 - Xa) * sx, (y0 - Ya) * sy, (x1 - Xa) * sx, (y1 - Ya) * sy]
            near = (AB[:, 2] > Xa) & (AB[:, 0] < Xb) & (AB[:, 3] > Ya) & (AB[:, 1] < Yb)
            ob = [[(b[0] - Xa) * sx, (b[1] - Ya) * sy, (b[2] - Xa) * sx, (b[3] - Ya) * sy, allb[j][4] == stem, allb[j][6]]
                  for j, b in zip(np.nonzero(near)[0], AB[near]) if not (allb[j][4] == stem and allb[j][5] == int(r['letter']))]
            m = dict(page=page, line=stem, zl_line=int(LINES[stem]['zl_line']) if stem in LINES else -1, letter=int(r['letter']),
                     g=r['zl_letter'], prob=float(r['zl_prob']), fold=fold, sheet=sh, U=U, bt=(bt - Ya) * sy, bb=(bb - Ya) * sy,
                     box=[round(v, 2) for v in tb], others=[[round(v, 2) for v in o[:4]] + [int(o[4]), o[5]] for o in ob],
                     scribe=lab.get(page, {}).get('davis_hand', ''), lang=lab.get(page, {}).get('language', ''))
            # clean-exemplar test
            paper = np.percentile(g, 90); ink = paper - g; pos = ink[ink > 5]
            thr = max(otsu(pos) if pos.size > 30 else 30, 25); B = ink > thr
            lab_, n = ndimage.label(B, structure=np.ones((3, 3)))
            bx0, by0, bx1, by1 = tb; w, h = bx1 - bx0, by1 - by0
            core = lab_[int(by0 + .3 * h):int(by1 - .3 * h) + 1, int(bx0 + .3 * w):int(bx1 - .3 * w) + 1]
            keep = sorted(set(np.unique(core)) - {0}); clean = False
            if keep and m['prob'] >= 0.5:
                M = np.isin(lab_, keep)
                gx0, gy0, gx1, gy1 = int(max(0, bx0 - .2 * UPX)), int(max(0, by0 - .2 * UPX)), int(min(W, bx1 + .2 * UPX)) + 1, int(min(H, by1 + .2 * UPX)) + 1
                inside = np.zeros_like(M); inside[gy0:gy1, gx0:gx1] = True
                ok = True
                for c in keep:
                    cm = lab_ == c; a = cm.sum()
                    if (cm & inside).sum() < 0.8 * a: ok = False; break
                    for o in ob:
                        om = np.zeros_like(M); om[int(max(0, o[1])):int(o[3]) + 1, int(max(0, o[0])):int(o[2]) + 1] = True
                        # other box share, measured outside the target box (boxes overlap at joins)
                        tbm = np.zeros_like(M); tbm[int(by0):int(by1) + 1, int(bx0):int(bx1) + 1] = True
                        if (cm & om & ~tbm).sum() > 0.15 * a: ok = False; break
                    if not ok: break
                if ok:
                    inbox = B[int(by0):int(by1) + 1, int(bx0):int(bx1) + 1]; minb = M[int(by0):int(by1) + 1, int(bx0):int(bx1) + 1]
                    ys, xs = np.nonzero(M)
                    clean = (minb.sum() >= 0.95 * max(inbox.sum(), 1) and ys.min() > 0 and ys.max() < H - 1 and xs.min() > 0
                             and xs.max() < W - 1 and (ys.max() - ys.min() + 1) >= 0.6 * UPX)
            if clean:   # the mask must not take over a neighbouring letter: <= 20 % of the ink in any other box's core
                for o in ob:
                    ow, oh = o[2] - o[0], o[3] - o[1]
                    sl = (slice(int(max(0, o[1] + .3 * oh)), int(max(0, o[3] - .3 * oh)) + 1), slice(int(max(0, o[0] + .3 * ow)), int(max(0, o[2] - .3 * ow)) + 1))
                    oi = B[sl].sum()
                    if oi > 3 and M[sl].sum() > 0.2 * oi: clean = False; break
            m['clean'] = bool(clean); m['i'] = len(wins)
            if clean:
                nclean[m['g']] += 1
                m['mask_bits'] = np.packbits(M.astype(np.uint8)).tobytes().hex()
            wins.append(np.clip(g, 0, 255).astype(np.uint8)); meta.append(m)
    print(page, len(wins), sum(nclean.values()), flush=True)
np.save(OUT / 'wins.npy', np.stack(wins))
json.dump(meta, open(OUT / 'meta.json', 'w'))
print('windows', len(wins), 'clean', sum(nclean.values()))
print(json.dumps(dict(sorted(nclean.items(), key=lambda t: -t[1]))))
