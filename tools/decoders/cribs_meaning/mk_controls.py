# Generate procedural control pages (hybrid full and pure procedure) for FIT and TEST slot shapes.
import sys, json
sys.path.insert(0, './work/meaning_procedure/code')
from hybrid import *
P = json.load(open('./work/hybrid_gen/final_test.json'))['params']
for k in INTS: P[k] = int(round(P[k]))
PURE = dict(P, pw=0.0, alpha=0.0)
out = {}
for name, prm in (('hybrid_full', P), ('pure_proc', PURE)):
    for sd in range(900, 905):
        out[f'{name}_{sd}'] = dict(FIT=gen(FITSH, prm, sd + 1000), TEST=gen(TESTSH, prm, sd))
        if name == 'pure_proc':
            g, ok, loss = score_on(out[f'{name}_{sd}']['TEST'], REF); print(name, sd, sum(ok.values()), [k for k in ok if not ok[k]], flush=True)
json.dump(out, open('./work/meaning_procedure/cache/proc_controls.json', 'w'))
