"""S6-Z base: shimz + S6-Y generator; PQ = that direction's S6-Y best (or S6Z_BASE json)."""
exec(open('./work/s6z/code/shimz.py').read())
exec(open('./work/s6y/code/s6y.py').read())
for _e in filter(None, os.environ.get('S6Z_EXT', '').split(',')): exec(open(f'./work/s6z/code/{_e}.py').read())
_bp = (os.environ.get('S6Z_BASE') or './work/s6y/out/{RUN}/best.json').format(RUN=_RUN, GRP=_GRP)
PQ = json.load(open(_bp))
DFIT = drift(FIp)
def loss_y(g):
    ok, L, x, v, w = loss_o(g); d = drift(g); return ok, L + min(((d - DFIT) / 0.045) ** 2, 25), x, v, (w, d)
PEALL = [[bool(x) for x in pe] for pe in PE]
def gen_group(prm, seed):
    """Generate this group's pages (FIT and TEST) as {page index: page}."""
    assert len(VLINES) == len(GLOB)
    return dict(zip(GLOB, gen12(VLINES, PEALL, prm, seed)))
for _e in filter(None, os.environ.get('S6Z_POST', '').split(',')): exec(open(f'./work/s6z/code/{_e}.py').read())
