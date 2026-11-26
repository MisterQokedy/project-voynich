"""S6-Z5 (A4-P full re-search) post-extension (S6Z_POST=z5): (1) onset habit: with probability aO, a mid-line word (not first,
not last) is redrawn (up to 60 tries) until its first glyph equals that of the word two back in the same line (A4-G mechanism);
(2) A4 (FIT-internal, as A4-G) added to the FIT objective: min(((A4(gen) - A4(real)) / sd)^2, 25), sd = sd of A4 over 40 random FIT page half-splits."""
exec(open('./work/s6z/code/a4lib.py').read().replace('def gg(w): return _GL4.findall(w)', 'gg4 = lambda w: _GL4.findall(w)').replace('slot_seqs(F, gg, v_end)', 'slot_seqs(F, gg4, v_end)').replace('slot_seqs(T, gg, v_end)', 'slot_seqs(T, gg4, v_end)'))
_CALL = "w = junc_templ(prev, page, pend, r, prm, mkey(gg(words[0])[0]))"
assert 'def gen11(' in _g and _CALL in _g
exec(_g.replace(_CALL, "_Z5W['w'] = words; " + _CALL))
_Z5W = {'w': []}
_jt_z5 = junc_templ
def junc_templ(prev, page, pend, r, prm, k):
    a = prm.get('aO', 0.0); words = _Z5W['w']
    if a <= 0 or len(words) < 2 or r.random() >= a: return _jt_z5(prev, page, pend, r, prm, k)
    want = gg4(words[-2])[0]; w = None
    for _ in range(60):
        w = _jt_z5(prev, page, pend, r, prm, k)
        if gg4(w) and gg4(w)[0] == want: return w
    return w
def _a4i(P, seed=1):
    a, b = internal(P); return A4(a, b, np.random.default_rng(seed))
A4_REAL = _a4i(FITSH); _rb = np.random.default_rng(44); _bs = []
for _ in range(40):   # split noise: random page halves instead of the fixed 4-page blocks
    _msk = _rb.random(len(FITSH)) < 0.5; _bs.append(A4([p for p, m in zip(FITSH, _msk) if m], [p for p, m in zip(FITSH, _msk) if not m], np.random.default_rng(1)))
A4_SD = max(float(np.std(_bs)), 0.001)
print('Z5 A4 target', round(A4_REAL, 4), 'sd', round(A4_SD, 4), flush=True)
_ly_z5 = loss_y
def loss_y(g):
    ok, L, x, v, w = _ly_z5(g); a = _a4i(g)
    return ok, L + min(((a - A4_REAL) / A4_SD) ** 2, 25), x, v, (w, a)
