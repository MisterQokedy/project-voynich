"""Montage of windows with a mask overlaid (red) and the target box (blue outline).
python -I view.py <data dir> <out.png> <mode: clean|model:<masks.npy>|base:<masks.npy>> <classes comma> [n per class] [fold filter] [seed]"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
D = Path(sys.argv[1]); OUTP = sys.argv[2]; mode = sys.argv[3]; cls = sys.argv[4].split(','); N = int(sys.argv[5]) if len(sys.argv) > 5 else 24
FOLD = int(sys.argv[6]) if len(sys.argv) > 6 and sys.argv[6] != '-' else None
SEED = int(sys.argv[7]) if len(sys.argv) > 7 else 0
wins = np.load(D / 'wins.npy', mmap_mode='r'); meta = json.load(open(D / 'meta.json'))
H, W = wins.shape[1:]
masks = None
if mode.startswith(('model:', 'base:')):
    masks = np.load(mode.split(':', 1)[1], mmap_mode='r'); idx = json.load(open(mode.split(':', 1)[1].replace('.npy', '_idx.json')))
    pos = {i: k for k, i in enumerate(idx)}
rng = np.random.RandomState(SEED)
rows = []; picked = []
for c in cls:
    want = c.split(':')[0]; ctx = c.split(':')[1] if ':' in c else None
    cand = [m for m in meta if m['g'] == want and (FOLD is None or m['fold'] == FOLD)
            and (mode != 'clean' or m['clean']) and (masks is None or m['i'] in pos)
            and (ctx is None or m.get('ctx') == ctx)]
    sel = [cand[j] for j in rng.permutation(len(cand))[:N]]
    tiles = []
    for m in sel:
        g = wins[m['i']].astype(float) / 255
        if mode == 'clean': M = np.unpackbits(np.frombuffer(bytes.fromhex(m['mask_bits']), np.uint8))[:H * W].reshape(H, W).astype(bool)
        else: M = masks[pos[m['i']]] > 0
        rgb = np.stack([g, g, g], -1)
        rgb[M] = rgb[M] * 0.35 + np.array([0.85, 0.1, 0.1]) * 0.65
        x0, y0, x1, y1 = [int(round(v)) for v in m['box']]
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W - 1, x1), min(H - 1, y1)
        rgb[y0:y1 + 1, [x0, x1]] = [0.1, 0.3, 1]; rgb[[y0, y1], x0:x1 + 1] = [0.1, 0.3, 1]
        t = np.ones((H + 4, W + 4, 3)); t[2:-2, 2:-2] = rgb; tiles.append(t); picked.append(m['i'])
    while len(tiles) < N: tiles.append(np.ones((H + 4, W + 4, 3)))
    per = 12
    for k in range(0, N, per): rows.append(np.hstack(tiles[k:k + per]))
img = np.vstack(rows)
Image.fromarray((img * 255).astype(np.uint8)).resize((img.shape[1] * 2, img.shape[0] * 2), Image.NEAREST).save(OUTP)
json.dump(picked, open(OUTP.replace('.png', '_ids.json'), 'w'))
print('saved', OUTP, len(picked))
