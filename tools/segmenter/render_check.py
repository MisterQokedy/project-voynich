"""Montage of rendered training scenes (truth mask in red, target box in blue). python -I render_check.py <data> <fold> <out.png>"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.argv, args = sys.argv[:1], sys.argv[1:]
import importlib.util
spec = importlib.util.spec_from_file_location('tr', str(Path(__file__).parent / 'train.py'))
D, fold, outp = Path(args[0]), int(args[1]), args[2]
sys.argv = ['x', str(D), str(fold), '/tmp/gs_dummy']
tr = importlib.util.module_from_spec(spec); spec.loader.exec_module(tr)
wins = np.load(D / 'wins.npy', mmap_mode='r'); meta = json.load(open(D / 'meta.json'))
b = tr.Bank(wins, meta, fold, 1)
print({k: len(v) for k, v in sorted(b.ex.items(), key=lambda t: -len(t[1]))})
tiles = []
for _ in range(36):
    x, y = b.scene(); g = np.clip(x[0] * 64 + 128, 0, 255) / 255
    rgb = np.stack([g, g, g], -1); M = y > 0; rgb[M] = rgb[M] * 0.4 + np.array([0.85, 0.1, 0.1]) * 0.6
    cb = x[1] > 0; edge = cb & ~np.pad(cb, 1)[2:, 1:-1] | cb & ~np.pad(cb, 1)[:-2, 1:-1] | cb & ~np.pad(cb, 1)[1:-1, 2:] | cb & ~np.pad(cb, 1)[1:-1, :-2]
    rgb[edge] = [0.1, 0.3, 1]
    raw = np.stack([g, g, g], -1)
    t = np.ones((100, 132, 3)); t[2:98, 2:66] = raw; t[2:98, 68:132] = rgb; tiles.append(t)
rows = [np.hstack(tiles[i:i + 6]) for i in range(0, 36, 6)]
img = np.vstack(rows); Image.fromarray((img * 255).astype(np.uint8)).resize((img.shape[1] * 2, img.shape[0] * 2), Image.NEAREST).save(outp)
