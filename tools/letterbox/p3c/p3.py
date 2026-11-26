"""P3 analysis (PREREG.md). python -I p3.py <feat dir> <out dir> [nperm]"""
import json, sys
from collections import defaultdict, Counter
from pathlib import Path
import numpy as np
from joblib import Parallel, delayed
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold
D, OUT = Path(sys.argv[1]), Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
NPERM = int(sys.argv[3]) if len(sys.argv) > 3 else 200
R = json.load(open(D / 'glyphs.json')); HG = np.load(D / 'hog.npy').astype(np.float32)
GEO = ['height', 'width', 'aspect', 'area', 'ncomp', 'thick', 'crossbar', 'tail_w']          # shape only (classifier)
PLACE = ['top_ext', 'bot_ext', 'left_ext', 'right_ext', 'dx', 'dy', 'tone', 'box_w', 'box_h']  # placement / ink / box (reported, not classified)
out = []
P = lambda *a: (print(*a, flush=True), out.append(' '.join(str(x) for x in a)))
GEOX = np.array([[r[k] for k in GEO] for r in R], np.float32)
XALL = np.hstack([HG, GEOX])
import os
MINN = int(os.environ.get('P3_MINN', 80))
MATCH = ['box_w', 'box_h', 'box_dy']
BAL = {}


def arms():
    """index lists per arm: (target group, comparison group). Paragraph-start lines and lines with < 4 words excluded."""
    A = defaultdict(list)
    for i, r in enumerate(R):
        if r['pstart'] or r['nw'] < 4: continue
        wi, nw, gi, wl = r['wi'], r['nw'], r['gi'], r['wl']
        if gi == 0:
            if wi == 0: A['L'].append(i)
            elif wi == 1: A['W2'].append(i)
            elif wi <= nw - 2: A['M'].append(i)
        if gi == wl - 1 and wl >= 2:
            if wi == nw - 1: A['RL'].append(i)
            elif wi == nw - 2: A['RP'].append(i)
            elif 1 <= wi <= nw - 3: A['RM'].append(i)
    return A


A = arms()
P('group sizes', {k: len(v) for k, v in A.items()})


def build(tgt, cmp_, classes=None, rng=None):
    rng = np.random.default_rng(1) if rng is None else rng
    """returns idx, y, cls, page; comparison capped at 3x target per class."""
    ct = Counter(R[i]['g'] for i in A[tgt]); cc = Counter(R[i]['g'] for i in A[cmp_])
    if classes is None: classes = sorted(g for g in ct if ct[g] >= MINN and cc[g] >= MINN)
    idx, y = [], []
    for g in classes:
        t = [i for i in A[tgt] if R[i]['g'] == g]; c = [i for i in A[cmp_] if R[i]['g'] == g]
        # P3-b: 1:1 placement matching on box width, box height, box vertical offset (sd units within class),
        # greedy nearest neighbour without replacement in random target order, caliper 0.5 sd (Euclidean)
        F = np.array([[R[i][k] for k in MATCH] for i in t + c], float); F = (F - F.mean(0)) / (F.std(0) + 1e-9)
        Ft, Fc = F[:len(t)], F[len(t):]; free = np.ones(len(c), bool); tt, cc = [], []
        for j in rng.permutation(len(t)):
            if not free.any(): break
            dd = np.linalg.norm(Fc - Ft[j], axis=1); dd[~free] = np.inf; k = int(np.argmin(dd))
            if dd[k] <= 0.5: tt.append(t[j]); cc.append(c[k]); free[k] = False
        BAL.setdefault((tgt, cmp_), {})[g] = (len(t), len(tt), np.round(np.abs(np.array([[R[i][k] for k in MATCH] for i in tt]).mean(0) - np.array([[R[i][k] for k in MATCH] for i in cc]).mean(0)) / (F.std(0) + 1e-9), 3).tolist() if tt else None)
        idx += tt + cc; y += [1] * len(tt) + [0] * len(cc)
    idx = np.array(idx, dtype=int); y = np.array(y, dtype=int)
    return idx, y, np.array([R[i]['g'] for i in idx]), np.array([R[i]['page'] for i in idx]), classes


def oof(X, y, cls, page):
    s = np.full(len(y), np.nan)
    for c in set(cls):
        m = cls == c; Xi, yi, gi = X[m], y[m], page[m]; si = np.full(m.sum(), np.nan)
        k = min(5, len(set(gi)))
        for tr, te in GroupKFold(k).split(Xi, yi, gi):
            if len(set(yi[tr])) < 2: continue
            mu, sd = Xi[tr].mean(0), Xi[tr].std(0) + 1e-6
            lr = LogisticRegression(C=0.05, max_iter=3000, class_weight='balanced').fit((Xi[tr] - mu) / sd, yi[tr])
            si[te] = lr.decision_function((Xi[te] - mu) / sd)
        s[m] = si
    return s


def pooled(s, y, cls, mask=None):
    num = den = 0.0; per = {}
    for c in sorted(set(cls)):
        m = (cls == c) & ~np.isnan(s)
        if mask is not None: m &= mask
        if len(set(y[m])) < 2 or min((y[m] == 1).sum(), (y[m] == 0).sum()) < 15: continue
        a = roc_auc_score(y[m], s[m]); w = (y[m] == 1).sum(); per[c] = (round(a, 3), int(w)); num += a * w; den += w
    return (num / den if den else float('nan')), per


def permuted(y, cls, page, seed):
    r = np.random.default_rng(seed); yp = y.copy(); st = defaultdict(list)
    for i, (c, p) in enumerate(zip(cls, page)): st[(c, p)].append(i)
    for ii in st.values():
        ii = np.array(ii); yp[ii] = r.permutation(y[ii])
    return yp


