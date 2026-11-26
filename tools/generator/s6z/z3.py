"""S6-Z3 extension: directional ending-order preference, one table per group (Currier language), FIT pages only.
Ending = last 2 characters (as M2); top 15 endings in the group's FIT text, others pooled as '~'.
T[a][b] = log((n_ab + 1) / (E_ab + 1)), E_ab = expected count of a -> b under within-line shuffling (20 shuffles).
A candidate next word w after prev is accepted with probability min(1, exp(bE * T[end(prev)][end(w)])), up to 5 redraws."""
def _z3_tab():
    end = lambda w: w[-2:]; toks = [w for p_ in FIp for l_ in p_ for w in l_]
    top = {e for e, _ in collections.Counter(map(end, toks)).most_common(15)}
    E = lambda w: end(w) if end(w) in top else '~'
    obs = collections.Counter(); exp_ = collections.Counter(); rr = random.Random(5)
    for p_ in FIp:
        for l_ in p_:
            ee = [E(w) for w in l_]
            for a_, b_ in zip(ee, ee[1:]): obs[(a_, b_)] += 1
            for _ in range(20):
                s_ = rr.sample(ee, len(ee))
                for a_, b_ in zip(s_, s_[1:]): exp_[(a_, b_)] += 1 / 20
    keys = set(obs) | set(exp_)
    return E, {k: math.log((obs[k] + 1) / (exp_[k] + 1)) for k in keys}
Z3_E, Z3_T = _z3_tab()
_jt_z3 = junc_templ
def junc_templ(prev, page, pend, r, prm, k):
    b = prm.get('bE', 0.0); w = _jt_z3(prev, page, pend, r, prm, k)
    if b <= 0 or not prev: return w
    ep = Z3_E(prev)
    for _ in range(5):
        if r.random() < min(1.0, math.exp(b * Z3_T.get((ep, Z3_E(w)), 0.0))): return w
        w = _jt_z3(prev, page, pend, r, prm, k)
    return w
