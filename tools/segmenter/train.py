"""GS segmenter training on rendered scenes (PREREG.md). python -I train.py <data dir> <fold to TRAIN on> <out dir> [epochs] [steps/epoch]
Scenes: a real letter context (target box + other boxes with classes) re-drawn from clean exemplars of the training fold."""
import json, sys, time, os
from pathlib import Path
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F
from scipy import ndimage
D, FOLD, OUT = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]); OUT.mkdir(parents=True, exist_ok=True)
EPOCHS = int(sys.argv[4]) if len(sys.argv) > 4 else 30
STEPS = int(sys.argv[5]) if len(sys.argv) > 5 else 600
BS = 64
H, W, UPX = 96, 64, 20
FOCUS = {'k': 4, 't': 4, 'p': 2, 'f': 2, 'n': 4, 'ckh': 2, 'cth': 2, 'cph': 1, 'cfh': 1}   # sampling weights for target class


def unpack(m): return np.unpackbits(np.frombuffer(bytes.fromhex(m['mask_bits']), np.uint8))[:H * W].reshape(H, W).astype(bool)


class Bank:
    """Exemplars and contexts of one fold, plus rendering."""
    def __init__(self, wins, meta, fold, seed):
        self.wins, self.rng = wins, np.random.RandomState(seed)
        self.ctx = [m for m in meta if m['fold'] == fold and m['prob'] >= 0.5]
        self.ex = {}
        for m in meta:
            if m['fold'] == fold and m['clean']:
                M = unpack(m); g = wins[m['i']].astype(np.float32); paper = np.percentile(g, 90)
                Md = ndimage.binary_dilation(M, iterations=1)
                T = np.where(Md, np.clip(g / max(paper, 1), 0.05, 1.0), 1.0).astype(np.float32)
                self.ex.setdefault(m['g'], []).append((T, M, np.array(m['box'], np.float32)))
        self.common = [c for c in ('o', 'e', 'y', 'a', 'ch', 'd', 'l', 'r') if c in self.ex]
        w = np.array([FOCUS.get(m['g'], 1) if m['g'] in self.ex else 0 for m in self.ctx], float)
        self.cw = w / w.sum()
        self.bg_ids = [m['i'] for m in self.ctx[::7]]

    def pick(self, g):
        L = self.ex.get(g) or self.ex[self.common[self.rng.randint(len(self.common))]]
        return L[self.rng.randint(len(L))]

    @staticmethod
    def shift(A, dy, dx, fill):
        out = np.full_like(A, fill); ys, yd = (slice(max(0, -dy), H - max(0, dy)), slice(max(0, dy), H - max(0, -dy)))
        xs, xd = (slice(max(0, -dx), W - max(0, dx)), slice(max(0, dx), W - max(0, -dx)))
        out[yd, xd] = A[ys, xs]; return out

    def place(self, ex, box):
        T, M, eb = ex
        dx = int(round((box[0] + box[2]) / 2 - (eb[0] + eb[2]) / 2)); dy = int(round((box[1] + box[3]) / 2 - (eb[1] + eb[3]) / 2))
        dx = int(np.clip(dx, -W + 1, W - 1)); dy = int(np.clip(dy, -H + 1, H - 1))
        return self.shift(T, dy, dx, 1.0), self.shift(M, dy, dx, False), eb + np.array([dx, dy, dx, dy], np.float32)

    def scene(self):
        r = self.rng
        c = self.ctx[r.choice(len(self.ctx), p=self.cw)]
        tex = self.pick(c['g'])
        Tt, Mt, tb = self.place(tex, c['box'])
        Ts = Tt.copy(); ob = []
        for o in c['others']:
            Tn, Mn, nb = self.place(self.pick(o[5]), o[:4])
            k = r.uniform(0.7, 1.15); Ts *= np.clip(1 - (1 - Tn) * k, 0.03, 1); ob.append(nb)
        bg = self.wins[self.bg_ids[r.randint(len(self.bg_ids))]].astype(np.float32)
        bg = ndimage.gaussian_filter(ndimage.grey_closing(bg, size=(11, 11)), 1.0)
        img = bg * Ts
        img = img * r.uniform(0.85, 1.1) + r.uniform(-15, 15)
        if r.rand() < 0.4: img = ndimage.gaussian_filter(img, r.uniform(0.3, 0.9))
        img = img + r.normal(0, r.uniform(1, 5), img.shape)
        jit = lambda b: b + r.uniform(-0.15, 0.15, 4) * UPX
        x = self.channels(np.clip(img, 0, 255), jit(tb), [jit(b) for b in ob])
        return x, Mt.astype(np.float32)

    @staticmethod
    def channels(img, tb, obs):
        g = (img.astype(np.float32) - 128) / 64
        cb = np.zeros((H, W), np.float32); ocb = np.zeros((H, W), np.float32)
        def fill(A, b, v):
            x0, y0, x1, y1 = [int(round(t)) for t in b]
            A[max(0, y0):max(0, min(H, y1 + 1)), max(0, x0):max(0, min(W, x1 + 1))] = v
        for b in obs: fill(ocb, b, 1)
        fill(cb, tb, 1)
        return np.stack([g, cb, ocb])


