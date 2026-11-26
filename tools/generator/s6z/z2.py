"""S6-Z2 extension: (a) fresh words built from the group's own word parts, kept away from recent words; (b) no exact immediate repeat.
pF: share of template words replaced by a part-built word. pR: probability an exact repeat of the previous word is redrawn."""
_tw_z2 = templ_word
def _near_recent(w, page):
    rec = page[-40:]
    return w in rec or any(ed1(w, x) for x in rec if abs(len(x) - len(w)) <= 1)
def parts_word(prev, page, r, prm):
    pd = onset_probs(prev, prm) if prev else None
    for _ in range(6):
        f = draw((list(pd), list(pd.values())), r) if pd else draw(dist(allf, 1.0, ('allf',)), r)
        b = draw(dist(bf[f], prm.get('tF', prm['taub']), ('b', f)), r) if bf[f] else ''
        e = new_ending(b, f, split3(prev)[2] if prev else None, r, prm); w = f + b + e
        if not _near_recent(w, page): return w
    return w
def templ_word(prev, page, pend, r, prm):
    pF = prm.get('pF', 0.0); pR = prm.get('pR', 0.0)
    w = parts_word(prev, page, r, prm) if pF > 0 and r.random() < pF else _tw_z2(prev, page, pend, r, prm)
    if pR > 0 and w == prev and r.random() < pR:
        for _ in range(3):
            w = _tw_z2(prev, page, pend, r, prm)
            if w != prev: break
    return w
