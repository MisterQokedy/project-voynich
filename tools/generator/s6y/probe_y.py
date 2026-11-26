exec(open('/tmp/probe_w2.py').read().split("show('base', P0)")[0])
GL_ = ['d', 'q', 't', 'l', 'a']
def _lineft(l):
    w = l[1:]
    if not w: return None
    G = [x for v in w for x in gg(v)]; c = collections.Counter(G); n = max(len(G), 1); f = [c[g] / n for g in GL_]
    return f + [f[3] + f[4] - f[0] - f[1] - f[2]]
_D = {'lineft': _lineft}
rk = lambda a: np.argsort(np.argsort(a, kind='stable')).astype(float)
def drift(pages):
    out = []
    for pg in pages:
        F = [_D['lineft'](l) for l in pg if l]; F = [f[5] for f in F if f]
        if len(F) >= 8: out.append(np.corrcoef(rk(np.arange(len(F))), rk(np.array(F)))[0, 1])
    return float(np.nanmean(out))
def comp(w):
    g = gg(w); n = max(len(g), 1); return (sum(x in ('l', 'a') for x in g) - sum(x in ('d', 'q', 't') for x in g)) / n
_PAGE = {'tot': [], 'i': -1, 'last': 10 ** 9}
_jt0 = junc_templ
def junc_templ(prev, page, pend, r, prm, k):
    if len(page) < _PAGE['last']: _PAGE['i'] += 1
    _PAGE['last'] = len(page)
    b = prm.get('bD', 0.0)
    if b <= 0: return _jt0(prev, page, pend, r, prm, k)
    tot = _PAGE['tot'][min(_PAGE['i'], len(_PAGE['tot']) - 1)]; pos = min(len(page) / max(tot, 1), 1.0) - 0.5
    for _ in range(5):
        w = _jt0(prev, page, pend, r, prm, k)
        if r.random() < min(1.0, math.exp(b * pos * comp(w))): return w
    return w
def gen_d(prm, seed):
    _PAGE.update(tot=[sum(len(l) for l in p) for p in FITSH], i=-1, last=10 ** 9); return gen12(FITSH, PEF, prm, seed)
print('real FIT drift %+.3f' % drift(FIp), flush=True)
for bd in (0.0, 2.0, 5.0, 10.0):
    g = gen_d(dict(P0, bD=bd), 11); h = FULL(g); n = sum(abs(h[k] - reff[k]) <= BAND[k] for k in KS)
    print(f'bD={bd}: drift {drift(g):+.3f} profile {n}/24 miss {[k for k in KS if abs(h[k]-reff[k]) > BAND[k]]}', flush=True)
