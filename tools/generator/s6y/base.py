"""S6-Y: shim + generator + base (= S6-V best) + objective with drift."""
exec(open('./work/s6y/code/shim6.py').read())
exec(open('./work/s6y/code/s6y.py').read())
PQ = json.load(open(f'./work/s6v/out/{_RUN}/best.json'))
assert 'bD' not in PQ
STAGES = dict(bD=(0.0, 12.0), bW=(0.0, 5.0), bR=(0.0, 5.0), bJ=(0.0, 5.0))
DFIT = drift(FIp)
def loss_y(g):
    ok, L, x, v, w = loss_o(g); d = drift(g); return ok, L + min(((d - DFIT) / 0.045) ** 2, 25), x, v, (w, d)
