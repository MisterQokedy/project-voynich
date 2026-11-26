"""Row grouping v2 for bundle 9. Geometry only (no transliteration).

v1 (bundle 7) joined each fragment to the row whose mean y was nearest. On pages where a drawing splits
the text into columns and the lines slope, the right-hand fragment of line k can sit nearer to the mean y
of line k+1, so halves of different lines were glued together (f1v, f48v).

v2 joins fragments left to right. For a left row A and a candidate right fragment B, it extrapolates A's
rightmost fragment along its own fitted slope to B's left end and measures the vertical miss there, in
x-heights. A and B are joined only when each is the other's best match (mutual best) and the miss is
under JOIN_XH. Repeated until nothing joins. Fragment filtering and row filtering are as in v1.
"""
import json
from pathlib import Path
import numpy as np
from rows import MIN_FRAG_XH, MIN_ROW_XH, MARK_TYPES_DROP, _frag

JOIN_PITCH = 0.6      # largest vertical miss at the join point, as a share of the page's row pitch
SHRINK = 0.5          # weight of a fragment's own slope (rest: page median slope)
GAP_W = 0.02          # cost per x-height of horizontal gap, so a join does not skip over a nearer fragment
OVERLAP_XH = 1.0      # B may start at most this far left of A's right end
MAX_GAP_FRAC = 0.75   # largest horizontal gap, as a share of the page's text width
SHORT_XH = 5.0        # fragments shorter than this use the page's median slope


def _fit(f, page_slope, xh):
    xs = np.array([p[0] for p in f['pts']]); ys = np.array([p[1] for p in f['pts']])
    if xs[-1] - xs[0] < SHORT_XH * xh or len(xs) < 3:
        f['slope'] = page_slope
    else:
        f['slope'] = float(np.polyfit(xs, ys, 1)[0])
    f['y0'], f['y1'] = float(ys[0]), float(ys[-1])


def load_frags(repo, image):
    d = json.load(open(Path(repo) / 'data' / 'lines' / f'{image}.json'))
    xh = float(d.get('xheight') or 19.0)
    marks = []
    mp = Path(repo) / 'data' / 'marks' / f'{image}.json'
    if mp.exists():
        for o in json.load(open(mp)).get('objects', []):
            if o.get('type') in MARK_TYPES_DROP and o.get('bbox'):
                marks.append(o['bbox'])
    frags = []
    for l in d['lines']:
        if l.get('status') == 'unclear' or len(l['pts']) < 2:
            continue
        f = _frag(l['pts'])
        if f['x1'] - f['x0'] < MIN_FRAG_XH * xh:
            continue
        mx, my = (f['x0'] + f['x1']) / 2, f['y']
        if any(b[0] <= mx <= b[2] and b[1] <= my <= b[3] for b in marks):
            continue
        frags.append(f)
    return frags, xh


def page_rows(repo, image):
    frags, xh = load_frags(repo, image)
    if not frags:
        return [], xh
    sl, w = [], []
    for f in frags:
        xs = np.array([p[0] for p in f['pts']]); ys = np.array([p[1] for p in f['pts']])
        if xs[-1] - xs[0] >= SHORT_XH * xh and len(xs) >= 3:
            sl.append(np.polyfit(xs, ys, 1)[0]); w.append(xs[-1] - xs[0])
    page_slope = float(np.average(sl, weights=w)) if sl else 0.0
    for f in frags:
        _fit(f, page_slope, xh)
    width = max(f['x1'] for f in frags) - min(f['x0'] for f in frags)
    rows = [{'frags': [f]} for f in frags]
    # row pitch: for each fragment, the gap to the nearest fragment below it that overlaps it horizontally
    dys = []
    for f in frags:
        below = [g['y'] - f['y'] for g in frags if g is not f and g['y'] - f['y'] > 1.5 * xh
                 and min(f['x1'], g['x1']) - max(f['x0'], g['x0']) > SHORT_XH * xh]
        if below:
            dys.append(min(below))
    pitch = float(np.median(dys)) if dys else 3.5 * xh
    join = JOIN_PITCH * pitch / xh

    def cost(A, B):
        a, b = A['frags'][-1], B['frags'][0]
        if b['x0'] < a['x1'] - OVERLAP_XH * xh or b['x0'] - a['x1'] > MAX_GAP_FRAC * width:
            return None
        # B must not overlap any fragment of A by more than OVERLAP_XH
        for g in A['frags']:
            for h in B['frags']:
                if min(g['x1'], h['x1']) - max(g['x0'], h['x0']) > OVERLAP_XH * xh:
                    return None
        xm = (a['x1'] + b['x0']) / 2           # meet halfway; each side extrapolates along its slope,
        sa = SHRINK * a['slope'] + (1 - SHRINK) * page_slope   # shrunk toward the page's median slope
        sb = SHRINK * b['slope'] + (1 - SHRINK) * page_slope
        ya = a['y1'] + sa * (xm - a['x1'])
        yb = b['y0'] + sb * (xm - b['x0'])
        return abs(ya - yb) / xh + GAP_W * max(b['x0'] - a['x1'], 0) / xh

    while True:
        n = len(rows); best_r = [None] * n; best_l = [None] * n
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                c = cost(rows[i], rows[j])
                if c is None or c > join:
                    continue
                if best_r[i] is None or c < best_r[i][0]:
                    best_r[i] = (c, j)
                if best_l[j] is None or c < best_l[j][0]:
                    best_l[j] = (c, i)
        joins = [(i, best_r[i][1]) for i in range(n) if best_r[i] and best_l[best_r[i][1]] and best_l[best_r[i][1]][1] == i]
        if not joins:
            break
        used, new = set(), []
        for i, j in joins:
            if i in used or j in used:
                continue
            used |= {i, j}; new.append({'frags': rows[i]['frags'] + rows[j]['frags']})
        rows = new + [r for k, r in enumerate(rows) if k not in used]
    out = []
    for r in rows:
        r['frags'].sort(key=lambda g: g['x0'])
        r['width'] = sum(g['x1'] - g['x0'] for g in r['frags'])
        w = [g['x1'] - g['x0'] for g in r['frags']]
        r['y'] = sum(g['y'] * wi for g, wi in zip(r['frags'], w)) / sum(w)
        if r['width'] >= MIN_ROW_XH * xh:
            out.append(r)
    out.sort(key=lambda r: r['y'])     # reading order as in v1: width-weighted mean y
    return out, xh
