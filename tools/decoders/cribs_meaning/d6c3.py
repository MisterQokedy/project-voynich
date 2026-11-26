# D6-C3: zodiac ring labels as a word-choice crib (month names / sign names), and a 2-bit plant crib. See ../PREREG5.md
import sys, json, random, math, re, numpy as np
ARGV = list(sys.argv)
exec(open('./work/meaning_procedure/code/d6c2.py').read().split("\nif __name__ == '__main__':")[0])
# ---- zodiac labels (as in cribs/code/c1_zodiac.py)
SIGNS = {'Pisces': ['f70v2'], 'Aries': ['f70v1', 'f71r'], 'Taurus': ['f71v', 'f72r1'], 'Gemini': ['f72r2'], 'Cancer': ['f72r3'],
         'Leo': ['f72v3'], 'Virgo': ['f72v2'], 'Libra': ['f72v1'], 'Scorpio': ['f73r'], 'Sagitt': ['f73v']}
MONTH = dict(zip(SIGNS, ['mars', 'abril', 'may', 'yong', 'jollet', 'augst', 'setembre', 'octembre', 'novembre', 'desembre']))
LATIN = dict(zip(SIGNS, ['pisces', 'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius']))
def zclean(w):
    w = re.sub(r'\[([^:\]]*):[^\]]*\]', r'\1', w); w = re.sub(r'\{[^}]*\}', '', w); w = re.sub(r'@\d+;', '', w); return re.sub(r'[^a-z]', '', w)
RINGS = {}
for line in open('./work/labels/ZL3b-n.txt', encoding='latin-1'):
    m = re.match(r'<(f7[0-3][rv]\d?)\.(\d+),(.)(\w\w)>\s*(.*)', line)
    if not m: continue
    pg, n, mk, ty, tx = m.groups(); tx = re.sub(r'<[^>]*>', '', tx)
    if ty != 'Lz': continue
    w = zclean(tx.split('.')[0].split(',')[0])
    if w: RINGS.setdefault(pg, []).append(w)
ZLAB = {s: [w for pg in SIGNS[s] for w in RINGS.get(pg, [])] for s in SIGNS}
FOLDS = [['Pisces', 'Taurus', 'Cancer', 'Virgo', 'Scorpio'], ['Aries', 'Gemini', 'Leo', 'Libra', 'Sagitt']]
def zcrib(nm): return (nm + ' ')[:6]
# ---- generic b-bit crib decoder
class GDec:
    def __init__(self, data, rng, b, fixed):
        self.b = b; self.fixed = fixed; self.rng = rng; cs = sorted({c for s, _ in data for c in s}, key=str); self.ci = {c: j for j, c in enumerate(cs)}; self.nc = len(cs)
        self.prep(data, own=True)
    def prep(self, data, own=False):
        n = len(data); mx = max(len(t) for _, t in data); nw = math.ceil(5 * mx / self.b)
        S = np.full((n, nw), self.nc); Y = np.full((n, mx), -1)
        for a, (s, t) in enumerate(data):
            k = len(t); ids = [self.ci.get(c, self.nc) for c in s[:math.ceil(5 * k / self.b)]]; S[a, :len(ids)] = ids; Y[a, :k] = [SYM.index(c) for c in t]
        if own: self.S, self.Y = S, Y
        return S, Y
    def score(self, T, L, S=None, Y=None):
        S = self.S if S is None else S; Y = self.Y if Y is None else Y; Tx = np.append(T, 0)
        bits = ((Tx[S][..., None] >> np.arange(self.b - 1, -1, -1)) & 1).reshape(S.shape[0], -1)
        mx = Y.shape[1]; g = bits[:, :5 * mx].reshape(S.shape[0], mx, 5) @ W5; return int(((L[g] == Y) & (Y >= 0)).sum())
    def fit(self, moves=60000, t0=2.0, t1=0.05):
        r = self.rng
        T = np.array([int(c) for c in sorted(self.ci, key=lambda c: self.ci[c])]) if self.fixed else np.array([r.randrange(1 << self.b) for _ in range(self.nc)])
        L = np.array(list(range(NS)) + [NS] * 5); r.shuffle(L); cur = self.score(T, L); best = (cur, T.copy(), L.copy())
        for m in range(moves):
            t = t0 * (t1 / t0) ** (m / moves); T2, L2 = T, L
            if not self.fixed and r.random() < 0.5: T2 = T.copy(); T2[r.randrange(self.nc)] = r.randrange(1 << self.b)
            else: L2 = L.copy(); a, b_ = r.randrange(32), r.randrange(32); L2[a], L2[b_] = L2[b_], L2[a]
            sc = self.score(T2, L2)
            if sc >= cur or r.random() < math.exp((sc - cur) / t): T, L, cur = T2, L2, sc
            if cur > best[0]: best = (cur, T.copy(), L.copy())
        return best
