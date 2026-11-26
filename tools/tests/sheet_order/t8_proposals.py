"""Score every published full order for Q13/Q20 (literature-review CSVs) on text and stain evidence,
ranked within the full space of nestings and singulion stacks (all sheet orders x orientations)."""
import sys, json, itertools, csv, re
from collections import defaultdict
import numpy as np
sys.path.insert(0, 'code'); from vlib import load, structure
exec(open('code/p1_stains.py').read().split("leaves = sorted")[0])  # maps, leafmap, prep
rng = np.random.default_rng(21)
keys = json.load(open('keys.json')); ix = {k: i for i, k in enumerate(keys)}
SIM = {'lsa': np.load('S_lsa.npy'), 'tfidf': np.load('S_tfidf.npy')}
rows = list(csv.DictReader(open('./work/page-order-review/proposed_orders_pages.csv')))
meta = {r['id']: r for r in csv.DictReader(open('./work/page-order-review/proposed_orders.csv'))}
props = defaultdict(list)
for r in rows: props[r['id']].append(r['page'].lstrip('f'))
def text_score(seq, S):
    v = []
    for a, b in zip(seq, seq[1:]):
        if a[:-1] == b[:-1]: continue          # same leaf: immutable
        if a in ix and b in ix: v.append(S[ix[a], ix[b]])
    return np.mean(v)
def leaves_of(seq):
    out = []
    for p in seq:
        L = int(p[:-1])
        if not out or out[-1] != L: out.append(L)
    return out
def stack_score(Ls, LM):
    return sum(np.corrcoef(LM[a].ravel(), LM[b].ravel())[0, 1] for a, b in zip(Ls, Ls[1:]))
def space(sh):
    n = len(sh); out = []
    for o in itertools.permutations(range(n)):
        for fl in itertools.product([0, 1], repeat=n):
            s = [sh[i] if not f else sh[i][::-1] for i, f in zip(o, fl)]
            nestL = [x[0] for x in s] + [x[1] for x in reversed(s)]
            singL = [y for x in s for y in x]
            out.append(('nest', nestL)); out.append(('sing', singL))
    return out
def pages_of(Ls): return [f'{L}{s}' for L in Ls for s in 'rv']
QSH = {'13': [(75, 84), (76, 83), (77, 82), (78, 81), (79, 80)],
       '20': [(103, 116), (104, 115), (105, 114), (106, 113), (107, 112), (108, 111)]}
LMs = {'P80': {L: leafmap(L, 'P80', 6) for L in range(75, 117) if leafmap(L, 'P80', 6) is not None},
       'B': {L: leafmap(L, 'B', 6) for L in range(75, 117) if leafmap(L, 'B', 6) is not None}}
res = {}
for q, sh in QSH.items():
    sp = space(sh)
    ref_text = {m: np.array([text_score(pages_of(Ls), S) for _, Ls in sp]) for m, S in SIM.items()}
    ref_stain = {k: np.array([stack_score(Ls, LM) for _, Ls in sp]) for k, LM in LMs.items()}
    print(f'\n=== Quire {q}: reference space {len(sp)} arrangements (all nestings + singulion stacks, all sheet orders and orientations)')
    print(f'{"proposal":12s} {"kind":9s} {"evidence":32s} | text pct LSA (same kind) | TF-IDF (same kind) | stain pct bright | stain pct yellow')
    for pid, seq in props.items():
        if not pid.startswith(f'Q{q}-'): continue
        Ls = leaves_of(seq); kind = meta[pid]['kind']
        # physical stack: for 'singulion' the stack is X,Y per sheet in sequence; for 'leaves' the given leaf order
        out = []
        kmask = np.array([k == ('sing' if kind == 'singulion' else 'nest') for k, _ in sp])
        for m, S in SIM.items():
            s = text_score(seq, S); out.append(np.mean(ref_text[m][kmask] >= s))
        for k, LM in LMs.items():
            s = stack_score(Ls, LM); out.append(np.mean(ref_stain[k] >= s))
            if pid.endswith('CURRENT'): print(f'   {pid} {k}: rank {int(np.sum(ref_stain[k] > s))+1} of {len(sp)}')
        res[pid] = out
        print(f'{pid:12s} {kind:9s} {meta[pid]["evidence_type"][:32]:32s} | ' + ' | '.join(f'{x:.3f}' for x in out))
print('\n(pct = share of all arrangements scoring at least as well; small = good fit; 0.5 = typical)')
json.dump(res, open('t8_res.json', 'w'))