class DS(torch.utils.data.IterableDataset):
    def __init__(self, D, fold): self.D, self.fold = D, fold
    def __iter__(self):
        wi = torch.utils.data.get_worker_info(); seed = (wi.id if wi else 0) * 7919 + int(time.time()) % 10000
        wins = np.load(self.D / 'wins.npy', mmap_mode='r'); meta = json.load(open(self.D / 'meta.json'))
        b = Bank(wins, meta, self.fold, seed)
        while True:
            x, y = b.scene(); yield torch.from_numpy(x), torch.from_numpy(y)


def block(i, o): return nn.Sequential(nn.Conv2d(i, o, 3, padding=1), nn.BatchNorm2d(o), nn.ReLU(inplace=True),
                                      nn.Conv2d(o, o, 3, padding=1), nn.BatchNorm2d(o), nn.ReLU(inplace=True))


class UNet(nn.Module):
    def __init__(self, c=(32, 64, 128, 256)):
        super().__init__()
        self.d = nn.ModuleList([block(3, c[0]), block(c[0], c[1]), block(c[1], c[2]), block(c[2], c[3])])
        self.u = nn.ModuleList([nn.ConvTranspose2d(c[i + 1], c[i], 2, stride=2) for i in range(3)])
        self.ub = nn.ModuleList([block(2 * c[i], c[i]) for i in range(3)])
        self.head = nn.Conv2d(c[0], 1, 1)
    def forward(self, x):
        s = []
        for i, b in enumerate(self.d):
            x = b(x); s.append(x)
            if i < 3: x = F.max_pool2d(x, 2)
        for i in (2, 1, 0): x = self.ub[i](torch.cat([self.u[i](x), s[i]], 1))
        return self.head(x)[:, 0]


def loss_fn(lo, y):
    p = torch.sigmoid(lo); inter = (p * y).sum((1, 2)); dice = 1 - (2 * inter + 1) / (p.sum((1, 2)) + y.sum((1, 2)) + 1)
    return F.binary_cross_entropy_with_logits(lo, y) + dice.mean()


if __name__ == '__main__':
    torch.manual_seed(FOLD)
    dl = torch.utils.data.DataLoader(DS(D, FOLD), batch_size=BS, num_workers=6, persistent_workers=True, prefetch_factor=4)
    net = UNet().cuda(); opt = torch.optim.AdamW(net.parameters(), 2e-3, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, 2e-3, total_steps=EPOCHS * STEPS)
    scaler = torch.amp.GradScaler()
    it = iter(dl); t0 = time.time()
    for ep in range(EPOCHS):
        net.train(); tot = 0
        for s in range(STEPS):
            x, y = next(it); x, y = x.cuda(non_blocking=True), y.cuda(non_blocking=True)
            with torch.autocast('cuda', dtype=torch.bfloat16): lo = net(x)
            l = loss_fn(lo.float(), y)
            opt.zero_grad(set_to_none=True); l.backward(); opt.step(); sched.step(); tot += l.item()
        torch.save(net.state_dict(), OUT / 'model.pt')
        print(f'epoch {ep} loss {tot / STEPS:.4f} {time.time() - t0:.0f}s', flush=True)
    print('DONE', flush=True)
    os._exit(0)
