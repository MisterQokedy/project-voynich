"""S6-Z4-d extension: Z3's directional ending-order table, but one table per SECTION (herbal, stars, balneological, pharma) inside
each Currier language, FIT pages only. A section with < 1,000 FIT words in the language uses the language-wide table.
Same table formula, ending classes (language top 15) and acceptance rule as Z3 (code/z3.py)."""
def _z4d_tab(pages, top):
    end = lambda w: w[-2:]; E = lambda w: end(w) if end(w) in top else '~'
    obs = collections.Counter(); exp_ = collections.Counter(); rr = random.Random(5)
    for p_ in pages:
        for l_ in p_:
            ee = [E(w) for w in l_]
            for a_, b_ in zip(ee, ee[1:]): obs[(a_, b_)] += 1
            for _ in range(20):
                s_ = rr.sample(ee, len(ee))
                for a_, b_ in zip(s_, s_[1:]): exp_[(a_, b_)] += 1 / 20
    return {k: math.log((obs[k] + 1) / (exp_[k] + 1)) for k in set(obs) | set(exp_)}
_z4d_top = {e for e, _ in collections.Counter(w[-2:] for p_ in FIp for l_ in p_ for w in l_).most_common(15)}
Z4D_E = lambda w: w[-2:] if w[-2:] in _z4d_top else '~'
_SECALL = [_D0[g].get('I') for g in GLOB]            # section of each group page (VLINES order)
_SECFIT = [_SECALL[i] for i in FI]                    # section of each FIT page (FITSH order)
Z4D_T = {'*': _z4d_tab(FIp, _z4d_top)}
for _s in ('H', 'S', 'B', 'P'):
    _pp = [FIp[j] for j, s in enumerate(_SECFIT) if s == _s]
    if sum(len(l) for p in _pp for l in p) >= 1000: Z4D_T[_s] = _z4d_tab(_pp, _z4d_top)
print('Z4d section tables', {s: len(t) for s, t in Z4D_T.items()}, 'FIT words', {s: sum(len(l) for j, p in enumerate(FIp) if _SECFIT[j] == s for l in p) for s in set(_SECFIT)}, flush=True)
_Z4D = {'sec': _SECFIT}
_g12_z4d = gen12
def gen12(shapes, pes, prm, seed, jshuf=False):
    _Z4D['sec'] = _SECFIT if shapes is FITSH else _SECALL if len(shapes) == len(_SECALL) else None
    assert _Z4D['sec'] is not None and len(_Z4D['sec']) == len(shapes)
    return _g12_z4d(shapes, pes, prm, seed, jshuf)
_jt_z4d = junc_templ
def junc_templ(prev, page, pend, r, prm, k):
    b = prm.get('bE', 0.0); w = _jt_z4d(prev, page, pend, r, prm, k)
    if b <= 0 or not prev: return w
    sec = _Z4D['sec'][min(max(_PAGE['i'], 0), len(_Z4D['sec']) - 1)]; T = Z4D_T.get(sec, Z4D_T['*']); ep = Z4D_E(prev)
    for _ in range(5):
        if r.random() < min(1.0, math.exp(b * T.get((ep, Z4D_E(w)), 0.0))): return w
        w = _jt_z4d(prev, page, pend, r, prm, k)
    return w
