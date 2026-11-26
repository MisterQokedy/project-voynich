"""Calibration: simple substitution of real Latin (Caesar BG4) and Italian (Paradiso) into EVA-like glyph units.
Does the harness (a) score the true key far above random keys, (b) give partial true keys graded credit,
(c) recover a working key by fitting on half the ciphertext, scored on the other half? Output ../calib.out"""
import sys, random, statistics as S
sys.path.insert(0, './work/decipherment_harness/code'); import harness as h
POOL = ['o', 'e', 'y', 'a', 'd', 'i', 'ch', 'l', 'k', 'r', 'n', 't', 'q', 'sh', 's', 'p', 'm', 'cth', 'ckh', 'f', 'cph', 'g', 'cfh', 'x', 'b', 'v']
out = open(f'{h.H}/calib.out', 'w')
def pr(*a): print(*a, flush=True); print(*a, file=out, flush=True)
def z(x, xs): return (x - S.mean(xs)) / (S.pstdev(xs) or 1e-9)
for lang, plain in (('latin', 'latin_plain'), ('italian', 'italian_plain')):
    toks = h.CORP[plain][:8000]; letters = sorted(set(''.join(toks))); r = random.Random(1); pool = POOL[:]; r.shuffle(pool)
    enc = dict(zip(letters, pool)); true = {v: k for k, v in enc.items()}
    lines = [[tuple(enc[c] for c in w) for w in toks[i:i + 9]] for i in range(0, len(toks), 9)]
    A, B = lines[:len(lines) // 2], lines[len(lines) // 2:]      # fit half / held-out half
    st = h.score(true, B, lang)
    rnd = []
    for k in range(300):
        vals = list(true.values()); r.shuffle(vals); rnd.append(h.score(dict(zip(true, vals)), B, lang))
    pr(f'== {lang}: {len(toks)} words, {len(letters)} letters -> {len(letters)} EVA units')
    pr(f'true key held-out: M1 {st["M1"]:.2f} bits/char  M2 {st["M2"]:.3f}  M4 {st["M4"]:.3f}')
    for m in ('M1', 'M2', 'M4'):
        xs = [x[m] for x in rnd]; pr(f'  random keys (300) {m}: {S.mean(xs):.3f} +- {S.pstdev(xs):.3f}  max/min {max(xs):.3f}/{min(xs):.3f}  z(true) {z(st[m], xs):+.1f}')
    sh = h.score(true, h.wshuffle(B, 3), lang); pr(f'  true key on glyph-shuffled ciphertext: M1 {sh["M1"]:.2f} M2 {sh["M2"]:.3f} M4 {sh["M4"]:.3f}')
    for f in (0.25, 0.5, 0.75):
        res = []
        for k in range(30):
            us = list(true); r.shuffle(us); bad = us[:round(len(us) * (1 - f))]; vals = [true[u] for u in bad]; r.shuffle(vals)
            kk = dict(true); kk.update(dict(zip(bad, vals))); res.append(h.score(kk, B, lang))
        pr(f'  partial key {int(f*100)}% correct: M1 {S.mean(x["M1"] for x in res):.2f}  M2 {S.mean(x["M2"] for x in res):.3f}  M4 {S.mean(x["M4"] for x in res):.3f}')
    inv = list(true); vals = letters
    for sd in (1, 2):
        fk = h.fit_key(A, lang, inv, vals, seed=sd); fs = h.score(fk, B, lang); acc = sum(fk[u] == true[u] for u in inv) / len(inv)
        pr(f'  key FITTED on other half (seed {sd}): held-out M1 {fs["M1"]:.2f} M2 {fs["M2"]:.3f} M4 {fs["M4"]:.3f}; {acc:.0%} of key correct')
out.close()
