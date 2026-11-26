"""Hybrid generator family: copy-and-vary (Timm) + slot onset/body/ending + boundary-weighted source
choice + line rules, all tables from FIT pages only. Scoring = the project's 24-statistic profile."""
import os, sys, random, re, collections, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boot  # noqa: F401  (maps ./work -> local mirror)

_src = open('./work/target_profile/score.py').read()
_src = _src.split("REF = {**vm")[0].replace("ARG = sys.argv[1:]", "ARG = []")
exec(_src)          # VLINES, FIp, FI, TI, gg, profile, cstats, c2, vm, vs, V1, sd1, V2, sd2, rule
REF = {**vm, **V1, **V2}; SD = {**vs, **sd1, **sd2}
KEYS = list(REF)
FITREF = full(FIp)  # FIT-half values of all 24 statistics (fitting target)

_w3 = open('./work/window_chain/code/wchain3.py').read()
exec(_w3[_w3.index("def ops("):_w3.index("def mutate(")])   # learned single-edit ops from FIT -> OPS
OPS = [o for o in OPS]
OPS_BY_POS = {p: [o for o in OPS if o[1] == p] for p in "FML"}

END = re.compile(r'(aiin|ain|iin|eedy|edy|dy|eey|ey|ol|or|ar|al|am|y|s|r|l|n|m)$')
GAL = ('k', 't', 'p', 'f', 'ckh', 'cth', 'cph', 'cfh')


def split3(w):
    g = gg(w); f = g[0]; rest = ''.join(g[1:]); m = END.search(rest); e = m.group(1) if m else ''
    return f, (rest[:len(rest) - len(e)] if e else rest), e


CL = lambda f: f if f in ('ch', 'sh', 'q', 'o', 'd', 'y', 'a', 's') else 'G' if f in GAL else 'x'
lastg = lambda w: gg(w)[-1]

# ---------------- FIT tables ----------------
on2 = collections.defaultdict(collections.Counter); on1 = collections.defaultdict(collections.Counter)
onw = collections.defaultdict(collections.Counter)            # word-level: prev word -> next onset
bf = collections.defaultdict(collections.Counter); eb = collections.defaultdict(collections.Counter)
LIw = collections.Counter(); PGw = collections.Counter(); allf = collections.Counter(); WC = collections.Counter()
for p in FIp:
    for li, l in enumerate(p):
        if not l: continue
        (PGw if li == 0 else LIw)[l[0]] += 1
        for w in l:
            f, b, e = split3(w); bf[f][b] += 1; eb[b[-1:] if b else f[-1:]][e] += 1; allf[f] += 1; WC[w] += 1
        for a, b_ in zip(l, l[1:]):
            on2[(lastg(a), CL(gg(a)[0]))][gg(b_)[0]] += 1; on1[lastg(a)][gg(b_)[0]] += 1; onw[a][gg(b_)[0]] += 1
TOPW = {w for w, _ in WC.most_common(150)}
wbi = collections.defaultdict(collections.Counter)
for p in FIp:
    for l in p:
        for a, b_ in zip(l, l[1:]): wbi[a][b_] += 1
WBI = {w: c for w, c in wbi.items() if sum(c.values()) >= 6}
ONW = {w: c for w, c in onw.items() if w in TOPW and sum(c.values()) >= 8}


def _tab(c, tau):
    k = list(c); v = np.array([c[x] for x in k], float) ** tau; return k, v / v.sum()


_cache = {}


def dist(c, tau, key):
    t = _cache.get((key, tau))
    if t is None: t = _cache[(key, tau)] = _tab(c, tau)
    return t


def draw(t, r):
    k, p = t; x = r.random(); acc = 0.0
    for a, b in zip(k, p):
        acc += b
        if x < acc: return a
    return k[-1]


def onset_probs(prev, prm):
    """P(onset | previous word): glyph-level part mixed with a word-level part (alpha)."""
    c = on2[(lastg(prev), CL(gg(prev)[0]))]
    if sum(c.values()) < 5: c = on1[lastg(prev)]
    if not c: c = allf
    k, p = dist(c, prm['tau'], ('on', lastg(prev), CL(gg(prev)[0])))
    pd = dict(zip(k, p))
    if prm['alpha'] > 0 and prev in ONW:
        k2, p2 = dist(ONW[prev], 1.0, ('onw', prev))
        for a, b in zip(k2, p2): pd[a] = (1 - prm['alpha']) * pd.get(a, 0) + prm['alpha'] * b
        for a in list(pd):
            if a not in k2: pd[a] *= (1 - prm['alpha'])
    return pd


