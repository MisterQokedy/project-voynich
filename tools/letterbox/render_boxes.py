"""Box-render control images: each letter box drawn as an outlined ellipse (gallows k/t/p/f get a crossbar), nothing else.
python -I render_boxes.py <voynich-letters repo> <out dir>"""
import csv, sys
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw
REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
by = defaultdict(list)
for r in csv.DictReader(open(REPO / 'data/letters/letters.csv')):
    if r['x0']: by[r['page']].append(r)
for p, rs in by.items():
    W = max(int(r['x1']) for r in rs) + 200; H = max(int(r['y1']) for r in rs) + 200
    im = Image.new('L', (W, H), 200); d = ImageDraw.Draw(im)
    for r in rs:
        x0, y0, x1, y1 = [int(r[k]) for k in ('x0', 'y0', 'x1', 'y1')]; t = max(2, (y1 - y0) // 12)
        d.ellipse([x0 + 1, y0 + 1, x1 - 1, y1 - 1], outline=40, width=t)
        if r['zl_letter'] in ('k', 't', 'p', 'f'): d.rectangle([x0 + 1, y0 + (y1 - y0) // 2, x1 - 1, y0 + (y1 - y0) // 2 + t], fill=40)
    im.save(OUT / f'{p}.png')
print('rendered', len(by))
