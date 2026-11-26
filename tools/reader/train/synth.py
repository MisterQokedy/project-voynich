"""Synthetic line images: training-page ZL text rendered in the Eva-2 font, matched to the real strip geometry
(x-height 30 px, centre line at 2.2 x-heights from the top, strip height 120). Train-page text only."""
import argparse, random, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, str(Path(__file__).parent))
import lineimg as LI


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--font', required=True); ap.add_argument('--text', required=True)
    ap.add_argument('--out', required=True); ap.add_argument('--n', type=int, default=20000)
    ap.add_argument('--seed', type=int, default=20261127)
    a = ap.parse_args()
    r = random.Random(a.seed); nr = np.random.default_rng(a.seed)
    lines = [l.strip() for l in open(a.text) if l.strip()]
    words = [w for l in lines for w in l.split()]
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    probe = ImageFont.truetype(a.font, 100); b = probe.getbbox('o'); xh100 = b[3] - b[1]; mid100 = (b[1] + b[3]) / 2
    H = int((LI.UP + LI.DOWN) * LI.XH_OUT); paths = []
    for i in range(a.n):
        # half real lines, half lines of random training words (so the model cannot memorise whole lines)
        t = r.choice(lines) if r.random() < 0.5 else ' '.join(r.choice(words) for _ in range(r.randint(3, 11)))
        xh = LI.XH_OUT * r.uniform(0.85, 1.15)
        size = max(8, int(round(100 * xh / xh100)))
        f = ImageFont.truetype(a.font, size)
        bb = f.getbbox(t); w = bb[2] - bb[0] + 40
        paper = r.uniform(150, 215); ink = r.uniform(40, 120)
        im = Image.new('L', (w, H + 20), int(paper))
        d = ImageDraw.Draw(im)
        y0 = 10 + LI.UP * LI.XH_OUT - mid100 * size / 100 + r.uniform(-3, 3)
        d.text((20 - bb[0], y0), t, font=f, fill=int(ink))
        im = im.rotate(r.uniform(-1.2, 1.2), resample=Image.BILINEAR, fillcolor=int(paper))
        if r.random() < 0.5:
            im = im.filter(ImageFilter.GaussianBlur(r.uniform(0.3, 1.2)))
        arr = np.asarray(im, np.float32)[10:10 + H]
        arr = arr + nr.normal(0, r.uniform(2, 10), arr.shape)
        arr = arr + np.linspace(r.uniform(-15, 15), r.uniform(-15, 15), arr.shape[1])[None, :]
        p = out / f'syn_{i:06d}.png'
        Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(p)
        (out / f'syn_{i:06d}.gt.txt').write_text(t + '\n')
        paths.append(str(p))
    k = int(0.95 * len(paths))
    (out / 'train.txt').write_text('\n'.join(paths[:k]) + '\n'); (out / 'val.txt').write_text('\n'.join(paths[k:]) + '\n')
    print(f'synth: {len(paths)} lines')


if __name__ == '__main__':
    main()
