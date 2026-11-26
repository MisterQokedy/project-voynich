# D6-V2 addendum attempt 4 (post hoc, written after attempts 1-3 failed; see ../D6V2_CALIB_LOG.md):
# back-off LM + letter-frequency penalty, joint annealing over balanced T swaps and L swaps.
import sys, json, random, math, numpy as np
ARGV = list(sys.argv)
exec(open('./work/meaning_procedure/code/d6v2.py').read().split("\nif __name__ == '__main__':")[0])
exec(open('./work/meaning_procedure/code/lmbo.py').read())
class Dec4(Dec2):
    def lmscore(self, ids):
        sc = Dec2.lmscore(self, ids); x = ids[ids < NS]
        q = np.bincount(x, minlength=NS) / max(len(x), 1) + 1e-6; return sc - 1.0 * float((q * np.log2(q / self.uni)).sum())
    def run(self, moves, attempt=4, t0=0.3, t1=0.002):
        r = self.rng; T = self.init_balanced(); cur, o, L = self.evalT(T); best = (cur, T.copy(), o, L.copy()); p = self.freq / self.freq.sum()
        for m in range(moves):
            t = t0 * (t1 / t0) ** (m / moves); u = r.random(); T2, L2, o2 = T, L, o
            if u < 0.45:
                ones = np.flatnonzero(T == 1); zeros = np.flatnonzero(T == 0)
                i = ones[np.searchsorted(np.cumsum(p[ones]) / p[ones].sum(), r.random())]; j = zeros[np.searchsorted(np.cumsum(p[zeros]) / p[zeros].sum(), r.random())]
                T2 = T.copy(); T2[i], T2[j] = 0, 1
            elif u < 0.98: L2 = L.copy(); a, b = r.randrange(32), r.randrange(32); L2[a], L2[b] = L2[b], L2[a]
            else: o2 = r.randrange(5)
            sc = self.lmscore(L2[self.codes(self.s, T2, o2)])
            if sc >= cur or r.random() < math.exp((sc - cur) / t): T, L, o, cur = T2, L2, o2, sc
            if cur > best[0]: best = (cur, T.copy(), o, L.copy())
        return best
def fit_apply4(LMb, uni, Ffit, Ftest, vocab, restarts=8, moves=300000, seed=0):
    best = None
    for rs in range(restarts):
        d = Dec4(LMb, uni, Ffit, random.Random(seed + rs)); d.uni = uni[:NS] + 1e-6; b = d.run(moves)
        if best is None or b[0] > best[0][0]: best = (b, d)
    (sc, T, o, L), d = best; ids = d.apply(Ftest, T, o, L); t = txt(ids)
    return dict(fit_score=sc, test_score=Dec2.lmscore(d, ids), coverage=coverage(t, vocab), coverage3=coverage3(t, vocab), sample=t[:160]), t
if __name__ == '__main__':
    mode, pname = ARGV[1], ARGV[2]; t0, cut, LM, uni, vocab = lang_setup(pname); LMb = lm4_backoff(t0[:cut], SYM)
    if mode == 'calib':
        D = cipher(pname); res, dec = fit_apply4(LMb, uni, cells_of(D['FIT']), cells_of(D['TEST']), vocab)
        res['acc'] = sum(a == b for a, b in zip(dec, D['msgT'])) / len(dec); print(json.dumps(res), flush=True)
        json.dump(res, open(f'./work/meaning_procedure/d6v2_calib_{pname}_a4.json', 'w'), indent=1)
