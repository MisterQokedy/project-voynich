"""Per-page physical maps in LEAF FRAME (versos mirrored so gutter is left, fore-edge right)."""
import sys, re, json
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
sys.path.insert(0, 'code'); from seg import segment
lab = [l.rstrip('\n').split('\t') for l in open('canvases.tsv')]
GX, GY = 48, 64
out = {}
for i, l in enumerate(lab):
    m = re.fullmatch(r'(\d+)([rv])', l[1])
    if not m: continue
    page = l[1]; side = m.group(2)
    (x0, y0, x1, y1), a = segment('small/%03d.jpg' % i, side)
    w, h = x1 - x0, y1 - y0
    # inset to avoid neighbouring leaves / flyleaf / page edges
    x0i, x1i = x0 + int(0.07 * w), x1 - int(0.07 * w); y0i, y1i = y0 + int(0.04 * h), y1 - int(0.04 * h)
    sub = a[y0i:y1i, x0i:x1i]
    if side == 'v': sub = sub[:, ::-1]
    # crude CIELab-ish: L = luminance, b = yellowness (R+G)/2 - B, sat
    R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    Lm = 0.299 * R + 0.587 * G + 0.114 * B; bm = (R + G) / 2 - B
    mx = sub.max(2); mn = sub.min(2); sat = (mx - mn) / (mx + 1)
    hh, ww = Lm.shape; cy = np.linspace(0, hh, GY + 1).astype(int); cx = np.linspace(0, ww, GX + 1).astype(int)
    P80 = np.zeros((GY, GX)); Bm = np.zeros((GY, GX)); PIG = np.zeros((GY, GX)); INK = np.zeros((GY, GX))
    for yy in range(GY):
        for xx in range(GX):
            c = Lm[cy[yy]:cy[yy+1], cx[xx]:cx[xx+1]]; cb = bm[cy[yy]:cy[yy+1], cx[xx]:cx[xx+1]]
            cs = sat[cy[yy]:cy[yy+1], cx[xx]:cx[xx+1]]
            P80[yy, xx] = np.percentile(c, 80)
            sel = c >= np.percentile(c, 60); Bm[yy, xx] = cb[sel].mean()
            INK[yy, xx] = (c < P80[yy, xx] - 45).mean()
    out[page] = dict(P80=P80, B=Bm, INK=INK, idx=i)
np.save('phys_maps.npy', out, allow_pickle=True)
print(len(out), 'pages')
