"""S6-Y shim: split and caches per run, chosen by env S6Y_RUN. Shared files are never written."""
import builtins, os, json
_V = './work/'; _RUN = os.environ['S6Y_RUN']
_C = _V + f's6y/cache/{_RUN}/'; os.makedirs(_C, exist_ok=True)
_orig_open = builtins.open; _orig_exists = os.path.exists
S6S_MAP = {
    _V + 'timm_generator/split.json': _V + f's6y/splits/{_RUN}.json',
    _V + 'le14/le_ref.json': _C + 'le_ref.json', _V + 's6k/ref.json': _C + 's6k_ref.json', _V + 's6m/ref.json': _C + 's6m_ref.json',
    _V + 'ws2/ref.json': _C + 'ws2_ref.json', _V + 'ws1/ws1.json': _C + 'ws1.json',
}
def _m(p):
    try: return S6S_MAP.get(os.fspath(p), p)
    except TypeError: return p
builtins.open = lambda p, *a, **k: _orig_open(_m(p), *a, **k)
os.path.exists = lambda p: _orig_exists(_m(p))
