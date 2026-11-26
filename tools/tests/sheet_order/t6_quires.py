"""T6: are quires textual units beyond scribe/language? Does similarity decay with quire distance (current quire order)?"""
import sys, json, itertools
from collections import defaultdict
import numpy as np
sys.path.insert(0, 'code'); from vlib import *
rng = np.random.default_rng(3)
P = load(); sheets, leafq = structure(P); pg = {p['page']: p for p in P}
qorder = 'ABCDEFGHIJKLMNOQST'
recs = []
for (q, b), LL in sheets.items():
    if len(LL) != 2: continue
    ps = [pg[k] for k in ['%dr' % LL[0], '%dv' % LL[0], '%dr' % LL[1], '%dv' % LL[1]] if k in pg]
    ws = [w for p in ps for w in p['words']]
    if len(ws) < 80: continue
    hs = {p.get('H') for p in ps}; ls = {p.get('L') for p in ps}; il = ps[0].get('I')
    recs.append(dict(q=q, b=b, LL=LL, words=ws, H=sorted(hs, key=str)[0], L=sorted(ls, key=str)[0], sec=il, nest=int(b)))
M, *_ = tfidf_matrix([r['words'] for r in recs]); S = cos_sim(M)
def analyse(sel, label):
    n = len(sel); idx = np.array(sel)
    Q = np.array([qorder.index(recs[i]['q']) for i in sel])
    St = S[np.ix_(idx, idx)]; iu = np.triu_indices(n, 1)
    same = (Q[:, None] == Q[None, :])[iu]; d = np.abs(Q[:, None] - Q[None, :])[iu]; s = St[iu]
    obs = s[same].mean() - s[~same].mean()
    rq = np.corrcoef(d[~same], s[~same])[0, 1]
    nulls, nullr = [], []
    for _ in range(5000):
        Qp = rng.permutation(Q)
        sm = (Qp[:, None] == Qp[None, :])[iu]; dp = np.abs(Qp[:, None] - Qp[None, :])[iu]
        nulls.append(s[sm].mean() - s[~sm].mean()); nullr.append(np.corrcoef(dp[~sm], s[~sm])[0, 1])
    nulls, nullr = np.array(nulls), np.array(nullr)
    print(f' {label}: sheets={n} quires={len(set(Q))} | same-quire minus other-quire sim = {obs:+.4f} p={(1+np.sum(nulls>=obs))/5001:.4f} | corr(sim, quire distance) = {rq:+.3f} p(more negative)={(1+np.sum(nullr<=rq))/5001:.4f}')
print('== T6 quire coherence (sheet-level TF-IDF, quire labels permuted among sheets of same hand+language)')
herb = [i for i, r in enumerate(recs) if r['q'] in 'ABCDEFG']
analyse([i for i in herb if r_ok(i)] if False else [i for i in herb if recs[i]['H'] == '1'], 'Herbal hand 1 / Currier A (Q1-7)')
analyse([i for i in herb if recs[i]['H'] == '2'], 'Herbal hand 2 / Currier B (Q4-7)')
# leave-one-out nearest-quire assignment for hand-1 herbal sheets
sel = [i for i in herb if recs[i]['H'] == '1']
print('\n leave-one-out: mean similarity of each hand-1 herbal sheet to every quire (top = assigned)')
hits = 0
for i in sel:
    by = defaultdict(list)
    for j in sel:
        if j != i: by[recs[j]['q']].append(S[i, j])
    m = {q: np.mean(v) for q, v in by.items()}; best = max(m, key=m.get)
    hits += best == recs[i]['q']
    if best != recs[i]['q']:
        print(f'   sheet {recs[i]["LL"][0]}/{recs[i]["LL"][1]} (Q{recs[i]["q"]}) closest to Q{best} ({m[best]:.3f} vs own {m.get(recs[i]["q"], float("nan")):.3f})')
# null for hits
def hits_for(Q):
    h = 0
    for a, i in enumerate(sel):
        by = defaultdict(list)
        for b2, j in enumerate(sel):
            if j != i: by[Q[b2]].append(S[i, j])
        m = {q: np.mean(v) for q, v in by.items()}
        h += max(m, key=m.get) == Q[a]
    return h
Q0 = [recs[i]['q'] for i in sel]
nh = [hits_for(list(rng.permutation(Q0))) for _ in range(1000)]
print(f'   own quire is nearest for {hits}/{len(sel)} sheets; shuffled-label null mean {np.mean(nh):.1f}, p={(1+np.sum(np.array(nh)>=hits))/1001:.4f}')
