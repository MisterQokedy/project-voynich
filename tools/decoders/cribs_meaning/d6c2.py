# D6-C2: plant-name crib over 5 channels x 2 placements. See ../PREREG4.md
import sys, json, random, math, numpy as np
ARGV = list(sys.argv)
exec(open('./work/meaning_procedure/code/d6c.py').read().split("\nif __name__ == '__main__':")[0])
GALS = {'k', 't', 'p', 'f', 'ckh', 'cth', 'cph', 'cfh'}
SYMF = {'cell': lambda w: (gg(w)[0], gg(w)[-1]), 'onset': lambda w: gg(w)[0], 'ending': lambda w: gg(w)[-1],
        'parity': lambda w: len(gg(w)) % 2, 'gallows': lambda w: int(any(g in GALS for g in gg(w)))}
FIXED = {'parity', 'gallows'}
def make_bins(ch, seed=1):
    f = SYMF[ch]
    if ch in FIXED: return f
    M = collections.Counter(f(w) for p in FIp for l in p for w in l); items = list(M.items()); random.Random(seed).shuffle(items); items.sort(key=lambda x: -x[1])
    mass = [0, 0]; T = {}
    for c, m in items: j = 0 if mass[0] <= mass[1] else 1; T[c] = j; mass[j] += m
    return lambda w: T.get(f(w), 0)
def planted2(shapes, idxs, seed, latin, bins, place):
    bits = []; pos = 0
    for p, i in zip(shapes, idxs):
        n = slots(p); nm = name_of(i) if META[i].get('I') == 'H' else None
        if nm:
            cr = crib(nm); nb = 5 * len(cr); filler = ''.join(ENC[c] for c in latin[pos:pos + n])[:max(n - nb, 0)]; pos += n
            namebits = ''.join(ENC[c] for c in cr)
            b = (namebits + filler) if place == 'start' else (filler + namebits)
        else:
            b = ''.join(ENC[c] for c in latin[pos:pos + n]); pos += n
        b = b[:n]; bits.append(b + '0' * (n - len(b)))
    pages, _, _ = gen_stego(shapes, P0, seed, bins, 1, ''.join(bits)); return pages