def mutate(w, r, prm):
    g = gg(w)
    wts = [prm['wF'], prm['wM'], prm['wL']]
    for _ in range(12):
        pos = r.choices("FML", wts)[0]
        if not OPS_BY_POS[pos]: continue
        t, _, x, y = r.choice(OPS_BY_POS[pos])
        idx = [0] if pos == 'F' else [len(g) - 1] if pos == 'L' else list(range(1, len(g) - 1))
        if t == 'sub':
            c = [i for i in idx if 0 <= i < len(g) and g[i] == x]
            if c: i = r.choice(c); return ''.join(g[:i] + [y] + g[i + 1:])
        elif t == 'del' and len(g) > 1:
            c = [i for i in idx if 0 <= i < len(g) and g[i] == x]
            if c: i = r.choice(c); return ''.join(g[:i] + g[i + 1:])
        elif t == 'ins':
            i = 0 if pos == 'F' else len(g) if pos == 'L' else (r.randrange(1, len(g)) if len(g) > 1 else None)
            if i is not None: return ''.join(g[:i] + [y] + g[i:])
    return w


def new_ending(b, f, prev_e, r, prm):
    key = b[-1:] if b else f[-1:]
    c = eb[key]
    if not c: return ''
    k, p = dist(c, prm['taue'], ('e', key))
    if prev_e is not None and r.random() < prm['anti']:
        pp = [0 if x == prev_e else y for x, y in zip(k, p)]; s = sum(pp)
        if s > 0: return r.choices(k, pp)[0]
    return draw((k, p), r)


def fresh(f, prev, page, pend, r, prm):
    same = [x for x in page[-prm['W']:] if split3(x)[0] == f]
    if same and r.random() < prm['pb']: b = split3(r.choice(same))[1]
    elif page and r.random() < prm['px']: b = split3(r.choice(page[-prm['W']:]))[1]
    else:
        b = draw(dist(bf[f], prm['taub'], ('b', f)), r) if bf[f] else ''
    if pend and r.random() < prm['pe']: e = r.choice(pend[-prm['W']:])
    else: e = new_ending(b, f, split3(prev)[2] if prev else None, r, prm)
    return f + b + e


def gen(shapes, prm, seed):
    r = random.Random(seed); out = []; hist = []
    for p in shapes:
        q = []; page = list(hist[-prm['carry']:]) if prm['carry'] else []; pend = [split3(x)[2] for x in page]
        for li, l in enumerate(p):
            words = []
            for k in range(len(l)):
                if k == 0:
                    w = draw(dist(PGw if li == 0 else LIw, prm['tauL'], ('L', li == 0)), r)
                else:
                    prev = words[-1]; pd = onset_probs(prev, prm)
                    src = page[-prm['W']:]
                    if prev in WBI and r.random() < prm['pw']:
                        # word-level transition (FIT word bigram), the word-order mechanism
                        w = draw(dist(WBI[prev], prm['tauw'], ('wb', prev)), r)
                        if r.random() < prm['mu'] * prm['mw']: w = mutate(w, r, prm)
                    elif src and r.random() < prm['pc']:
                        # copy-and-vary: K candidates, weighted by boundary fit of their onset and recency
                        cand = [src[r.randrange(len(src))] for _ in range(prm['K'])]
                        wt = [(pd.get(gg(c)[0], 0) + 1e-4) ** prm['beta'] for c in cand]
                        w = r.choices(cand, wt)[0]
                        if r.random() < prm['mu']: w = mutate(w, r, prm)
                        if r.random() < 1 - prm['keepE']:
                            f, b, e = split3(w); w = f + b + new_ending(b, f, split3(prev)[2], r, prm)
                    else:
                        f = draw((list(pd), list(pd.values())), r)
                        w = fresh(f, prev, page, pend, r, prm)
                    if not w: w = prev
                words.append(w); page.append(w); pend.append(split3(w)[2])
            q.append(words)
        hist = page
        out.append(rule([q], prm['q'], r)[0] if prm['q'] > 0 else q)
    return out


def score_on(pages, ref):
    g = full(pages)
    ok = {k: abs(g[k] - ref[k]) < 2 * SD[k] for k in KEYS}
    loss = sum(min(((g[k] - ref[k]) / SD[k]) ** 2, 25) for k in KEYS)
    return g, ok, loss


FITSH = FIp
TESTSH = [VLINES[i] for i in TI]

SPACE = dict(tau=(0.4, 1.6), alpha=(0.0, 0.8), tauL=(0.5, 1.2), taub=(0.5, 1.5), taue=(0.5, 1.5),
             pc=(0.0, 0.95), K=(1, 12), beta=(0.0, 4.0), mu=(0.0, 0.9), wF=(0.05, 1.0), wM=(0.05, 1.0), wL=(0.05, 1.0),
             keepE=(0.0, 1.0), anti=(0.0, 1.0), pb=(0.0, 0.95), px=(0.0, 0.6), pe=(0.0, 0.7), W=(20, 400),
             carry=(0, 200), q=(0.0, 0.8), pw=(0.0, 0.7), tauw=(0.3, 1.5), mw=(0.0, 1.0))
INTS = {'K', 'W', 'carry'}


def fit_loss(prm, seed=1):
    g, ok, loss = score_on(gen(FITSH, prm, seed), FITREF)
    return loss, sum(ok.values()), g
