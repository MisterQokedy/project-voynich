"""Cut a straightened line image for one text row from its centre-line fragments."""
import numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates

XH_OUT = 30           # output x-height in pixels; strip height = (UP + DOWN) * XH_OUT = 120
UP, DOWN = 2.2, 1.8   # strip extends this many x-heights above / below the centre line
END_PAD = 0.6         # extend each fragment by this many x-heights at both ends
GAP = 1.5             # paper-coloured gap between fragments of one row, in x-heights


def gray(im):
    return np.asarray(im.convert('L'), dtype=np.float32)


def fragment_strip(g, pts, xh, s=1.0, ox=0.0, oy=0.0):
    """g: grayscale image array; pts in scan px; image px = (scan - o) * s."""
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts])
    step = xh / XH_OUT                           # scan px per output px
    u = np.arange(xs[0] - END_PAD * xh, xs[-1] + END_PAD * xh, step)
    yc = np.interp(u, xs, ys)                    # constant extrapolation at the ends
    v = np.arange(-UP * xh, DOWN * xh, step)
    Y = ((yc[None, :] + v[:, None]) - oy) * s
    X = np.broadcast_to((u[None, :] - ox) * s, Y.shape)
    return map_coordinates(g, [Y, X], order=1, mode='nearest')


def row_image(g, row, xh, s=1.0, ox=0.0, oy=0.0):
    strips = [fragment_strip(g, f['pts'], xh, s, ox, oy) for f in row['frags']]
    paper = float(np.median(np.concatenate([st.ravel() for st in strips])))
    gap = np.full((strips[0].shape[0], int(GAP * XH_OUT)), paper, np.float32)
    parts = []
    for i, st in enumerate(strips):
        if i:
            parts.append(gap)
        parts.append(st)
    a = np.clip(np.concatenate(parts, 1), 0, 255).astype(np.uint8)
    return Image.fromarray(a)
