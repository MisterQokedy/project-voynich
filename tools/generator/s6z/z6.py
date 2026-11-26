"""S6-Z6 post-extension (S6Z_POST=z6): long-word gallows habit, mid-line only (junc_templ is the mid-line word chooser;
line-initial and line-final words keep their own rules). For a mid-line word of >= 6 glyphs that is not among the page's
previous 40 words: (1) with probability dD, if it has a doubled e or i, redraw up to 4 times for a long, new word without one;
(2) with probability gP, if it has no p/f gallows, insert p or f (FIT p:f ratio) before a random inner ch/sh."""
def _dbl(g): return any(a == b and a in ('e', 'i') for a, b in zip(g, g[1:]))
_pf = collections.Counter(x for p in FITSH for l in p for v in l for x in gg(v) if x in ('p', 'f'))
_PSH = _pf['p'] / max(1, _pf['p'] + _pf['f'])
_jt_z6 = junc_templ
def junc_templ(prev, page, pend, r, prm, k):
    w = _jt_z6(prev, page, pend, r, prm, k); g = gg(w)
    if len(g) < 6 or w in page[-40:]: return w
    dD = prm.get('dD', 0.0); gP = prm.get('gP', 0.0)
    if dD > 0 and _dbl(g) and r.random() < dD:
        for _ in range(4):
            w2 = _jt_z6(prev, page, pend, r, prm, k); g2 = gg(w2)
            if len(g2) >= 6 and w2 not in page[-40:] and not _dbl(g2): w, g = w2, g2; break
    if gP > 0 and not any(x in ('p', 'f') for x in g) and r.random() < gP:
        ix = [i for i in range(1, len(g)) if g[i] in ('ch', 'sh')]
        if ix:
            i = r.choice(ix); w = ''.join(g[:i]) + ('p' if r.random() < _PSH else 'f') + ''.join(g[i:])
    return w
