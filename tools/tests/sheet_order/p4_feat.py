"""P4 features for hair/flesh: blank-parchment tiles at full resolution: yellowness, fine-scale dark-spot density, texture."""
import sys, re, json
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, 'code'); from seg import segment
lab = [l.rstrip('\n').split('\t') for l in open('canvases.tsv')]
def work(i):
    l = lab[i]; side = l[1][-1]
    (x0, y0, x1, y1), sm = segment('small/%03d.jpg' % i, side)
    im = Image.open('img/%03d.jpg' % i).convert('RGB'); a = np.asarray(im).astype(np.float32)
    f = a.shape[1] / sm.shape[1]
    X0, X1, Y0, Y1 = [int(v * f) for v in (x0, x1, y0, y1)]
    w, h = X1 - X0, Y1 - Y0
    sub = a[Y0 + int(.08*h):Y1 - int(.08*h), X0 + int(.12*w):X1 - int(.12*w)]
    L = sub.mean(2); R, G, B = sub[..., 0], sub[..., 1], sub[..., 2]
    T = 64; res = []
    med = np.median(L)
    for yy in range(0, L.shape[0] - T, T):
        for xx in range(0, L.shape[1] - T, T):
            t = L[yy:yy+T, xx:xx+T]
            if t.min() < med - 55 or t.mean() < med - 18: continue  # ink / dark stain
            tr = sub[yy:yy+T, xx:xx+T]; mx = tr.max(2); mn = tr.min(2)
            if ((mx - mn) / (mx + 1)).mean() > .30: continue
            dog = gaussian_filter(t, 1.2) - gaussian_filter(t, 4)
            bb = ((R[yy:yy+T, xx:xx+T] + G[yy:yy+T, xx:xx+T]) / 2 - B[yy:yy+T, xx:xx+T]).mean()
            res.append((bb, (dog < -3).mean(), dog.std(), t.mean()))
    r = np.array(res)
    if len(r) < 10: return l[1], None
    return l[1], dict(n=len(r), yellow=float(np.median(r[:, 0]) / np.median(r[:, 3])), spots=float(np.median(r[:, 1])),
                      tex=float(np.median(r[:, 2])), bright=float(np.median(r[:, 3])))
ids = [i for i, l in enumerate(lab) if re.fullmatch(r'\d+[rv]', l[1])]
with ProcessPoolExecutor(4) as ex: out = dict(ex.map(work, ids))
json.dump(out, open('p4_feat.json', 'w'), indent=0)
print(sum(v is not None for v in out.values()), 'pages with features')
