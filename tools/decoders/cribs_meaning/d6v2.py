# D6-V2: decoder for the grid channel (1 bit/word, 5-bit letter code) that must recover a planted message first. See ../PREREG2.md
import sys, json, random, math, collections, numpy as np
ARGV = list(sys.argv)
exec(open('./work/meaning_procedure/code/d6v.py').read().split("\nif __name__ == '__main__':")[0])
W5 = np.array([16, 8, 4, 2, 1])
class Dec2:
    def __init__(self, LM, uni, seq, rng, vocab=None, word_w=0.0):
        self.LM = LM; self.rng = rng; cs = sorted(set(seq)); self.ci = {c: i for i, c in enumerate(cs)}; self.nc = len(cs)
        self.s = np.array([self.ci[c] for c in seq]); self.freq = np.bincount(self.s, minlength=self.nc).astype(float)
        self.rank_letters = np.argsort(-uni[:NS]); self.vocab = vocab; self.word_w = word_w
    def codes(self, s, T, o):
        b = T[s]; n = (len(b) - o) // 5; return b[o:o + 5 * n].reshape(n, 5) @ W5
    def rankL(self, g):
        c = np.bincount(g, minlength=32); order = np.argsort(-c, kind='stable'); L = np.full(32, NS); L[order[:NS]] = self.rank_letters; return L
    def lmscore(self, ids):
        nul = ids == NS; x = np.where(nul, 26, ids); lp = self.LM[x[:-3], x[1:-2], x[2:-1], x[3:]]
        lp = np.where(nul[3:] | nul[:-3] | nul[1:-2] | nul[2:-1], -12.0, lp); sc = float(lp.mean())
        if self.word_w: sc += self.word_w * coverage3(txt(ids), self.vocab)
        return sc
    def evalT(self, T, L=None):
        best = None
        for o in range(5):
            g = self.codes(self.s, T, o); LL = self.rankL(g) if L is None else L; sc = self.lmscore(LL[g])
            if best is None or sc > best[0]: best = (sc, o, LL)
        return best
    def init_balanced(self):
        idx = list(range(self.nc)); self.rng.shuffle(idx); idx.sort(key=lambda i: -self.freq[i]); m = [0.0, 0.0]; T = np.zeros(self.nc, int)
        for i in idx:
            j = 0 if m[0] <= m[1] else 1
            if self.rng.random() < 0.3: j = 1 - j
            T[i] = j; m[j] += self.freq[i]
        return T
    def run(self, moves, attempt, t0=0.15, t1=0.002):
        r = self.rng; T = self.init_balanced(); cur, o, L = self.evalT(T); best = (cur, T.copy(), o, L)
        p = self.freq / self.freq.sum()
        for m in range(moves):
            t = t0 * (t1 / t0) ** (m / moves); ones = np.flatnonzero(T == 1); zeros = np.flatnonzero(T == 0)
            if len(ones) == 0 or len(zeros) == 0: break
            i = ones[np.searchsorted(np.cumsum(p[ones]) / p[ones].sum(), r.random())] if r.random() < 0.7 else ones[r.randrange(len(ones))]
            j = zeros[np.searchsorted(np.cumsum(p[zeros]) / p[zeros].sum(), r.random())] if r.random() < 0.7 else zeros[r.randrange(len(zeros))]
            T2 = T.copy(); T2[i], T2[j] = 0, 1; sc, o2, L2 = self.evalT(T2)
            if sc >= cur or r.random() < math.exp((sc - cur) / t): T, cur, o, L = T2, sc, o2, L2
            if cur > best[0]: best = (cur, T.copy(), o, L)
        cur, T, o, L = best
        if attempt >= 2:
            improved = True
            while improved:
                improved = False
                for c in np.argsort(-self.freq):
                    T2 = T.copy(); T2[c] ^= 1; sc, o2, L2 = self.evalT(T2)
                    if sc > cur + 1e-9: T, cur, o, L = T2, sc, o2, L2; improved = True
        # L refinement by swaps at fixed T and offset
        g = self.codes(self.s, T, o)
        for m in range(20000):
            a, b = r.randrange(32), r.randrange(32)
            if L[a] == L[b]: continue
            L2 = L.copy(); L2[a], L2[b] = L2[b], L2[a]; sc = self.lmscore(L2[g])
            if sc > cur: L, cur = L2, sc
        return cur, T, o, L
    def apply(self, seq, T, o, L):
        s = np.array([self.ci.get(c, -1) for c in seq]); Tx = np.append(T, 0); s = np.where(s < 0, self.nc, s); return L[self.codes(s, Tx, o)]
