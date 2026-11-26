"""P3-e: control-manuscript windows in the glyphseg/harvest.py format, from Kraken ALTO (lines, words, glyph cuts).
python -I harvest_ctl.py <img dir> <alto dir> <out dir>
Kraken glyph boxes span the line polygon height, so each box is tightened to the Otsu ink inside its cut (x and y).
Window / clean-exemplar logic copied from harvest.py unchanged."""
import json, re, sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.transform import resize
Image.MAX_IMAGE_PIXELS = None
IMG, ALTO, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
SMALL = set('aoeinumc')
LETTER = re.compile(r'^[a-zſ]$')
UPX, H, W = 20, 96, 64
WL, WU, WD = 1.6, 2.2, 1.6


def otsu(v):
    h, e = np.histogram(v, 128); c = (e[:-1] + e[1:]) / 2; w = np.cumsum(h); m = np.cumsum(h * c); wb = w[-1] - w; mb = m[-1] - m
    ok = (w > 0) & (wb > 0); var = np.where(ok, w * wb * ((m / np.maximum(w, 1)) - (mb / np.maximum(wb, 1))) ** 2, 0)
    return c[np.argmax(var)]


def tag(e): return e.tag.rsplit('}', 1)[-1]


def lines_of(xml):
    """-> list of (block idx, line idx in block, [words: [glyphs: (char, x0, y0, x1, y1, conf)]])"""
    root = ET.parse(xml).getroot(); out = []
    for bi, blk in enumerate(e for e in root.iter() if tag(e) == 'TextBlock'):
        for li, tl in enumerate(e for e in blk.iter() if tag(e) == 'TextLine'):
            words = []
            for s in (e for e in tl if tag(e) == 'String'):
                # Kraken glyphs are CTC peak positions (width ~1 px): cut boundaries = midpoints between consecutive peaks,
                # outer boundaries = the String box; vertical = String box
                sx, sy, sw, sh = (float(s.get(k, 0)) for k in ('HPOS', 'VPOS', 'WIDTH', 'HEIGHT'))
                G_ = [g for g in s.iter() if tag(g) == 'Glyph']
                px = [float(g.get('HPOS', 0)) + float(g.get('WIDTH', 0)) / 2 for g in G_]
                gl = []
                for k, g in enumerate(G_):
                    a = sx if k == 0 else (px[k - 1] + px[k]) / 2; b = sx + sw if k == len(G_) - 1 else (px[k] + px[k + 1]) / 2
                    gl.append((g.get('CONTENT', ''), a, sy, max(b, a + 1), sy + sh, float(g.get('GC', 1) or 1)))
                if gl: words.append(gl)
            if words: out.append((bi, li, words))
    return out


def tighten(B, b):
    """ink bbox inside the cut b (page coords) on binary page B; None if no ink"""
    x0, y0, x1, y1 = (int(round(v)) for v in b)
    x0, y0 = max(0, x0), max(0, y0); x1, y1 = min(B.shape[1], x1), min(B.shape[0], y1)
    if x1 - x0 < 2 or y1 - y0 < 2: return None
    sub = B[y0:y1, x0:x1]; ys, xs = np.nonzero(sub)
    if len(ys) < 8: return None
    # keep rows within the main vertical run (drop ink of the line above / below touching the polygon)
    prof = sub.sum(1) > 0; lab, n = ndimage.label(prof)
    if n > 1:
        big = max(range(1, n + 1), key=lambda k: sub[lab == k].sum()); rows = np.nonzero(lab == big)[0]
        ys2 = ys[(ys >= rows[0]) & (ys <= rows[-1])]; xs = xs[(ys >= rows[0]) & (ys <= rows[-1])]; ys = ys2
    return [x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1]