def run(tgt, cmp_, X, label, classes=None, nperm=NPERM):
    idx, y, cls, page, classes = build(tgt, cmp_, classes)
    s = oof(X[idx], y, cls, page); auc, per = pooled(s, y, cls)
    def one(k):
        yp = permuted(y, cls, page, 1000 + k); return pooled(oof(X[idx], yp, cls, page), yp, cls)[0]
    null = np.array(Parallel(n_jobs=8)(delayed(one)(k) for k in range(nperm))) if nperm else np.array([])
    p = (1 + (null >= auc).sum()) / (1 + len(null)) if nperm else float('nan')
    P(f'{label}: {tgt} vs {cmp_} pooled AUC {auc:.3f}  perm p {p:.4f}  null mean {null.mean() if nperm else float("nan"):.3f} '
      f'95th {np.percentile(null, 95) if nperm else float("nan"):.3f}  classes {per}')
    lang = np.array([R[i]['lang'] for i in idx]); scr = np.array([R[i]['scribe'] for i in idx])
    sub = {f'lang {l}': pooled(s, y, cls, lang == l) for l in ('A', 'B')}
    sub.update({f'scribe {h}': pooled(s, y, cls, scr == h) for h in ('1', '2', '3')})
    P('   subsets:', {k: round(v[0], 3) for k, v in sub.items()})
    return dict(auc=auc, p=p, per=per, null=null.tolist(), classes=classes, sub={k: v[0] for k, v in sub.items()}), (idx, y, cls, page, s)


def demean(v, groups, it=30):
    r = v.astype(float).copy()
    for _ in range(it):
        for g in groups:
            s = np.bincount(g, r); n = np.bincount(g); r -= (s / np.maximum(n, 1))[g]
    return r


def codes(v):
    u = {k: i for i, k in enumerate(sorted(set(v)))}; return np.array([u[k] for k in v])


def features(idx, y, label, nperm=1000):
    """per-feature effect in sd units, fixed effects (glyph x next glyph) and page; permutation within (glyph, page)."""
    cls = np.array([R[i]['g'] for i in idx]); page = np.array([R[i]['page'] for i in idx])
    nx = np.array([R[i]['g'] + '>' + (R[i]['nxt'] if label.startswith('L') or label.startswith('W') else R[i]['prv']) for i in idx])
    groups = [codes(nx), codes(page)]; res = {}
    rng = np.random.default_rng(7); st = defaultdict(list)
    for j, (c, p) in enumerate(zip(cls, page)): st[(c, p)].append(j)
    st = [np.array(v) for v in st.values()]
    for k in GEO + PLACE:
        v = np.array([R[i][k] for i in idx], float); v = (v - v.mean()) / (v.std() + 1e-9); rv = demean(v, groups)
        def b(yy):
            rx = demean(yy.astype(float), groups); return float(rx @ rv / (rx @ rx))
        b0 = b(y); null = []
        for _ in range(nperm):
            yp = y.copy()
            for ii in st: yp[ii] = rng.permutation(y[ii])
            null.append(b(yp))
        null = np.abs(np.array(null)); res[k] = (round(b0, 3), round(float((1 + (null >= abs(b0)).sum()) / (1 + nperm)), 4))
    P(f'   features {label} (sd, perm p):', res)
    return res


result = {}
geo_idx = list(range(HG.shape[1], XALL.shape[1]))
for tgt, cmp_, lab_ in [('L', 'M', 'P3-L'), ('W2', 'M', 'P3-L placebo (word 2)'), ('RL', 'RM', 'P3-R'), ('RP', 'RM', 'P3-R placebo (word n-1)')]:
    base = 'L' if tgt in ('L', 'W2') else 'R'
    cl = result.get(base, {}).get('classes')   # placebo uses the target arm's classes
    r, (idx, y, cls, page, s) = run(tgt, cmp_, XALL, lab_, cl)
    rg, _ = run(tgt, cmp_, XALL[:, geo_idx], lab_ + ' [geometry only]', cl, nperm=0)
    r['geo_auc'] = rg['auc']
    rh, _ = run(tgt, cmp_, XALL[:, :HG.shape[1]], lab_ + ' [HOG only]', cl, nperm=0)   # P3-c: pen form without mask extent
    r['hog_auc'] = rh['auc']
    try: r['features'] = features(idx, y, lab_, nperm=300)
    except Exception as ex: r['features'] = 'failed: %s' % ex
    result[tgt if tgt not in ('L', 'RL') else base] = r
    if tgt in ('L', 'RL'): result[base]['classes'] = r['classes']


def verdict(t, p_):
    a, pl = result[t], result[p_]
    ok = a['p'] < 0.01 and a['auc'] >= 0.53 and (pl['auc'] - 0.5) < 0.5 * (a['auc'] - 0.5)
    return 'PASS' if ok else 'FAIL'


result['verdict_L'] = verdict('L', 'W2'); result['verdict_R'] = verdict('R', 'RP')
result['balance'] = {f'{a}-{b}': v for (a, b), v in BAL.items()}
P('matching (n target, n matched, |std diff| box_w box_h box_dy):', result['balance'])
P('VERDICT P3-L (line-initial glyph drawn differently):', result['verdict_L'])
P('VERDICT P3-R (line-final glyph drawn differently):', result['verdict_R'])
json.dump(result, open(OUT / 'p3_result.json', 'w'), indent=1)
open(OUT / 'p3.out', 'w').write('\n'.join(out) + '\n')
