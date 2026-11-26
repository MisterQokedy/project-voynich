import json, random, re, math, collections, unicodedata, numpy as np
exec(open('./work/timm_rules/code_endrule/confirm.py').read().split("\nVT = [VLINES[i]")[0])
def ed(a, b):
    a, b = gg(a), gg(b); d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        p, d[0] = d[0], i
        for j, y in enumerate(b, 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (x != y))
    return d[-1]
def etype(a, b):
    if a == b: return 'S'
    A, B = gg(a), gg(b)
    if ed(a, b) >= 2: return '2'
    if len(A) == len(B):
        i = [k for k in range(len(A)) if A[k] != B[k]][0]
    else:
        S, Lg = (A, B) if len(A) < len(B) else (B, A); i = next((k for k in range(len(S)) if S[k] != Lg[k]), len(S))
        if i >= len(S): i = len(Lg) - 1
    n = max(len(A), len(B))
    return 'F' if i == 0 else 'L' if i >= n - 1 else 'M'
BK = lambda d: 0 if d == 1 else 1 if d <= 3 else 2 if d <= 8 else 3 if d <= 15 else 4
def choices(pages):
    out = []
    for p in pages:
        flat = [w for l in p for w in l]; seq = []
        for t, w in enumerate(flat):
            best = None
            for d in range(1, min(30, t) + 1):
                e = ed(w, flat[t - d])
                if e <= 2 and (best is None or e < best[0]): best = (e, d)
                if e == 0: break
            seq.append('N' if best is None else f'{BK(best[1])}{etype(w, flat[t - best[1]])}')
        if seq: out.append(seq)
    return out
SYM = ['N'] + [f'{b}{e}' for b in range(5) for e in 'SFLM2']; SI = {s: i for i, s in enumerate(SYM)}
def cmat(seqs, idx=SI):
    C = np.zeros((len(idx), len(idx)))
    for s in seqs:
        for a, b in zip(s, s[1:]): C[idx[a], idx[b]] += 1
    return C
# language bigram models
def letters(t): t = unicodedata.normalize('NFD', t.lower()); return [c for c in t if 'a' <= c <= 'z']
C = json.load(open('./work/decipherment_harness/corpora.json'))
MH = json.load(open('./work/regional/mhg_pages.json')); HT = json.load(open('./work/regional/htr_pages.json'))
LANGS = {'latin': letters(' '.join(C['latin'])), 'mhg': letters(' '.join(w for k in ('tauler', 'nikolaus', 'freising_law', 'oberalt_evang', 'engelthal') for p in MH[k] for l in p for w in l)),
         'italian': letters(' '.join(C['italian'])), 'occitan': letters(' '.join(w for p in HT['occitan'] for l in p for w in l))}
AL = [chr(c) for c in range(97, 123)]; AI = {c: i for i, c in enumerate(AL)}
def lm(L):
    B = np.full((26, 26), 0.5)
    for a, b in zip(L, L[1:]): B[AI[a], AI[b]] += 1
    return np.log2(B / B.sum(1, keepdims=True))
LM = {k: lm(v) for k, v in LANGS.items()}
def ll(Cm, m, LP): return (Cm * LP[np.ix_(m, m)]).sum() / Cm.sum()
def anneal(Cm, LP, seed, it=40000):
    r = np.random.default_rng(seed); best = None
    for rs in range(5):
        m = r.integers(0, 26, Cm.shape[0]); cur = ll(Cm, m, LP); T = 0.05
        for i in range(it):
            j = r.integers(Cm.shape[0]); old = m[j]; m[j] = r.integers(26); v = ll(Cm, m, LP)
            if v >= cur or r.random() < math.exp((v - cur) / T): cur = v
            else: m[j] = old
            T = 0.05 * (1 - i / it) + 1e-4
        if best is None or cur > best[0]: best = (cur, m.copy())
    return best
