"""Merge per-group parts into 202-slot texts: out/<TAG>/<run>/gen_<s>.json. argv: TAG groups(comma)"""
import json, sys, os
TAG, GR = sys.argv[1], sys.argv[2].split(','); O = f'./work/s6z/out/{TAG}'
for run in sorted(os.listdir(O)):
    for s in range(900, 905):
        parts = [f'{O}/{run}/part_{g}_{s}.json' for g in GR]
        if not all(os.path.exists(p) for p in parts): continue
        P = [None] * 202
        for p in parts:
            for k, v in json.load(open(p)).items(): P[int(k)] = v
        assert all(x is not None for x in P), (run, s); json.dump(P, open(f'{O}/{run}/gen_{s}.json', 'w'))
