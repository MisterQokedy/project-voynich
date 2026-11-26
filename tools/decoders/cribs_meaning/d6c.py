# D6-C: herbal-page plant names as a crib for the grid word-choice channel. See ../PREREG3.md
import sys, json, random, math, numpy as np
ARGV = list(sys.argv)
exec(open('./work/meaning_procedure/code/d6.py').read().split("if __name__ == '__main__':")[0])
META = json.load(open('./work/manuscript_wide/pages2.json'))
ID = {k: v for k, v in json.load(open('./work/cribs/plant_ids.json')).items() if not k.startswith('_')}
REAL = dict(ID)
SYM = ALPHA; NS = 27; W5 = np.array([16, 8, 4, 2, 1])
def name_of(i): return ID.get('f' + META[i].get('page', ''))
def crib(nm): return (nm + ' ')[:8]
rng0 = random.Random(5); _c = list(range(32)); rng0.shuffle(_c); ENC = {c: format(_c[i], '05b') for i, c in enumerate(SYM)}
def slots(p): return sum(max(len(l) - 1, 0) for l in p if l)
def planted(shapes, idxs, seed, latin):
    bits = []; pos = 0
    for p, i in zip(shapes, idxs):
        n = slots(p); nm = name_of(i) if META[i].get('I') == 'H' else None
        msg = (nm + ' ' if nm else '') + latin[pos:pos + n]; pos += n
        b = ''.join(ENC[c] for c in msg)[:n]; bits.append(b + '0' * (n - len(b)))
    pages, _, _ = gen_stego(shapes, P0, seed, keyG(1), 1, ''.join(bits)); return pages
def page_cells(pages, idxs):
    out = []
    for p, i in zip(pages, idxs):
        nm = name_of(i)
        if not nm or META[i].get('I') != 'H': continue
        cr = crib(nm); seq = [(gg(w)[0], gg(w)[-1]) for l in p if l for w in l[:-1]][:5 * len(cr)]
        k = len(seq) // 5; 
        if k: out.append((seq[:5 * k], cr[:k]))
    return out
class CribDec:
    def __init__(self, data, rng):
        cs = sorted({c for s, _ in data for c in s}); self.ci = {c: j for j, c in enumerate(cs)}; self.nc = len(cs); self.rng = rng
        self.mx = max(len(t) for _, t in data); n = len(data)
        self.C = np.full((n, self.mx, 5), self.nc); self.Y = np.full((n, self.mx), -1)
        for a, (s, t) in enumerate(data):
            for k in range(len(t)):
                self.C[a, k] = [self.ci[c] for c in s[5 * k:5 * k + 5]]; self.Y[a, k] = SYM.index(t[k])
        self.freq = np.bincount(self.C[self.C < self.nc], minlength=self.nc).astype(float)
    def score(self, T, L, C=None, Y=None):
        C = self.C if C is None else C; Y = self.Y if Y is None else Y; Tx = np.append(T, 0); g = Tx[C] @ W5; return int(((L[g] == Y) & (Y >= 0)).sum())
    def fit(self, moves=100000, t0=2.0, t1=0.05):
        r = self.rng; T = np.array([r.randrange(2) for _ in range(self.nc)]); L = np.array(list(range(NS)) + [NS] * 5); r.shuffle(L)
        cur = self.score(T, L); best = (cur, T.copy(), L.copy())
        for m in range(moves):
            t = t0 * (t1 / t0) ** (m / moves)
            if r.random() < 0.5: T2 = T.copy(); j = r.randrange(self.nc); T2[j] ^= 1; L2 = L
            else: L2 = L.copy(); a, b = r.randrange(32), r.randrange(32); L2[a], L2[b] = L2[b], L2[a]; T2 = T
            sc = self.score(T2, L2)
            if sc >= cur or r.random() < math.exp((sc - cur) / t): T, L, cur = T2, L2, sc
            if cur > best[0]: best = (cur, T.copy(), L.copy())
        return best
    def encode_other(self, data):
        n = len(data); mx = max(len(t) for _, t in data); C = np.full((n, mx, 5), self.nc); Y = np.full((n, mx), -1)
        for a, (s, t) in enumerate(data):
            for k in range(len(t)):
                C[a, k] = [self.ci.get(c, self.nc) for c in s[5 * k:5 * k + 5]]; Y[a, k] = SYM.index(t[k])
        return C, Y
def run(Fp, Tp, restarts=8, seed=0):
    dF = page_cells(Fp, FI); dT = page_cells(Tp, TI); best = None
    for rs in range(restarts):
        d = CribDec(dF, random.Random(seed + rs)); b = d.fit()
        if best is None or b[0] > best[0][0]: best = (b, d)
    (sc, T, L), d = best; C, Y = d.encode_other(dT); n = int((Y >= 0).sum())
    return dict(fit_rate=sc / int((d.Y >= 0).sum()), test_rate=d.score(T, L, C, Y) / n, n_test_letters=n, n_fit_pages=len(dF), n_test_pages=len(dT))
def shuffled_names(seed):
    # shuffle names only among the herbal pages that carry one (so every crib page keeps a name)
    herb = {'f' + m.get('page', '') for m in META if m.get('I') == 'H'}
    r = random.Random(seed); keys = [k for k in REAL if k in herb]; vals = [REAL[k] for k in keys]; r.shuffle(vals); d = dict(REAL); d.update(zip(keys, vals)); return d
if __name__ == '__main__':
    mode = ARGV[1]; latin = PLAIN['latin_pliny_herbal']; OUT = {}
    if mode == 'calib':
        Fp = planted(FITSH, FI, 1900, latin); Tp = planted(TESTSH, TI, 900, latin[200000 // 2:])
        g, ok, loss = score_on(Tp, REF); print('planted cipher profile', int(sum(ok.values())), flush=True)
        S = {'planted': (Fp, Tp)}
    else:
        S = {'voynich': (FIp, TESTSH)}
        Tm = json.load(open('./work/timm_rules/timm_rules_pages.json'))['21']; S['timm_21'] = ([Tm[i] for i in FI], [Tm[i] for i in TI])
        Pc = json.load(open('./work/meaning_procedure/cache/proc_controls.json')); S['pure_proc_900'] = (Pc['pure_proc_900']['FIT'], Pc['pure_proc_900']['TEST'])
    first = list(S)[0]; real_ID = dict(ID)
    for name, (Fp, Tp) in S.items():
        ID.clear(); ID.update(real_ID); OUT[name] = run(Fp, Tp); print(name, OUT[name], flush=True)
    nulls = []
    Fp, Tp = S[first]
    for s in range(20):
        ID.clear(); ID.update(shuffled_names(100 + s)); nulls.append(run(Fp, Tp, seed=1000 + s)['test_rate'])
    ID.clear(); ID.update(real_ID)
    OUT['shuffled_names'] = dict(rates=nulls, p99=float(np.percentile(nulls, 99)), mean=float(np.mean(nulls)))
    print('shuffled-name null on', first, OUT['shuffled_names'], flush=True)
    json.dump(OUT, open(f'./work/meaning_procedure/d6c_{mode}.json', 'w'), indent=1)
