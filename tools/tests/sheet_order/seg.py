import numpy as np
from PIL import Image
def segment(path, side):
    """Return bbox (x0,y0,x1,y1) of the main page in a 600px thumbnail scale coords, plus image array."""
    im = Image.open(path).convert('RGB'); a = np.asarray(im).astype(float)
    L = a.mean(2); mask = L > 95
    H, W = mask.shape
    rows = mask.mean(1); y = np.where(rows > 0.35)[0]; y0, y1 = y[0], y[-1]
    cols = mask[y0:y1].mean(0)
    good = cols > 0.80
    # longest run of good columns
    best = (0, 0); s = None
    for x in range(W + 1):
        g = good[x] if x < W else False
        if g and s is None: s = x
        if not g and s is not None:
            if x - s > best[1] - best[0]: best = (s, x)
            s = None
    x0, x1 = best
    rr = mask[:, x0:x1].mean(1); y = np.where(rr > 0.8)[0]; y0, y1 = y[0], y[-1]
    return (x0, y0, x1, y1), a

def refine(path, side):
    (x0, y0, x1, y1), a = segment(path, side)
    L = a.mean(2)
    from scipy.ndimage import uniform_filter1d
    w = x1 - x0; h = y1 - y0
    ys = slice(y0 + h // 5, y1 - h // 5); xs = slice(x0 + w // 5, x1 - w // 5)
    g = np.abs(np.diff(L[ys, x0:x1], axis=1)).mean(0); g = uniform_filter1d(g, 3)
    band = int(0.16 * w)
    lx = x0 + int(np.argmax(g[:band])) + 1
    rx = x0 + band_off(g, band) 
    gy = np.abs(np.diff(L[y0:y1, xs], axis=0)).mean(1); gy = uniform_filter1d(gy, 3)
    bh = int(0.08 * h)
    ty = y0 + int(np.argmax(gy[:bh])) + 1
    by = y0 + len(gy) - bh + int(np.argmax(gy[-bh:]))
    return (lx, ty, rx, by), a
def band_off(g, band):
    return len(g) - band + int(np.argmax(g[-band:]))
