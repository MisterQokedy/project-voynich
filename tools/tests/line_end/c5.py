"""C5 (PREREG.md)."""
import sys, json, random, collections, math, numpy as np
sys.path.insert(0, './work/line_end/code')
from parse import parse, gg
V = './work/'
def js(a, b):
    k = set(a) | set(b); na, nb = sum(a.values()), sum(b.values()); d = 0
    for x in k:
        p, q = a[x] / na, b[x] / nb; m = (p + q) / 2
        d += (p * math.log2(p / m) if p else 0) + (q * math.log2(q / m) if q else 0)
    return d / 2
def mk(pages_words, flags=None):
    """pages_words: [[ [words] ]] -> list of pages of line dicts with 'short' proxy (and 'pe' real flag if given)."""
    out = []
    for pi, p in enumerate(pages_words):
        L = [[w for w in l if w] for l in p]; ln = [len(' '.join(l)) for l in L if l]
        if not ln: continue
        med = float(np.median(ln)); Q = []
        for li, l in enumerate(L):
            if not l: continue
            Q.append(dict(w=l, short=len(' '.join(l)) < 0.7 * med, pe=(flags[pi][li] if flags else None)))
        out.append(Q)
    return out
def feats(P, key='short'):
    fin, mid, ff, fm = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    C = collections.Counter(); lines = [l for p in P for l in p if len(l['w']) >= 3]
    for l in lines:
        for x in l['w'][1:-1]: C[x] += 1
    fa, ma = [], []; Lf = {True: [], False: []}; Lm = {True: [], False: []}
    for l in lines:
        w = l['w']; g = [gg(x) for x in w]
        fin[g[-1][-1]] += 1; ff[g[-1][0]] += 1
        for x in g[1:-1]: mid[x[-1]] += 1; fm[x[0]] += 1
        own = collections.Counter(w[1:-1]); fa.append(C[w[-1]] - own[w[-1]] > 0); ma += [C[x] - own[x] > 0 for x in w[1:-1]]
        t = bool(l[key]); Lf[t].append(len(g[-1])); Lm[t] += [len(x) for x in g[1:-1]]
    nf, nm = sum(fin.values()), sum(mid.values())
    lift = max((fin[u] / nf) / max(mid[u] / nm, 1e-4) for u in fin if fin[u] / nf >= 0.01)
    exc = lambda t: (np.mean(Lf[t]) - np.mean(Lm[t])) if Lf[t] and Lm[t] else float('nan')
    return dict(E2=js(fin, mid), E2first=js(ff, fm), LE4=float(np.mean(fa) - np.mean(ma)), short_full=exc(False), Dproxy=exc(True) - exc(False), lift=lift)
def shuf(P, r):
    out = []
    for p in P:
        Q = []
        for l in p: w = l['w'][:]; r.shuffle(w); Q.append(dict(l, w=w))
        out.append(Q)
    return out
def excess(P, n=200, seed=1):
    r = random.Random(seed); o = feats(P); N = [feats(shuf(P, r)) for _ in range(n)]
    return {k: o[k] - float(np.nanmean([x[k] for x in N])) for k in o}, o
TX = {}
b8 = json.load(open(V + 'regional/comparison/comparison_pages_b8.json'))
for k in ('de_austrian_klosterneuburg_cod48_ms_15c', 'de_swabian_inzigkofen_oct842_ms_15c', 'de_swabian_inzigkofen_fol1045_ms_15c', 'de_bav_enhg_charters_1480_85_ms'): TX[k] = ('ms', b8[k])
for f in ('mhg_pages', 'htr_pages'):
    for k, v in json.load(open(V + f'regional/{f}.json')).items(): TX[k] = ('ms', v)
for k, v in b8.items():
    if k.endswith('_ridges'): TX[k] = ('print', v)
VP = parse(V + 'transcriptions/ZL3b-n.txt')
VW = [[l['w'] for l in p['lines']] for p in VP]; VF = [[l['pe'] for l in p['lines']] for p in VP]
VM = mk([[[w for w in l if w] for l in p] for p in VW], VF)
res = {}
ev, ov = excess(VM); evr, _ = excess(VM, key_real := None) if False else (None, None)
# Voynich with real paragraph flags (proxy check)
def feats_real(P): return feats(P, key='pe')
r = random.Random(1); o = feats_real(VM); N = [feats_real(shuf(VM, r)) for _ in range(200)]; evr = {k: o[k] - float(np.nanmean([x[k] for x in N])) for k in o}
agree = np.mean([l['short'] == bool(l['pe']) for p in VM for l in p if len(l['w']) >= 3])
rb = random.Random(3); BS = collections.defaultdict(list)
for _ in range(200):
    S = [VM[rb.randrange(len(VM))] for _ in VM]; e, _ = excess(S, n=20, seed=rb.randrange(10 ** 6))
    for k, x in e.items(): BS[k].append(x)
SD = {k: float(np.nanstd(v)) for k, v in BS.items()}
print(f'Voynich (proxy): ' + ' '.join(f'{k} {v:+.3f} (sd {SD[k]:.3f})' for k, v in ev.items()))
print(f'Voynich (real paragraph flags): ' + ' '.join(f'{k} {v:+.3f}' for k, v in evr.items()) + f' | proxy agrees with real flag on {agree:.2f} of lines')
res['voynich'] = dict(excess=ev, raw=ov, sd=SD, excess_real=evr, proxy_agree=float(agree))
for k, (kind, pages) in TX.items():
    e, o = excess(mk(pages)); res[k] = dict(kind=kind, excess=e, raw=o, lines=sum(len(p) for p in pages))
    print(f'{kind:5s} {k:45s} ' + ' '.join(f'{f} {v:+.3f}' for f, v in e.items()), flush=True)
print('\nVerdicts (13 manuscript sets):')
verd = {}
for f in ev:
    xs = [res[k]['excess'][f] for k in TX if TX[k][0] == 'ms' and not math.isnan(res[k]['excess'][f])]; lo, hi = min(xs), max(xs); v = ev[f]
    out = 'WITHIN' if lo <= v <= hi else ('SPECIFIC' if (v > hi + 2 * SD[f] or v < lo - 2 * SD[f]) else 'EDGE')
    verd[f] = out; print(f'  {f:11s} Voynich {v:+.3f}  manuscripts [{lo:+.3f}, {hi:+.3f}]  -> {out}')
res['verdicts'] = verd
json.dump(res, open(V + 'c5/c5.json', 'w'), indent=1, default=float)