def page_syms(pages, idxs, ch, place):
    f = SYMF[ch]; out = []
    for p, i in zip(pages, idxs):
        nm = name_of(i)
        if not nm or META[i].get('I') != 'H': continue
        cr = crib(nm); ws = [w for l in p if l for w in l[:-1]]; k = min(len(cr), len(ws) // 5)
        if not k: continue
        if place == 'start': seq = ws[:5 * k]; t = cr[:k]
        else:
            # the name occupies the last 5*len(cr) slots; if the page is short, keep the tail that fits
            seq = ws[len(ws) - 5 * len(cr):] if len(ws) >= 5 * len(cr) else ws[len(ws) - 5 * k:]; t = cr[:k] if len(ws) >= 5 * len(cr) else cr[len(cr) - k:]
            seq = seq[:5 * k]; t = t[:k]
        out.append(([f(w) for w in seq], t))
    return out
class CribDec2(CribDec):
    def __init__(self, data, rng, fixed):
        super().__init__(data, rng); self.fixed = fixed
        if fixed: self.T0 = np.array([inv for c, inv in sorted((c, int(c)) for c in self.ci)])  # symbol value = bit
    def fit(self, moves=100000, t0=2.0, t1=0.05):
        if not self.fixed: return super().fit(moves, t0, t1)
        r = self.rng; T = np.array([int(c) for c, j in sorted(self.ci.items(), key=lambda x: x[1])]); L = np.array(list(range(NS)) + [NS] * 5); r.shuffle(L)
        cur = self.score(T, L); best = (cur, T.copy(), L.copy())
        for m in range(moves // 2):
            t = t0 * (t1 / t0) ** (m / (moves // 2)); L2 = L.copy(); a, b = r.randrange(32), r.randrange(32); L2[a], L2[b] = L2[b], L2[a]; sc = self.score(T, L2)
            if sc >= cur or r.random() < math.exp((sc - cur) / t): L, cur = L2, sc
            if cur > best[0]: best = (cur, T.copy(), L.copy())
        return best
def run2(Fp, Tp, ch, place, restarts=8, seed=0):
    dF = page_syms(Fp, FI, ch, place); dT = page_syms(Tp, TI, ch, place); best = None
    for rs in range(restarts):
        d = CribDec2(dF, random.Random(seed + rs), ch in FIXED); b = d.fit()
        if best is None or b[0] > best[0][0]: best = (b, d)
    (sc, T, L), d = best; C, Y = d.encode_other(dT); n = int((Y >= 0).sum())
    return dict(fit_rate=sc / int((d.Y >= 0).sum()), test_rate=d.score(T, L, C, Y) / n, n_test_letters=n)
def nullrates(Fp, Tp, ch, place, k=20):
    out = []
    for s in range(k):
        ID.clear(); ID.update(shuffled_names(100 + s)); out.append(run2(Fp, Tp, ch, place, seed=1000 + s)['test_rate'])
    ID.clear(); ID.update(REAL); return out
if __name__ == '__main__':
    ch, place = ARGV[1], ARGV[2]; latin = PLAIN['latin_pliny_herbal']; bins = make_bins(ch); OUT = dict(channel=ch, placement=place)
    Fp = planted2(FITSH, FI, 1900, latin, bins, place); Tp = planted2(TESTSH, TI, 900, latin[100000:], bins, place)
    g, ok, loss = score_on(Tp, REF); OUT['planted_profile'] = int(sum(ok.values()))
    OUT['calib'] = run2(Fp, Tp, ch, place); nl = nullrates(Fp, Tp, ch, place); OUT['calib_null'] = dict(p99=float(np.percentile(nl, 99)), max=max(nl), mean=float(np.mean(nl)))
    gate = OUT['calib']['test_rate'] >= 0.5 and OUT['calib']['test_rate'] > OUT['calib_null']['p99']; OUT['gate'] = bool(gate)
    print(ch, place, 'planted profile', OUT['planted_profile'], 'calib', OUT['calib'], 'null', OUT['calib_null'], 'gate', gate, flush=True)
    if gate:
        S = {'voynich': (FIp, TESTSH)}
        Tm = json.load(open('./work/timm_rules/timm_rules_pages.json'))['21']; S['timm_21'] = ([Tm[i] for i in FI], [Tm[i] for i in TI])
        Pc = json.load(open('./work/meaning_procedure/cache/proc_controls.json')); S['pure_proc_900'] = (Pc['pure_proc_900']['FIT'], Pc['pure_proc_900']['TEST'])
        for k, (F, T) in S.items(): OUT[k] = run2(F, T, ch, place)
        nl = nullrates(FIp, TESTSH, ch, place); OUT['voynich_null'] = dict(p99=float(np.percentile(nl, 99)), max=max(nl), mean=float(np.mean(nl)))
        v = OUT['voynich']['test_rate']
        hit = v > OUT['voynich_null']['p99'] and v > OUT['timm_21']['test_rate'] and v > OUT['pure_proc_900']['test_rate']
        OUT['hit'] = bool(hit)
        if hit:
            # reverse direction: fit on TEST, score on FIT (swap roles by swapping FI/TI page lists)
            dF = page_syms(TESTSH, TI, ch, place); dT = page_syms(FIp, FI, ch, place); best = None
            for rs in range(8):
                d = CribDec2(dF, random.Random(rs), ch in FIXED); b = d.fit()
                if best is None or b[0] > best[0][0]: best = (b, d)
            (sc, T, L), d = best; C, Y = d.encode_other(dT); OUT['reverse_rate'] = d.score(T, L, C, Y) / int((Y >= 0).sum())
        print(ch, place, 'VOYNICH', OUT['voynich'], 'timm', OUT['timm_21']['test_rate'], 'pure', OUT['pure_proc_900']['test_rate'], 'null', OUT['voynich_null'], 'hit', hit, OUT.get('reverse_rate'), flush=True)
    json.dump(OUT, open(f'./work/meaning_procedure/d6c2_{ch}_{place}.json', 'w'), indent=1)
