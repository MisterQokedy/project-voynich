"""Usage: run.py corp.json out.json"""
import sys, json, random
import numpy as np
sys.path.insert(0, './work/language_test/code')
from gen import *; from stats import *
C = json.load(open(sys.argv[1])); r = random.Random(7)
V = C['voynich']
C['C1_verbose_latin'] = cipher_verbose(C['latin_isidore'], verbose_map())
C['C2_sorted_latin'] = cipher_sorted(C['latin_isidore'])
vt = np.mean([len(set([w for p in ch for l in p for w in l][:5000])) for ch in chunks(V)])
def types_of(pp): return np.mean([len(set([w for p in ch for l in p for w in l][:5000])) for ch in chunks(pp)])
best = min(((abs(types_of(timm(V, a)) - vt), a) for a in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]))
C['G1_timm'] = timm(V, best[1], seed=3); print('timm rate', best[1], 'voy types', vt)
best = min(((abs(types_of(rugg(V, n)) - vt), n) for n in [10, 15, 20, 30, 40, 60, 80, 120, 200]))
C['G2_rugg'] = rugg(V, best[1], seed=3); print('rugg rows', best[1])
W = [w for p in V for l in p for w in l]; r.shuffle(W); sh, i = [], 0
for p in V:
    sh.append([]);
    for l in p: sh[-1].append(W[i:i + len(l)]); i += len(l)
C['ctrl_voynich_shuffled'] = sh
chars = [c for w in W for c in w]; alpha = sorted(set(chars))
noise = lambda pick: [[[''.join(pick() for _ in w) for w in l] for l in p] for p in V]   # same word lengths, lines, pages
C['N1_uniform_noise'] = noise(lambda: r.choice(alpha))
C['N2_freq_noise'] = noise(lambda: r.choice(chars))
json.dump(C, open(sys.argv[2].replace('.json', '_corp.json'), 'w'))
R = {}
ONLY = sys.argv[3].split(',') if len(sys.argv) > 3 else None
import os
if ONLY and os.path.exists(sys.argv[2]): R = json.load(open(sys.argv[2]))
for k, pp in C.items():
    if ONLY and k not in ONLY: continue
    R[k] = [stats(ch, r) for ch in chunks(pp)]
    m = {s: round(float(np.mean([x[s] for x in R[k]])), 3) for s in R[k][0]}
    print(k, len(R[k]), m, flush=True)
json.dump(R, open(sys.argv[2], 'w'))