def fit_score(dF, dT, b, fixed, restarts=8, seed=0):
    best = None
    for rs in range(restarts):
        d = GDec(dF, random.Random(seed + rs), b, fixed); x = d.fit()
        if best is None or x[0] > best[0][0]: best = (x, d)
    (sc, T, L), d = best; S, Y = d.prep(dT); return d.score(T, L, S, Y), int((Y >= 0).sum()), sc / int((d.Y >= 0).sum())
def zdata(labs, ch, cribs, signs):
    f = SYMF[ch]; out = []
    for s in signs:
        ws = labs[s][:-1]; cr = zcrib(cribs[s]); k = min(len(cr), len(ws) // 5)
        if k: out.append(([f(w) for w in ws[:5 * k]], cr[:k]))
    return out
def zrun(labs, ch, cribs, seed=0):
    hit = tot = 0
    for fi in (0, 1):
        dF = zdata(labs, ch, cribs, FOLDS[fi]); dT = zdata(labs, ch, cribs, FOLDS[1 - fi]); h, n, _ = fit_score(dF, dT, 1, ch in FIXED, seed=seed); hit += h; tot += n
    return hit / tot
def zplant(ch, cribs, seed, prm=None, plant=True):
    bins = make_bins(ch); latin = PLAIN['latin_pliny_herbal']; out = {}; pos = 0
    for j, s in enumerate(SIGNS):
        n = len(ZLAB[s]); shapes = [[[0] * n]]
        if plant:
            b = ''.join(ENC[c] for c in zcrib(cribs[s])) + ''.join(ENC[c] for c in latin[pos:pos + n]); pos += n
            pages, _, _ = gen_stego(shapes, prm or P0, seed + j, bins, 1, b[:n - 1])
        else: pages, _, _ = gen_stego(shapes, prm or P0, seed + j, bins, 0, '')
        out[s] = pages[0][0]
    return out
def zshuf(cribs, s):
    r = random.Random(s); ks = list(cribs); vs = [cribs[k] for k in ks]; r.shuffle(vs); return dict(zip(ks, vs))
if __name__ == '__main__':
    mode = ARGV[1]
    if mode == 'zodiac':
        ch, cs = ARGV[2], ARGV[3]; cribs = MONTH if cs == 'month' else LATIN; OUT = dict(channel=ch, crib=cs, n_labels={s: len(v) for s, v in ZLAB.items()})
        P = zplant(ch, cribs, 900); OUT['calib'] = zrun(P, ch, cribs); nl = [zrun(P, ch, zshuf(cribs, 100 + i), seed=50 + i) for i in range(20)]
        OUT['calib_null'] = dict(p99=float(np.percentile(nl, 99)), max=max(nl), mean=float(np.mean(nl))); OUT['gate'] = bool(OUT['calib'] >= 0.5 and OUT['calib'] > OUT['calib_null']['p99'])
        print(ch, cs, 'calib', round(OUT['calib'], 3), OUT['calib_null'], 'gate', OUT['gate'], flush=True)
        if OUT['gate']:
            OUT['voynich'] = zrun(ZLAB, ch, cribs); nl = [zrun(ZLAB, ch, zshuf(cribs, 100 + i), seed=50 + i) for i in range(20)]
            OUT['voynich_null'] = dict(p99=float(np.percentile(nl, 99)), max=max(nl), mean=float(np.mean(nl)))
            PURE = dict(P0, pw=0.0, alpha=0.0); G = zplant(ch, cribs, 900, PURE, plant=False); OUT['pure_proc'] = zrun(G, ch, cribs)
            OUT['hit'] = bool(OUT['voynich'] > OUT['voynich_null']['p99'] and OUT['voynich'] > OUT['pure_proc'])
            print(ch, cs, 'VOYNICH', round(OUT['voynich'], 3), OUT['voynich_null'], 'pure', round(OUT['pure_proc'], 3), 'hit', OUT['hit'], flush=True)
        json.dump(OUT, open(f'./work/meaning_procedure/d6c3_zodiac_{ch}_{cs}.json', 'w'), indent=1)
    else:   # plant crib, cell channel, 2 bits per word, name at page start
        f = SYMF['cell']; M = collections.Counter(f(w) for p in FIp for l in p for w in l); items = list(M.items()); random.Random(1).shuffle(items); items.sort(key=lambda x: -x[1])
        mass = [0] * 4; TT = {}
        for c, m in items: j = min(range(4), key=lambda i: (mass[i], i)); TT[c] = j; mass[j] += m
        bins = lambda w: TT.get(f(w), 0); latin = PLAIN['latin_pliny_herbal']
        def plant2(shapes, idxs, seed, lat):
            bits = []; pos = 0
            for p, i in zip(shapes, idxs):
                n = 2 * slots(p); nm = name_of(i) if META[i].get('I') == 'H' else None
                msg = (crib(nm) if nm else '') + lat[pos:pos + n]; pos += n; b = ''.join(ENC[c] for c in msg)[:n]; bits.append(b + '0' * (n - len(b)))
            pages, _, _ = gen_stego(shapes, P0, seed, bins, 2, ''.join(bits)); return pages
        def pdata(pages, idxs):
            out = []
            for p, i in zip(pages, idxs):
                nm = name_of(i)
                if not nm or META[i].get('I') != 'H': continue
                cr = crib(nm); ws = [w for l in p if l for w in l[:-1]]; k = min(len(cr), (2 * len(ws)) // 5)
                if k: out.append(([f(w) for w in ws[:math.ceil(5 * k / 2)]], cr[:k]))
            return out
        def prun(Fp, Tp, seed=0):
            h, n, fr = fit_score(pdata(Fp, FI), pdata(Tp, TI), 2, False, seed=seed); return h / n, fr
        OUT = {}
        Fp = plant2(FITSH, FI, 1900, latin); Tp = plant2(TESTSH, TI, 900, latin[100000:]); g, ok, loss = score_on(Tp, REF); OUT['planted_profile'] = int(sum(ok.values()))
        OUT['calib'] = prun(Fp, Tp)[0]; nl = []
        for s in range(20):
            ID.clear(); ID.update(shuffled_names(100 + s)); nl.append(prun(Fp, Tp, seed=1000 + s)[0])
        ID.clear(); ID.update(REAL); OUT['calib_null'] = dict(p99=float(np.percentile(nl, 99)), max=max(nl)); OUT['gate'] = bool(OUT['calib'] >= 0.5 and OUT['calib'] > OUT['calib_null']['p99'])
        print('plant 2-bit calib', OUT, flush=True)
        if OUT['gate']:
            OUT['voynich'], OUT['voynich_fit'] = prun(FIp, TESTSH)
            Tm = json.load(open('./work/timm_rules/timm_rules_pages.json'))['21']; OUT['timm_21'] = prun([Tm[i] for i in FI], [Tm[i] for i in TI])[0]
            Pc = json.load(open('./work/meaning_procedure/cache/proc_controls.json')); OUT['pure_proc_900'] = prun(Pc['pure_proc_900']['FIT'], Pc['pure_proc_900']['TEST'])[0]
            nl = []
            for s in range(20):
                ID.clear(); ID.update(shuffled_names(100 + s)); nl.append(prun(FIp, TESTSH, seed=1000 + s)[0])
            ID.clear(); ID.update(REAL); OUT['voynich_null'] = dict(p99=float(np.percentile(nl, 99)), max=max(nl))
            OUT['hit'] = bool(OUT['voynich'] > OUT['voynich_null']['p99'] and OUT['voynich'] > OUT['timm_21'] and OUT['voynich'] > OUT['pure_proc_900'])
            print('plant 2-bit VOYNICH', OUT, flush=True)
        json.dump(OUT, open('./work/meaning_procedure/d6c3_plant2bit.json', 'w'), indent=1)
