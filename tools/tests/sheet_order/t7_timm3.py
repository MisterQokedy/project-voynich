"""Timm Experiment 3: seriate herbal bifolia on vocabulary WITHOUT <ed>/<dy> forms; test whether the held-out
<ed> rate varies monotonically along the recovered order, including inside the A and B blocks."""
import sys, re
import numpy as np
from scipy.stats import spearmanr
sys.path.insert(0, 'code'); from vlib import *
rng = np.random.default_rng(12)
P = load(); sheets, leafq = structure(P); pg = {p['page']: p for p in P}
recs = []
for (q, b), LL in sheets.items():
    if q not in 'ABCDEFG' or len(LL) != 2: continue
    ws = [w for L in LL for s in 'rv' for w in pg.get('%d%s' % (L, s), {'words': []})['words']]
    if len(ws) < 100: continue
    held = lambda w: 'ed' in w or w.endswith('dy')
    recs.append(dict(name=f'{LL[0]}/{LL[1]}', lang=pg['%dr' % LL[0]].get('L'), ed=np.mean([held(w) for w in ws]),
                     res=[w for w in ws if not held(w)]))
M, *_ = tfidf_matrix([r['res'] for r in recs]); S = cos_sim(M); np.fill_diagonal(S, 0)
D = np.diag(S.sum(1)); Lp = D - S
vals, vecs = np.linalg.eigh(Lp); f = vecs[:, 1]
order = np.argsort(f)
ed = np.array([recs[i]['ed'] for i in order]); lang = [recs[i]['lang'] for i in order]
rho = spearmanr(np.arange(len(ed)), ed).correlation
print(f'herbal sheets={len(recs)}; Fiedler order on residual vocab (no ed/dy forms)')
print(' order languages:', ''.join(lang))
print(' ed-rate along order:', ' '.join(f'{x:.2f}' for x in ed))
print(f' overall Spearman(position, ed-rate) = {rho:+.3f}')
for Lg in 'AB':
    idx = [k for k, l in enumerate(lang) if l == Lg]
    if len(idx) < 4: continue
    r = spearmanr(idx, ed[idx]).correlation
    null = [spearmanr(idx, rng.permutation(ed[idx])).correlation for _ in range(5000)]
    # sign expectation: same direction as overall
    s = np.sign(rho)
    p = (1 + np.sum(np.array(null) * s >= r * s)) / 5001
    print(f' within {Lg} block: n={len(idx)} Spearman={r:+.3f} p(same direction as overall)={p:.3f}')
# null for the whole thing: does the residual vocab alone separate A from B? (step) 
sep = np.mean([l == 'A' for l in lang[:len(lang)//2]])
print(f' share of A in first half of order: {sep:.2f}')
