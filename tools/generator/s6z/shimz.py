"""S6-Z shim: direction (S6Z_RUN) + page group (S6Z_GRP = all | A | B). Pages outside the group are
removed from the page file inside this process; all tables and FIT targets then come
from the group's FIT pages only. Shared files are never written."""
import builtins, os, json
_V = './work/'; _RUN = os.environ['S6Z_RUN']; _GRP = os.environ.get('S6Z_GRP', 'all')
_C = _V + f's6z/cache/{_RUN}_{_GRP}/'; os.makedirs(_C, exist_ok=True)
_orig_open = builtins.open; _orig_exists = os.path.exists
_D0 = json.load(_orig_open(_V + 'manuscript_wide/pages2.json'))
def GROUP(p):  # Currier language group; unlabelled pages (hand 4 etc.) go with B, as in timm_generator/common.py
    return 'A' if p.get('L') == 'A' else 'B'
GLOB = [i for i, p in enumerate(_D0) if _GRP == 'all' or GROUP(p) == _GRP]   # original page indices of this group
_PG = _V + 'manuscript_wide/pages2.json'
if _GRP != 'all':   # this process sees only the group's pages (FIT and TEST), so every module's FI/TI agree
    _tmp = f'/tmp/s6z/pages2_only{_GRP}.json'; os.makedirs('/tmp/s6z', exist_ok=True)
    if not _orig_exists(_tmp):
        json.dump([_D0[i] for i in GLOB], _orig_open(_tmp + '.part', 'w')); os.replace(_tmp + '.part', _tmp)
    _PG = _tmp
S6S_MAP = {
    _V + 'timm_generator/split.json': _V + f's6y/splits/{_RUN}.json',
    _V + 'manuscript_wide/pages2.json': _PG,
    _V + 'le14/le_ref.json': _C + 'le_ref.json', _V + 's6k/ref.json': _C + 's6k_ref.json', _V + 's6m/ref.json': _C + 's6m_ref.json',
    _V + 'ws2/ref.json': _C + 'ws2_ref.json', _V + 'ws1/ws1.json': _C + 'ws1.json',
}
def _m(p):
    try: return S6S_MAP.get(os.fspath(p), p)
    except TypeError: return p
builtins.open = lambda p, *a, **k: _orig_open(_m(p), *a, **k)
os.path.exists = lambda p: _orig_exists(_m(p))
# timm_generator/common.py needs FIT pages of both languages for SHAPE (used only by the Timm runner):
# load it as a module with SHAPE skipped for a language that has no pages in this process.
import sys as _sys, types as _types
_sys.path.insert(0, _V + 'timm_generator/code'); _sys.path.insert(0, _V + 'gibberish/code')
if _GRP != 'all' and 'common' not in _sys.modules:
    _src = _orig_open(_V + 'timm_generator/code/common.py').read()
    _src = _src.replace("SHAPE = {L: shape(L) for L in 'AB'}", "SHAPE = {L: shape(L) for L in 'AB' if idx(L, 'fit')}")
    assert 'if idx(L' in _src
    _mod = _types.ModuleType('common'); _mod.__file__ = _V + 'timm_generator/code/common.py'
    exec(compile(_src, _mod.__file__, 'exec'), _mod.__dict__); _sys.modules['common'] = _mod

# Small groups: a FIT or TEST half under 5,000 words gives no profile chunk. In group mode only, a half with
# no full chunk is scored as one chunk of all its pages (same rule for real and generated pages in the process).
if _GRP != 'all':
    for _src_p, _fn in (('naibbe_test/code/nb.py', 'chunks'), ('timm_rules/code_endrule/confirm.py', 'chunks5')):
        _t = f'/tmp/s6z/patched_{_fn}.py'
        if not _orig_exists(_t):
            _x = _orig_open(_V + _src_p).read(); _old = "        if c >= n: o.append(cur); cur, c = [], 0\n    return o" if _fn == 'chunks5' else "        if c >= n: out.append(cur); cur, c = [], 0\n    return out"
            assert _old in _x, _fn
            _new = _old.replace("return o", "return o or ([q for q in pp if q] and [[q for q in pp if q]])") if _fn == 'chunks5' else _old.replace("return out", "return out or ([q for q in pp if q] and [[q for q in pp if q]])")
            _orig_open(_t + '.part', 'w').write(_x.replace(_old, _new)); os.replace(_t + '.part', _t)
        S6S_MAP[_V + _src_p] = _t
