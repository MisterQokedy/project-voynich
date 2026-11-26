"""S16e search: staged heat-bath (Gibbs) annealing over the same D1 objective (n-gram LM + MLE emission term)."""
import math, numpy as np, numba as nb

@nb.njit(cache=True)
def _ng(text, j, lp, A, n):
    if j - n + 1 < 0: return 0.0
    idx = 0
    for q in range(j - n + 1, j + 1):
        c = text[q]
        if c < 0: return 0.0
        idx = idx * A + c
    return lp[idx]

@nb.njit(cache=True)
def _xlogx(x):
    return x * math.log(x) if x > 0 else 0.0

@nb.njit(cache=True)
def _local(text, s, pos_ptr, pos_idx, lp, A, n, mark, stamp):
    tot = 0.0
    for q in range(pos_ptr[s], pos_ptr[s + 1]):
        p = pos_idx[q]
        for j in range(p, p + n):
            if j < len(text) and mark[j] != stamp:
                mark[j] = stamp; tot += _ng(text, j, lp, A, n)
    return tot

@nb.njit(cache=True)
def _hb(seq, pos_ptr, pos_idx, nsym, lp, A, n, sweeps, T0, T1, seed, key0, active, wE):
    """active[s]=1: symbol is decoded; 0: masked (-1). Each sweep visits every active symbol once in random order and
    resamples its letter from exp(delta/T) over all A letters (heat bath). Returns best key seen and its objective."""
    np.random.seed(seed)
    key = key0.copy()
    text = np.empty(len(seq), dtype=np.int64)
    for i in range(len(seq)):
        s = seq[i]
        text[i] = key[s] if (s >= 0 and active[s] == 1) else -1
    ns = np.zeros(nsym)
    for s in range(nsym): ns[s] = pos_ptr[s + 1] - pos_ptr[s]
    NL = np.zeros(A)
    for s in range(nsym):
        if active[s] == 1: NL[key[s]] += ns[s]
    act = np.where(active == 1)[0]
    mark = np.zeros(len(seq), dtype=np.int64); stamp = 0
    sc = np.empty(A)
    cur = 0.0
    best = -1e300; bestkey = key.copy()
    for sw in range(sweeps):
        T = T0 * (T1 / T0) ** (sw / max(1, sweeps - 1))
        order = np.random.permutation(act)
        for s in order:
            old = key[s]; c = ns[s]
            NL[old] -= c
            for L in range(A):
                for q in range(pos_ptr[s], pos_ptr[s + 1]): text[pos_idx[q]] = L
                stamp += 1
                sc[L] = _local(text, s, pos_ptr, pos_idx, lp, A, n, mark, stamp) - wE * (_xlogx(NL[L] + c) - _xlogx(NL[L]))
            m = sc.max(); z = 0.0
            for L in range(A):
                sc[L] = math.exp((sc[L] - m) / T); z += sc[L]
            u = np.random.random() * z; acc = 0.0; new = A - 1
            for L in range(A):
                acc += sc[L]
                if u <= acc: new = L; break
            key[s] = new; NL[new] += c
            for q in range(pos_ptr[s], pos_ptr[s + 1]): text[pos_idx[q]] = new
        # objective after the sweep (full recompute, cheap relative to a sweep)
        tot = 0.0
        for j in range(len(text)): tot += _ng(text, j, lp, A, n)
        for L in range(A): tot -= wE * _xlogx(NL[L])
        cur = tot
        if cur > best: best = cur; bestkey[:] = key
    return bestkey, best

@nb.njit(parallel=True, cache=True)
def hb_many(seq, pos_ptr, pos_idx, nsym, lp, A, n, sweeps, T0, T1, seeds, keys0, active, wE):
    R = len(seeds); out = np.empty((R, nsym), dtype=np.int64); scs = np.empty(R)
    for r in nb.prange(R):
        k, b = _hb(seq, pos_ptr, pos_idx, nsym, lp, A, n, sweeps, T0, T1, seeds[r], keys0[r], active, wE)
        out[r] = k; scs[r] = b
    return out, scs

def staged(seq, ptr, idx, nsym, lp, A, n, R, seeds, keys0, wE, stages, sweeps, T0, T1, final_sweeps=30):
    """stages: list of fractions of symbols (by frequency) made active. Keys carry over between stages; newly activated
    symbols start from keys0 values (frequency-random). Ends with a near-greedy pass (T=0.05) over all symbols."""
    cnt = np.diff(ptr); order = np.argsort(-cnt, kind='stable')
    keys = keys0.copy(); scores = None
    for k, f in enumerate(stages):
        active = np.zeros(nsym, dtype=np.int64); active[order[:max(1, int(round(f * nsym)))]] = 1
        keys, scores = hb_many(seq, ptr, idx, nsym, lp, A, n, sweeps, T0, T1, seeds + 1000 * k, keys, active, wE)
    active = np.ones(nsym, dtype=np.int64)
    keys, scores = hb_many(seq, ptr, idx, nsym, lp, A, n, final_sweeps, 0.3, 0.05, seeds + 99999, keys, active, wE)
    return keys, scores