wins, meta = [], []; nclean = defaultdict(int)
pages = sorted(ALTO.glob('*.xml'))
for pi, xml in enumerate(pages):
    page = xml.stem; src = IMG / (page + '.jpg')
    if not src.exists(): continue
    G = np.asarray(Image.open(src).convert('L'), dtype=np.float32)
    paperP = np.percentile(G, 90); inkP = paperP - G; pv = inkP[inkP > 5][::50]
    BP = inkP > max(otsu(pv) if pv.size > 30 else 30, 25)
    fold = pi % 2
    LS = lines_of(xml); recs = []   # per line: list of glyph dicts
    for bi, li, words in LS:
        stem = f'{page}_{bi:02d}_{li:03d}'; gl = []; k = 0
        for wi, w in enumerate(words):
            for gi, (ch, *b, conf) in enumerate(w):
                tb = tighten(BP, b)
                gl.append(dict(stem=stem, letter=k, g=ch, conf=conf, box=tb, wi=wi, nw=len(words), gi=gi, wl=len(w),
                               word=''.join(c[0] for c in w), nxt=w[gi + 1][0] if gi + 1 < len(w) else '#',
                               prv=w[gi - 1][0] if gi > 0 else '#', pstart=(li == 0), zl_line=li)); k += 1
        recs.append(gl)
    allb = [(*r['box'], r['stem'], r['letter'], r['g']) for gl in recs for r in gl if r['box']]
    AB = np.array([b[:4] for b in allb], float) if allb else np.zeros((0, 4))
    for gl in recs:
        pts = [((r['box'][0] + r['box'][2]) / 2, r['box'][1], r['box'][3]) for r in gl if r['box'] and r['g'] in SMALL]
        if len(pts) < 3: continue
        x, t, b = map(np.array, zip(*pts)); U = float(np.median(b - t))
        if U < 4: continue
        if len(pts) >= 6 and np.ptp(x) > 5 * U:
            ft, fb = np.polyfit(x, t, 1), np.polyfit(x, b, 1)
            k_ = (np.abs(np.polyval(ft, x) - t) < 0.5 * U) & (np.abs(np.polyval(fb, x) - b) < 0.5 * U)
            if k_.sum() >= 4: ft, fb = np.polyfit(x[k_], t[k_], 1), np.polyfit(x[k_], b[k_], 1)
            ftop, fbot = (lambda X, f=ft: float(np.polyval(f, X))), (lambda X, f=fb: float(np.polyval(f, X)))
        else:
            mt, mb = float(np.median(t)), float(np.median(b)); ftop, fbot = (lambda X, v=mt: v), (lambda X, v=mb: v)
        s = UPX / U
        for r in gl:
            if not r['box']: continue
            x0, y0, x1, y1 = r['box']; cx = (x0 + x1) / 2; bt, bb = ftop(cx), fbot(cx)
            X0, Y0 = cx - WL * U, bt - WU * U
            Xa, Ya, Xb, Yb = int(round(X0)), int(round(Y0)), int(round(X0 + W / s)), int(round(Y0 + H / s))
            if Xa < 0 or Ya < 0 or Xb > G.shape[1] or Yb > G.shape[0]:
                pad = np.full((Yb - Ya, Xb - Xa), paperP, np.float32)
                ya, yb, xa, xb = max(0, Ya), min(G.shape[0], Yb), max(0, Xa), min(G.shape[1], Xb)
                if yb <= ya or xb <= xa: continue
                pad[ya - Ya:yb - Ya, xa - Xa:xb - Xa] = G[ya:yb, xa:xb]; crop = pad
            else:
                crop = G[Ya:Yb, Xa:Xb]
            g = resize(crop, (H, W), anti_aliasing=True, preserve_range=True)
            sx, sy = W / (Xb - Xa), H / (Yb - Ya)
            tb = [(x0 - Xa) * sx, (y0 - Ya) * sy, (x1 - Xa) * sx, (y1 - Ya) * sy]
            near = (AB[:, 2] > Xa) & (AB[:, 0] < Xb) & (AB[:, 3] > Ya) & (AB[:, 1] < Yb)
            ob = [[(b[0] - Xa) * sx, (b[1] - Ya) * sy, (b[2] - Xa) * sx, (b[3] - Ya) * sy, allb[j][4] == r['stem'], allb[j][6]]
                  for j, b in zip(np.nonzero(near)[0], AB[near]) if not (allb[j][4] == r['stem'] and allb[j][5] == r['letter'])]
            isl = bool(LETTER.match(r['g']))
            m = dict(page=page, line=r['stem'], zl_line=r['zl_line'], letter=r['letter'], g=r['g'], prob=(1.0 if isl else 0.0),
                     ocr_conf=r['conf'], fold=fold, sheet=page, U=U, bt=(bt - Ya) * sy, bb=(bb - Ya) * sy,
                     box=[round(v, 2) for v in tb], others=[[round(v, 2) for v in o[:4]] + [int(o[4]), o[5]] for o in ob],
                     scribe='1', lang='A', wi=r['wi'], nw=r['nw'], gi=r['gi'], wl=r['wl'], word=r['word'], nxt=r['nxt'],
                     prv=r['prv'], pstart=r['pstart'])
            paper = np.percentile(g, 90); ink = paper - g; pos = ink[ink > 5]
            thr = max(otsu(pos) if pos.size > 30 else 30, 25); B = ink > thr
            lab_, n = ndimage.label(B, structure=np.ones((3, 3)))
            bx0, by0, bx1, by1 = tb; w, h = bx1 - bx0, by1 - by0
            core = lab_[int(max(0, by0 + .3 * h)):int(max(0, by1 - .3 * h)) + 1, int(max(0, bx0 + .3 * w)):int(max(0, bx1 - .3 * w)) + 1]
            keep = sorted(set(np.unique(core)) - {0}); clean = False
            if keep and m['prob'] >= 0.5:
                M = np.isin(lab_, keep)
                gx0, gy0, gx1, gy1 = int(max(0, bx0 - .2 * UPX)), int(max(0, by0 - .2 * UPX)), int(min(W, bx1 + .2 * UPX)) + 1, int(min(H, by1 + .2 * UPX)) + 1
                inside = np.zeros_like(M); inside[gy0:gy1, gx0:gx1] = True
                tbm = np.zeros_like(M); tbm[int(max(0, by0)):int(by1) + 1, int(max(0, bx0)):int(bx1) + 1] = True
                ok = True
                for c in keep:
                    cm = lab_ == c; a = cm.sum()
                    if (cm & inside).sum() < 0.8 * a: ok = False; break
                    for o in ob:
                        om = np.zeros_like(M); om[int(max(0, o[1])):int(max(0, o[3])) + 1, int(max(0, o[0])):int(max(0, o[2])) + 1] = True
                        if (cm & om & ~tbm).sum() > 0.15 * a: ok = False; break
                    if not ok: break
                if ok:
                    inbox = B[tbm]; minb = M[tbm]; ys, xs = np.nonzero(M)
                    clean = (minb.sum() >= 0.95 * max(inbox.sum(), 1) and ys.min() > 0 and ys.max() < H - 1 and xs.min() > 0
                             and xs.max() < W - 1 and (ys.max() - ys.min() + 1) >= 0.6 * UPX)
            if clean:
                for o in ob:
                    ow, oh = o[2] - o[0], o[3] - o[1]
                    sl = (slice(int(max(0, o[1] + .3 * oh)), int(max(0, o[3] - .3 * oh)) + 1), slice(int(max(0, o[0] + .3 * ow)), int(max(0, o[2] - .3 * ow)) + 1))
                    oi = B[sl].sum()
                    if oi > 3 and M[sl].sum() > 0.2 * oi: clean = False; break
            m['clean'] = bool(clean); m['i'] = len(wins)
            if clean:
                nclean[m['g']] += 1; m['mask_bits'] = np.packbits(M.astype(np.uint8)).tobytes().hex()
            wins.append(np.clip(g, 0, 255).astype(np.uint8)); meta.append(m)
    print(page, len(wins), sum(nclean.values()), flush=True)
np.save(OUT / 'wins.npy', np.stack(wins)); json.dump(meta, open(OUT / 'meta.json', 'w'))
print('windows', len(wins), 'clean', sum(nclean.values()))
print(json.dumps(dict(sorted(nclean.items(), key=lambda t: -t[1]))))
