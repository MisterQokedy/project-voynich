"""P3-d: mean line-edge vs mid-line GS masks (clipped), aligned on the box centre, U = 20 px; figure for the paper."""
import json, os
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
W_ = os.path.expanduser('~/glyphseg_work')
R = json.load(open(f'{W_}/feat_clip/glyphs.json')); meta = json.load(open(f'{W_}/data/meta.json'))
masks = np.load(f'{W_}/masks_model.npy', mmap_mode='r'); H, W, U = 96, 64, 20


def clipped(r):
    m = meta[r['wid']]; M = masks[r['wid']].astype(float).copy(); x0, y0, x1, y1 = m['box']; cx = (x0 + x1) / 2
    same = [o for o in m['others'] if o[4] and abs((o[1] + o[3]) / 2 - (y0 + y1) / 2) < U]
    a = [o for o in same if (o[0] + o[2]) / 2 < cx]; b = [o for o in same if (o[0] + o[2]) / 2 > cx]
    if a: M[:, :max(0, min(W, int(round(max((o[0] + o[2]) / 2 for o in a))) + 1))] = 0
    if b: M[:, max(0, min(W, int(round(min((o[0] + o[2]) / 2 for o in b))))):] = 0
    return M  # windows are already centred on the box centre and the band top


ok = lambda r: not r['pstart'] and r['nw'] >= 4 and r['complete'] >= 0.75
SETS = [('y', 'L'), ('t', 'L'), ('sh', 'L'), ('q', 'L'), ('n', 'R'), ('y', 'R')]
fig, ax = plt.subplots(len(SETS), 3, figsize=(5.4, 2.1 * len(SETS)))
stats = {}
for k, (g, side) in enumerate(SETS):
    if side == 'L':
        A = [r for r in R if ok(r) and r['g'] == g and r['wi'] == 0 and r['gi'] == 0]
        B = [r for r in R if ok(r) and r['g'] == g and r['gi'] == 0 and 2 <= r['wi'] <= r['nw'] - 2]
    else:
        A = [r for r in R if ok(r) and r['g'] == g and r['wi'] == r['nw'] - 1 and r['gi'] == r['wl'] - 1 and r['wl'] >= 2]
        B = [r for r in R if ok(r) and r['g'] == g and r['gi'] == r['wl'] - 1 and r['wl'] >= 2 and 1 <= r['wi'] <= r['nw'] - 3]
    B = [B[j] for j in np.random.RandomState(0).permutation(len(B))[:2000]]
    mA = np.mean([clipped(r) for r in A], 0); mB = np.mean([clipped(r) for r in B], 0)
    stats[f'{g}-{side}'] = (len(A), len(B))
    lbl = 'line-initial' if side == 'L' else 'line-final'; mid = 'mid-line'
    for j, (img, t, cm, lim) in enumerate([(mA, f'{g}: {lbl} (n={len(A)})', 'Greys', (0, 1)), (mB, f'{g}: {mid} (n={len(B)})', 'Greys', (0, 1)),
                                           (mA - mB, 'difference', 'RdBu_r', (-0.35, 0.35))]):
        ax[k, j].imshow(img, cmap=cm, vmin=lim[0], vmax=lim[1]); ax[k, j].set_title(t, fontsize=7); ax[k, j].axis('off')
fig.text(0.5, 0.005, 'Mean segmenter masks (U = 20 px, windows centred on the letter box). Red = more ink at line edge, blue = more ink mid-line.',
         ha='center', fontsize=6)
plt.tight_layout(rect=(0, 0.02, 1, 1))
plt.savefig('p3d_line_edge_masks.png', dpi=200)
print('P3-d', stats)
