"""S6-Y: S6-V + page-position drift term (bD)."""
exec(open('./work/s6v/code/s6v.py').read())
GL_ = ['d', 'q', 't', 'l', 'a']
def _lineft(l):
    w = l[1:]
    if not w: return None
    G = [x for v in w for x in gg(v)]; c = collections.Counter(G); n = max(len(G), 1); f = [c[g] / n for g in GL_]
    return f[3] + f[4] - f[0] - f[1] - f[2]
_rk = lambda a: np.argsort(np.argsort(a, kind='stable')).astype(float)
def drift(pages):
    out = []
    for pg in pages:
        F = [_lineft(l) for l in pg if l]; F = [f for f in F if f is not None]
        if len(F) >= 8:
            c = np.corrcoef(_rk(np.arange(len(F))), _rk(np.array(F)))[0, 1]
            if c == c: out.append(c)
    return float(np.mean(out)) if out else 0.0
def comp(w):
    g = gg(w); n = max(len(g), 1); return (sum(x in ('l', 'a') for x in g) - sum(x in ('d', 'q', 't') for x in g)) / n
_PAGE = {'tot': [1], 'i': -1, 'last': 10 ** 9}
_jt0 = junc_templ
def junc_templ(prev, page, pend, r, prm, k):
    if len(page) < _PAGE['last']: _PAGE['i'] += 1
    _PAGE['last'] = len(page)
    b = prm.get('bD', 0.0)
    if b <= 0: return _jt0(prev, page, pend, r, prm, k)
    tot = _PAGE['tot'][min(max(_PAGE['i'], 0), len(_PAGE['tot']) - 1)]; pos = min(len(page) / max(tot, 1), 1.0) - 0.5
    for _ in range(5):
        w = _jt0(prev, page, pend, r, prm, k)
        if r.random() < min(1.0, math.exp(b * pos * comp(w))): return w
    return w
_gen12_v = gen12
def gen12(shapes, pes, prm, seed, jshuf=False):
    _PAGE.update(tot=[sum(len(l) for l in p) for p in shapes], i=-1, last=10 ** 9)
    return _gen12_v(shapes, pes, prm, seed, jshuf)
