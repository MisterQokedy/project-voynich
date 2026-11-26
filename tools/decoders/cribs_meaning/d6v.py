# D6-V: try to read a text through key G at 1 bit per word (fixed-length 5-bit letter code), with calibration first. See ../PREREG.md
import sys, json, random, math, collections, numpy as np
ARGV = list(sys.argv)
import os; LAMBDA = float(os.environ.get('D6V_KL', '0'))  # exploratory v2: penalty on decoded letter-frequency mismatch
exec(open('./work/meaning_procedure/code/d6.py').read().split("if __name__ == '__main__':")[0])
SYM = ALPHA; NS = 27
def lm4(text, k=0.1):
    global UNI; UNI = np.bincount([SYM.index(c) for c in text], minlength=NS) / len(text) + 1e-6
    ids = np.array([SYM.index(c) for c in text]); T = np.zeros((NS,) * 4); np.add.at(T, (ids[:-3], ids[1:-2], ids[2:-1], ids[3:]), 1)
    T += k; T /= T.sum(-1, keepdims=True); return np.log2(T)
def cells_of(pages):
    seq = [(gg(w)[0], gg(w)[-1]) for p in pages for l in p for w in l[:-1]]; return seq
class Dec:
    def __init__(self, LM, seq_fit, rng):
        self.LM = LM; self.rng = rng; cs = sorted(set(seq_fit)); self.ci = {c: i for i, c in enumerate(cs)}
        self.s = np.array([self.ci[c] for c in seq_fit]); self.nc = len(cs); self.freq = np.bincount(self.s, minlength=self.nc)
    def decode(self, s, T, L, o):
        bits = T[s]; n = (len(bits) - o) // 5; g = bits[o:o + 5 * n].reshape(n, 5) @ np.array([16, 8, 4, 2, 1]); return L[g]
    def score(self, ids):
        nul = ids == NS; x = np.where(nul, 26, ids)
        lp = self.LM[x[:-3], x[1:-2], x[2:-1], x[3:]]; lp = np.where(nul[3:] | nul[:-3] | nul[1:-2] | nul[2:-1], -12.0, lp); sc = lp.mean()
        if LAMBDA:
            q = np.bincount(x, minlength=NS) / len(x) + 1e-6; sc -= LAMBDA * float((q * np.log2(q / UNI)).sum())
        return sc
    def anneal(self, moves=300000, t0=0.3, t1=0.003):
        r = self.rng; T = np.array([r.randrange(2) for _ in range(self.nc)]); L = np.array(list(range(NS)) + [NS] * 5); r.shuffle(L); o = r.randrange(5)
        cur = self.score(self.decode(self.s, T, L, o)); best = (cur, T.copy(), L.copy(), o); p = self.freq / self.freq.sum()
        for m in range(moves):
            t = t0 * (t1 / t0) ** (m / moves); u = r.random(); T2, L2, o2 = T, L, o
            if u < 0.5: T2 = T.copy(); j = np.random.choice(self.nc, p=p) if r.random() < 0.7 else r.randrange(self.nc); T2[j] ^= 1
            elif u < 0.97: L2 = L.copy(); a, b = r.randrange(32), r.randrange(32); L2[a], L2[b] = L2[b], L2[a]
            else: o2 = r.randrange(5)
            sc = self.score(self.decode(self.s, T2, L2, o2))
            if sc >= cur or r.random() < math.exp((sc - cur) / t): T, L, o, cur = T2, L2, o2, sc
            if cur > best[0]: best = (cur, T.copy(), L.copy(), o)
        return best
    def apply(self, seq, T, L, o):
        s = np.array([self.ci.get(c, -1) for c in seq]); Tx = np.append(T, 0); s = np.where(s < 0, self.nc, s); return self.decode(s, Tx, L, o)
def txt(ids): return ''.join(SYM[i] if i < NS else '#' for i in ids)
def coverage(t, vocab):
    toks = t.split(' '); good = sum(len(w) for w in toks if len(w) >= 2 and w in vocab); return good / max(1, sum(len(w) for w in toks))
def fit_eval(LM, Ffit, Ftest, vocab, restarts, seed, truthT=None):
    best = None
    for rs in range(restarts):
        d = Dec(LM, Ffit, random.Random(seed + rs)); np.random.seed(seed + rs); b = d.anneal()
        if best is None or b[0] > best[0][0]: best = (b, d)
    (sc, T, L, o), d = best; ids = d.apply(Ftest, T, L, o); t = txt(ids)
    return dict(fit_score=float(sc), test_score=float(d.score(ids)), coverage=coverage(t, vocab), sample=t[:160]), (T, L, o, d)
if __name__ == '__main__':
    mode = ARGV[1]; pname = ARGV[2]; R = int(ARGV[3]) if len(ARGV) > 3 else 8
    txt0 = PLAIN[pname]; cut = int(0.6 * len(txt0)); LM = lm4(txt0[:cut]); vocab = set(txt0[:cut].split())
    rng = random.Random(5); codes = list(range(32)); rng.shuffle(codes); enc = {c: format(codes[i], '05b') for i, c in enumerate(SYM)}; inv = {v: k for k, v in enc.items()}
    bins = keyG(1); OUT = {}
    if mode == 'calib':
        msgF = txt0[:cut][1000:]; msgT = txt0[cut:]
        pf, _, _ = gen_stego(FITSH, P0, 1900, bins, 1, ''.join(enc[c] for c in msgF)); pt, _, used = gen_stego(TESTSH, P0, 900, bins, 1, ''.join(enc[c] for c in msgT))
        g, ok, loss = score_on(pt, REF); print('calibration cipher profile', int(sum(ok.values())), [k for k in ok if not ok[k]], flush=True)
        res, (T, L, o, d) = fit_eval(LM, cells_of(pf), cells_of(pt), vocab, R, 100)
        ids = d.apply(cells_of(pt), T, L, o); dec = txt(ids); truth = msgT[:len(dec)]
        # accuracy up to the frame: compare with the truth at the best of the 5 offsets
        acc = max(sum(a == b for a, b in zip(dec, msgT[s:])) / len(dec) for s in range(0, 3))
        res['acc'] = acc; res['truth_score'] = float(d.score(np.array([SYM.index(c) for c in truth]))); print(json.dumps(res), flush=True); OUT = res
    else:
        S = {}
        S['voynich'] = (FIp, TESTSH)
        r0 = random.Random(5); W = [w for p in TESTSH for l in p for w in l]; r0.shuffle(W); it = iter(W); S['voynich_shuffled'] = (FIp, [[[next(it) for _ in l] for l in p] for p in TESTSH])
        Tm = json.load(open('./work/timm_rules/timm_rules_pages.json'))['21']; S['timm_21'] = ([Tm[i] for i in FI], [Tm[i] for i in TI])
        Pc = json.load(open('./work/meaning_procedure/cache/proc_controls.json'))
        S['pure_proc_900'] = (Pc['pure_proc_900']['FIT'], Pc['pure_proc_900']['TEST']); S['hybrid_full_900'] = (Pc['hybrid_full_900']['FIT'], Pc['hybrid_full_900']['TEST'])
        for name, (F, T_) in S.items():
            F = [[l for l in p if l] for p in F]; T_ = [[l for l in p if l] for p in T_]
            res, _ = fit_eval(LM, cells_of(F), cells_of(T_), vocab, R, 200); OUT[name] = res; print(name, json.dumps(res), flush=True)
    json.dump(OUT, open(f'./work/meaning_procedure/d6v_{mode}_{pname}' + (f'_kl{LAMBDA:g}' if LAMBDA else '') + '.json', 'w'), indent=1)