def structure(seqs, r):
    def H2(ss):
        Cm = cmat(ss); P = Cm / Cm.sum(); pa = P.sum(1); return -(P[P > 0] * np.log2(P[P > 0])).sum() + (pa[pa > 0] * np.log2(pa[pa > 0])).sum()
    return np.mean([H2([r.sample(s, len(s)) for s in seqs]) for _ in range(5)]) - H2(seqs)
def run(name, fit_seqs, test_seqs, langs=LM, nnull=200):
    r = random.Random(11); Cf = cmat(fit_seqs); Ct = cmat(test_seqs); res = {}
    print(f'{name}: symbols FIT {int(Cf.sum())} TEST {int(Ct.sum())}; order structure (bits, shuffle H − H) FIT {structure(fit_seqs, r):.4f} TEST {structure(test_seqs, r):.4f}', flush=True)
    for k, LP in langs.items():
        f, m = anneal(Cf, LP, 1); t = ll(Ct, m, LP)
        null = [ll(cmat([r.sample(s, len(s)) for s in test_seqs]), m, LP) for _ in range(nnull)]
        res[k] = dict(fit=f, test=t, p99=float(np.percentile(null, 99)), null_mean=float(np.mean(null)))
        print(f'   {k:8} FIT LL {f:.4f}  TEST LL {t:.4f}  shuffle mean {np.mean(null):.4f} p99 {np.percentile(null, 99):.4f}  {"> p99" if t > np.percentile(null, 99) else "not > p99"}  map: ' + ''.join(AL[x] for x in m), flush=True)
    return res
out = {}
out['voynich'] = run('Voynich', choices(FIp), choices([VLINES[i] for i in TI]))
P = json.load(open('./work/timm_rules/timm_rules_pages3_1.json'))
for s in list(P)[:3]:
    TP = rule(P[s], 0.6, random.Random(int(s))); out[f'timm{s}'] = run(f'Timm+rules seed {s}', choices([TP[i] for i in FI]), choices([TP[i] for i in TI]))
# positive calibration: homophonic Latin, 26 symbols
rr = random.Random(5); key = {c: [] for c in AL}; syms = list(range(26)); rr.shuffle(syms)
order = sorted(AL, key=lambda c: -LANGS['latin'].count(c))
for i, s in enumerate(syms): key[order[i % len(order)]].append(s) if i < 26 else None
LT = [c for c in letters(' '.join(C['latin'][-40000:]))]; LT = [c for c in LT if key[c]]
enc = [str(rr.choice(key[c])) for c in LT]; IDX = {str(i): i for i in range(26)}
segs = [enc[i:i + 150] for i in range(0, len(enc), 150)]; h = len(segs) // 2
def run_cal():
    r = random.Random(12); Cf = cmat(segs[:h], IDX); Ct = cmat(segs[h:], IDX); LP = LM['latin']; f, m = anneal(Cf, LP, 1); t = ll(Ct, m, LP)
    null = [ll(cmat([r.sample(s, len(s)) for s in segs[h:]], IDX), m, LP) for _ in range(200)]
    print(f'CALIBRATION homophonic Latin -> latin model: FIT {f:.4f} TEST {t:.4f} shuffle p99 {np.percentile(null, 99):.4f} -> {"PASS" if t > np.percentile(null, 99) else "FAIL"}', flush=True)
    return dict(test=t, p99=float(np.percentile(null, 99)))
out['calibration'] = run_cal()
for k in LM:
    v = out['voynich'][k]; tm = max(out[f'timm{s}'][k]['test'] for s in list(P)[:3])
    print(f'VERDICT {k}: Voynich TEST {v["test"]:.4f} vs shuffle p99 {v["p99"]:.4f}, best Timm control {tm:.4f} -> {"PASS" if v["test"] > v["p99"] and v["test"] > tm and out["calibration"]["test"] > out["calibration"]["p99"] else "FAIL"}')
json.dump(out, open('./work/choice_decode/cd.json', 'w'), indent=1, default=float)