def coverage3(t, vocab):
    toks = t.split(' '); return sum(len(w) for w in toks if len(w) >= 3 and w in vocab) / max(1, sum(len(w) for w in toks))
def fit_apply(LM, uni, Ffit, Ftest, vocab, attempt, restarts=8, moves=150000, seed=0):
    best = None
    for rs in range(restarts):
        d = Dec2(LM, uni, Ffit, random.Random(seed + rs), vocab, 0.5 if attempt >= 3 else 0.0); b = d.run(moves, attempt)
        if best is None or b[0] > best[0][0]: best = (b, d)
    (sc, T, o, L), d = best; ids = d.apply(Ftest, T, o, L); t = txt(ids)
    d.word_w = 0.0; ts = d.lmscore(ids)
    return dict(fit_score=sc, test_score=ts, coverage=coverage(t, vocab), coverage3=coverage3(t, vocab), sample=t[:160]), t
def lang_setup(pname):
    t0 = PLAIN[pname]; cut = int(0.6 * len(t0)); LM = lm4(t0[:cut]); uni = np.bincount([SYM.index(c) for c in t0[:cut]], minlength=NS) / cut
    return t0, cut, LM, uni, set(t0[:cut].split())
def cipher(pname):
    import os
    f = f'./work/meaning_procedure/cache/d6v_cipher_{pname}.json'
    if os.path.exists(f): return json.load(open(f))
    t0, cut, LM, uni, vocab = lang_setup(pname)
    rng = random.Random(5); codes = list(range(32)); rng.shuffle(codes); enc = {c: format(codes[i], '05b') for i, c in enumerate(SYM)}; bins = keyG(1)
    msgF = t0[:cut][1000:]; msgT = t0[cut:]
    pf, _, _ = gen_stego(FITSH, P0, 1900, bins, 1, ''.join(enc[c] for c in msgF)); pt, _, _ = gen_stego(TESTSH, P0, 900, bins, 1, ''.join(enc[c] for c in msgT))
    D = dict(FIT=pf, TEST=pt, msgT=msgT); json.dump(D, open(f, 'w')); return D
if __name__ == '__main__':
    mode, pname, attempt = ARGV[1], ARGV[2], int(ARGV[3]); t0, cut, LM, uni, vocab = lang_setup(pname)
    if mode == 'calib':
        D = cipher(pname); res, dec = fit_apply(LM, uni, cells_of(D['FIT']), cells_of(D['TEST']), vocab, attempt)
        res['acc'] = sum(a == b for a, b in zip(dec, D['msgT'])) / len(dec); res['truth'] = D['msgT'][:100]; print(json.dumps(res), flush=True)
        json.dump(res, open(f'./work/meaning_procedure/d6v2_calib_{pname}_a{attempt}.json', 'w'), indent=1)
    else:
        S = {'voynich': (FIp, TESTSH)}
        r0 = random.Random(5); W = [w for p in TESTSH for l in p for w in l]; r0.shuffle(W); it = iter(W); S['voynich_shuffled'] = (FIp, [[[next(it) for _ in l] for l in p] for p in TESTSH])
        Tm = json.load(open('./work/timm_rules/timm_rules_pages.json'))['21']; S['timm_21'] = ([Tm[i] for i in FI], [Tm[i] for i in TI])
        Pc = json.load(open('./work/meaning_procedure/cache/proc_controls.json'))
        S['pure_proc_900'] = (Pc['pure_proc_900']['FIT'], Pc['pure_proc_900']['TEST']); S['hybrid_full_900'] = (Pc['hybrid_full_900']['FIT'], Pc['hybrid_full_900']['TEST'])
        other = {'latin_pliny_herbal': 'mhg_megenberg_herbs', 'mhg_megenberg_herbs': 'italian_dante', 'italian_dante': 'latin_pliny_herbal'}[pname]
        Dw = cipher(other); S['wrong_language_cipher'] = (Dw['FIT'], Dw['TEST'])
        OUT = {}
        for name, (F, T_) in S.items():
            F = [[l for l in p if l] for p in F]; T_ = [[l for l in p if l] for p in T_]
            res, _ = fit_apply(LM, uni, cells_of(F), cells_of(T_), vocab, attempt, seed=200); OUT[name] = res; print(name, json.dumps(res), flush=True)
            json.dump(OUT, open(f'./work/meaning_procedure/d6v2_voynich_{pname}_a{attempt}.json', 'w'), indent=1)
