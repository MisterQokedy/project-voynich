"""P3-c by scribe and by section: write glyphs.json + hog.npy subsets of feat_clip. python -I subsets.py <feat dir> <out root> <page labels csv>"""
import csv, json, sys
from pathlib import Path
import numpy as np
F, O = Path(sys.argv[1]), Path(sys.argv[2])
lab = {r['page']: r for r in csv.DictReader(open(sys.argv[3]))}
R = json.load(open(F / 'glyphs.json')); HG = np.load(F / 'hog.npy')
groups = {}
for i, r in enumerate(R):
    groups.setdefault(f"scribe{r['scribe']}", []).append(i)
    groups.setdefault(f"sec{lab.get(r['page'], {}).get('illustration', '?')}", []).append(i)
for g, idx in sorted(groups.items()):
    if len(idx) < 3000: print('skip', g, len(idx)); continue
    d = O / g; d.mkdir(parents=True, exist_ok=True)
    json.dump([R[i] for i in idx], open(d / 'glyphs.json', 'w')); np.save(d / 'hog.npy', HG[idx]); print(g, len(idx))
