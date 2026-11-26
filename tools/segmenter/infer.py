"""Cross-fitted masks for every real letter window + the H10g-style baseline masks, and rendered held-out evaluation.
python -I infer.py <data dir> <work dir>
Writes <work>/masks_model.npy (+ _idx.json), masks_base.npy (+ _idx.json), eval_render.json."""
import json, sys, importlib.util
from pathlib import Path
import numpy as np
import torch
from scipy import ndimage
D, WK = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location('tr', str(Path(__file__).parent / 'train.py'))
sys.argv = ['x', str(D), '0', '/tmp/gs_dummy']
tr = importlib.util.module_from_spec(spec); spec.loader.exec_module(tr)
H, W, UPX = tr.H, tr.W, tr.UPX
wins = np.load(D / 'wins.npy', mmap_mode='r'); meta = json.load(open(D / 'meta.json'))


def otsu(v):
    h, e = np.histogram(v, 128); c = (e[:-1] + e[1:]) / 2; w = np.cumsum(h); m = np.cumsum(h * c); wb = w[-1] - w; mb = m[-1] - m
    ok = (w > 0) & (wb > 0); var = np.where(ok, w * wb * ((m / np.maximum(w, 1)) - (mb / np.maximum(wb, 1))) ** 2, 0)
    return c[np.argmax(var)]


def baseline(g, tb, others, bt, gall):
    """H10g threshold-and-cut, in window coordinates. others: [x0,y0,x1,y1,same_line,(cls)]"""
    paper = np.percentile(g, 90); ink = paper - g; pv = ink[ink > 5]
    thr = max(otsu(pv) if pv.size > 30 else 30, 25); B = ink > thr
    x0, y0, x1, y1 = tb; cx = (x0 + x1) / 2
    same = [o for o in others if o[4] and abs((o[1] + o[3]) / 2 - (y0 + y1) / 2) < UPX]
    left = [o for o in same if (o[0] + o[2]) / 2 < cx]; right = [o for o in same if (o[0] + o[2]) / 2 > cx]
    if left:
        o = max(left, key=lambda o: o[2]); c = int(round((o[2] + x0) / 2)); B[:, :max(0, min(W, c))] = False
    if right:
        o = min(right, key=lambda o: o[0]); c = int(round((o[0] + x1) / 2)); B[:, max(0, min(W, c)):] = False
    cut = int(bt - (1.8 if gall else 1.3) * UPX)
    if cut > 0: B[:cut] = False
    lab, n = ndimage.label(B, structure=np.ones((3, 3)))
    w, h = x1 - x0, y1 - y0
    core = lab[int(max(0, y0 + .3 * h)):int(max(0, y1 - .3 * h)) + 1, int(max(0, x0 + .3 * w)):int(max(0, x1 - .3 * w)) + 1]
    keep = list(set(np.unique(core)) - {0})
    if not keep:
        core = lab[int(max(0, y0)):int(max(0, y1)) + 1, int(max(0, x0)):int(max(0, x1)) + 1]; keep = list(set(np.unique(core)) - {0})
    return np.isin(lab, keep) if keep else np.zeros_like(B)


def post(P, tb):
    """threshold 0.5, keep components that overlap the target box grown by 0.1 U, drop specks < 6 px"""
    M = P > 0.5; lab, n = ndimage.label(M, structure=np.ones((3, 3)))
    if n == 0: return M
    x0, y0, x1, y1 = tb; g = 0.1 * UPX
    sl = lab[int(max(0, y0 - g)):int(max(0, y1 + g)) + 1, int(max(0, x0 - g)):int(max(0, x1 + g)) + 1]
    keep = [c for c in set(np.unique(sl)) - {0} if (lab == c).sum() >= 6]
    return np.isin(lab, keep)


def load(f):
    net = tr.UNet().cuda().eval(); net.load_state_dict(torch.load(WK / f'model_f{f}' / 'model.pt', map_location='cuda')); return net


@torch.no_grad()
def predict(net, X):
    out = []
    for i in range(0, len(X), 512):
        x = torch.from_numpy(np.stack(X[i:i + 512])).cuda()
        with torch.autocast('cuda', dtype=torch.bfloat16): out.append(torch.sigmoid(net(x).float()).cpu().numpy())
    return np.concatenate(out)


GALL = {'k', 't', 'p', 'f', 'ckh', 'cth', 'cph', 'cfh'}
if __name__ == '__main__':
    nets = {f: load(f) for f in (0, 1)}
    res = {}
    for f in (0, 1):
        b = tr.Bank(wins, meta, 1 - f, 321 + f)
        pc = {}
        for cls in ('k', 't', 'n', 'o', 'ch', 'y', 'e', 'd'):
            ctxs = [m for m in b.ctx if m['g'] == cls]
            if cls not in b.ex or not ctxs: continue
            X, Y, BL, TB = [], [], [], []
            for j in range(min(400, 4 * len(ctxs))):
                c = ctxs[b.rng.randint(len(ctxs))]
                Tt, Mt, tbx = b.place(b.pick(c['g']), c['box']); Ts = Tt.copy(); ob = []
                for o in c['others']:
                    Tn, Mn, nb = b.place(b.pick(o[5]), o[:4]); Ts *= np.clip(1 - (1 - Tn) * b.rng.uniform(0.7, 1.15), 0.03, 1)
                    ob.append(list(nb) + [o[4]])
                bg = wins[b.bg_ids[b.rng.randint(len(b.bg_ids))]].astype(np.float32)
                bg = ndimage.gaussian_filter(ndimage.grey_closing(bg, size=(11, 11)), 1.0)
                img = np.clip(bg * Ts + b.rng.normal(0, 3, Ts.shape), 0, 255)
                X.append(b.channels(img, tbx, [o[:4] for o in ob])); Y.append(Mt); TB.append(tbx)
                BL.append(baseline(img, tbx, ob, c['bt'], cls in GALL))
            Pm = predict(nets[f], X)
            iou = lambda A, B: (A & B).sum() / max((A | B).sum(), 1)
            im = [iou(post(Pm[j], TB[j]), Y[j]) for j in range(len(X))]
            ib = [iou(BL[j], Y[j]) for j in range(len(X))]
            pc[cls] = dict(n=len(X), model=round(float(np.mean(im)), 3), base=round(float(np.mean(ib)), 3))
            print('fold model', f, cls, pc[cls], flush=True)
        res[f] = pc
    json.dump(res, open(WK / 'eval_render.json', 'w'), indent=1)
    # 2) real windows: cross-fitted model masks and baseline masks
    MM = np.zeros((len(meta), H, W), np.uint8); MB = np.zeros((len(meta), H, W), np.uint8)
    for f in (0, 1):
        sel = [m for m in meta if m['fold'] == 1 - f]
        for s in range(0, len(sel), 4096):
            ch = sel[s:s + 4096]
            X = [tr.Bank.channels(wins[m['i']], m['box'], [o[:4] for o in m['others']]) for m in ch]
            Pm = predict(nets[f], X)
            for j, m in enumerate(ch):
                MM[m['i']] = post(Pm[j], m['box'])
                MB[m['i']] = baseline(wins[m['i']].astype(np.float32), m['box'], m['others'], m['bt'], m['g'] in GALL)
            print('real fold', 1 - f, s + len(ch), '/', len(sel), flush=True)
    np.save(WK / 'masks_model.npy', MM); np.save(WK / 'masks_base.npy', MB)
    idx = [m['i'] for m in meta]
    json.dump(idx, open(WK / 'masks_model_idx.json', 'w')); json.dump(idx, open(WK / 'masks_base_idx.json', 'w'))
    print('DONE')
