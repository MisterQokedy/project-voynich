"""S6-Z2-b post-extension (S6Z_POST=z2b): adds one-off share (S27) and edit-of-previous-40 (S28) to the FIT objective.
Target = real FIT pages of the group; scale = sd of the statistic, estimated as sd(|half A - half B|)/2 over 40 random page half-splits of FIT."""
exec(open('./work/s6z/code/oneoff.py').read())
O_REAL = oneoff(FITSH)
_rr = random.Random(27); _d = {k: [] for k in O_REAL}
for _ in range(40):
    _ix = list(range(len(FITSH))); _rr.shuffle(_ix); _h = len(_ix) // 2
    _a, _b = oneoff([FITSH[i] for i in _ix[:_h]]), oneoff([FITSH[i] for i in _ix[_h:]])
    for k in _d: _d[k].append(_a[k] - _b[k])
O_SD = {k: max(float(np.std(v)) / 2, 1e-3) for k, v in _d.items()}
print('Z2b targets', {k: round(v, 4) for k, v in O_REAL.items()}, 'sd', {k: round(v, 4) for k, v in O_SD.items()}, flush=True)
_ly_z2b = loss_y
def loss_y(g):
    ok, L, x, v, w = _ly_z2b(g); o = oneoff(g)
    return ok, L + sum(min(((o[k] - O_REAL[k]) / O_SD[k]) ** 2, 25) for k in O_REAL), x, v, (w, o)
