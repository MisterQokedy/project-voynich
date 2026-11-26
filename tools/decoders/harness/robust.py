"""Robustness of the one Cheshire PASS (Latin): refit with 3 more seeds on Voynich and on each Timm seed. Output ../robust.out"""
import sys; sys.path.insert(0, './work/decipherment_harness/code'); import harness as h
import score_claims_defs as d
I = d.held(d.CH_SRC); F = d.fitpages(d.CH_SRC); T = d.texts(I); TF = d.texts(F)
out = open(f'{h.H}/robust.out', 'w')
for k in ('voynich', 'timm2001', 'timm2002', 'timm2003'):
    for sd in (2, 3, 4):
        sc = h.score(h.fit_key(TF[k], 'latin', d.INV, d.CH_VALS, fixed=d.CH_CORE, iters=1500, seed=sd), T[k], 'latin')
        line = f'{k} seed {sd}: M1 {sc["M1"]:.2f} M2 {sc["M2"]:.3f} M4 {sc["M4"]:.3f} pairs {sc["npairs"]}'; print(line, flush=True); print(line, file=out, flush=True)
