"""Group daniilvaino row-line fragments into text rows. Uses geometry only (no transliteration)."""
import json
from pathlib import Path

MIN_FRAG_XH = 1.5     # fragments shorter than this many x-heights are dropped (dots, ticks)
SAME_ROW_XH = 1.6     # a fragment joins a row if its mean y is within this many x-heights of the row's y
OVERLAP_XH = 1.0      # ... and it overlaps the row's fragments horizontally by at most this much
MIN_ROW_XH = 3.0      # rows narrower than this in total are dropped
MARK_TYPES_DROP = {'folio_number', 'quire_mark', 'pencil_letter', 'colour_note', 'marginalia', 'month_name',
                   'alphabet_column', 'ex_libris', 'red_tick', 'red_spot', 'scribble', 'dirt', 'other'}


def _frag(pts):
    pts = sorted(([float(x), float(y)] for x, y in pts), key=lambda p: p[0])
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return {'pts': pts, 'x0': xs[0], 'x1': xs[-1], 'y': sum(ys) / len(ys)}


def page_rows(repo, image):
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
    rows = []
    for f in sorted(frags, key=lambda f: -(f['x1'] - f['x0'])):
        best = None
        for r in rows:
            dy = abs(f['y'] - r['y'])
            if dy > SAME_ROW_XH * xh:
                continue
            ov = max(min(f['x1'], g['x1']) - max(f['x0'], g['x0']) for g in r['frags'])
            if ov > OVERLAP_XH * xh:
                continue
            if best is None or dy < best[0]:
                best = (dy, r)
        if best:
            r = best[1]; r['frags'].append(f)
            w = [g['x1'] - g['x0'] for g in r['frags']]
            r['y'] = sum(g['y'] * wi for g, wi in zip(r['frags'], w)) / sum(w)
        else:
            rows.append({'y': f['y'], 'frags': [f]})
    out = []
    for r in rows:
        r['frags'].sort(key=lambda g: g['x0'])
        r['width'] = sum(g['x1'] - g['x0'] for g in r['frags'])
        if r['width'] >= MIN_ROW_XH * xh:
            out.append(r)
    out.sort(key=lambda r: r['y'])
    return out, xh


SKIP_ROW = 0.9        # DP cost of leaving a row unpaired (labels, marks, stray rows)
SKIP_LOC = 1.2        # DP cost of leaving a locus unpaired (row missed or merged)
MAX_RESID = 0.20      # a pair is dropped if |log(width/xh) - log(len) - c| exceeds this (99% of true pairs on count-equal pages are within it)
MIN_R = 0.5           # page kept only if width tracks label length this well over its pairs (>= 6 pairs)
MAX_LOC_SKIP = 0.25   # page kept only if at most this share of its loci is unpaired


def pair_rows(rows, xh, labels):
    """Monotone alignment of rows (top to bottom) to P loci (file order), by width vs label length.
    Returns (list of (row_index, locus_index), info). Uses only lengths of the labels, not their content."""
    import math
    import numpy as np
    n, m = len(rows), len(labels)
    if not n or not m:
        return [], {'r': None, 'kept': False}
    lw = [math.log(max(r['width'] / xh, 1e-3)) for r in rows]
    ll = [math.log(max(len(t), 1)) for t in labels]
    c = float(np.median(lw) - np.median(ll))
    pairs = []
    for _ in range(3):
        D = np.full((n + 1, m + 1), np.inf); B = np.zeros((n + 1, m + 1), int); D[0, 0] = 0
        for i in range(n + 1):
            for j in range(m + 1):
                if i and D[i - 1, j] + SKIP_ROW < D[i, j]:
                    D[i, j] = D[i - 1, j] + SKIP_ROW; B[i, j] = 1
                if j and D[i, j - 1] + SKIP_LOC < D[i, j]:
                    D[i, j] = D[i, j - 1] + SKIP_LOC; B[i, j] = 2
                if i and j:
                    v = D[i - 1, j - 1] + min(abs(lw[i - 1] - ll[j - 1] - c), 2.0)
                    if v < D[i, j]:
                        D[i, j] = v; B[i, j] = 3
        i, j, pairs = n, m, []
        while i or j:
            b = B[i, j]
            if b == 3:
                pairs.append((i - 1, j - 1)); i, j = i - 1, j - 1
            elif b == 1:
                i -= 1
            else:
                j -= 1
        pairs.reverse()
        if not pairs:
            break
        c = float(np.median([lw[a] - ll[b] for a, b in pairs]))
    pairs = [(a, b) for a, b in pairs if abs(lw[a] - ll[b] - c) <= MAX_RESID]
    info = {'rows': n, 'loci': m, 'pairs': len(pairs), 'c': c}
    if len(pairs) >= 6:
        r = float(np.corrcoef([rows[a]['width'] / xh for a, _ in pairs], [len(labels[b]) for _, b in pairs])[0, 1])
    else:
        r = 1.0
    info['r'] = r
    info['kept'] = bool(pairs) and r >= MIN_R and (m - len(pairs)) / m <= MAX_LOC_SKIP
    return (pairs if info['kept'] else []), info
