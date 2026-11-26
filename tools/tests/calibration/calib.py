"""Calibration of text-based sheet re-ordering on known texts (true order known).
Each text is cut into consecutive pages of W words; consecutive groups of 4 pages form a 'singulion' sheet
(Xr Xv Yr Yv read in sequence, exactly the Layfield & Davis model); n consecutive sheets form a quire.
For every quire window we search all n! sheet orders with the same objective as reorder2.py / lsa_reorder.py:
mean similarity of (last page of sheet i, first page of sheet i+1). Metrics: tfidf, jaccard, cosine_raw
(reorder2.py) and LSA (lsa_reorder.py: stop-word heuristic w=6 v=3, ~40-word docs, idf, SVD k=75, fold-in, cosine).
Also 'tfidf_sheet': whole-sheet vs whole-sheet tf-idf similarity (a more generous variant).
Per window we record: rank of the TRUE order among n!, whether best == true, share of true links kept in the best
order (chance = 1/n), and the shuffled-page null p for best-minus-median (the test applied to the Voynich).
MODE run: text runs across page breaks (cut every W words). MODE aligned: every page starts a new unit (recipe, herb
entry, numbered section), units packed whole up to W words, nothing crosses a page break (overflow dropped), like a
Voynich page whose paragraphs end on the page.
Usage: calib.py texts.json MODE W n stride nnull out.json [texts,comma,separated]"""
import json, sys, itertools
import numpy as np
from collections import Counter

J = json.load(open(sys.argv[1])); MODE = sys.argv[2]; W = int(sys.argv[3]); n = int(sys.argv[4]); stride = int(sys.argv[5])
NNULL = int(sys.argv[6]); OUT = sys.argv[7]
SCR = MODE.endswith('_scr'); MODE = MODE.replace('_scr', '')   # _scr: sheets randomly permuted across the whole text (no true order: false-positive check)
texts = J['stream'] if MODE == 'run' else J['units']
only = sys.argv[8].split(',') if len(sys.argv) > 8 else list(texts)
rng = np.random.default_rng(11)
ORD = np.array(list(itertools.permutations(range(n))))          # n! x n
A_, B_ = ORD[:, :-1], ORD[:, 1:]
TRUE = ORD.tolist().index(list(range(n)))

def all_scores(T):  # T[a,b] = sim(last page of a, first page of b)
    return T[A_, B_].mean(1)

def cosm(X, Y):
    X = X / np.maximum(np.linalg.norm(X, axis=1, keepdims=True), 1e-12)
    Y = Y / np.maximum(np.linalg.norm(Y, axis=1, keepdims=True), 1e-12)
    return X @ Y.T

def jacm(X, Y):
    X = (X > 0).astype(float); Y = (Y > 0).astype(float); inter = X @ Y.T
    return inter / (X.sum(1)[:, None] + Y.sum(1)[None, :] - inter)

def paginate(T):
    if MODE == 'run': return [T[i:i + W] for i in range(0, len(T) - W + 1, W)]
    pages, cur = [], []
    for u in T:
        if cur and len(cur) + len(u) > W and len(cur) >= W // 2: pages.append(cur); cur = []
        cur = (cur + u)[:W]
        if len(cur) >= W: pages.append(cur); cur = []
    return pages

def build(words):
    pages = paginate(words)
    npg = len(pages) // 4 * 4; pages = pages[:npg]
    if SCR:
        perm = np.random.default_rng(99).permutation(npg // 4); pages = [pages[4 * s + j] for s in perm for j in range(4)]
    vocab = {w: i for i, w in enumerate(sorted(set(w for p in pages for w in p)))}
    X = np.zeros((npg, len(vocab)))
    for i, p in enumerate(pages):
        for w, c in Counter(p).items(): X[i, vocab[w]] = c
    df = (X > 0).sum(0); idf = np.log(npg / df)
    R = {'tfidf': np.log1p(X) * idf, 'cosine_raw': X, 'jaccard': X}
    # LSA as in lsa_reorder.py, semantic space built from this whole text
    tf = Counter(w for p in pages for w in p); srt = [c for _, c in tf.most_common()]; x = 0
    while np.mean(-np.diff(srt[x:x + 6])) >= 3: x += 1
    stop = {w for w, _ in tf.most_common(6 + x - 1)}
    docs = []
    for p in pages:
        ws = [w for w in p if w not in stop]; nd = max(1, round(len(ws) / 40))
        b = np.linspace(0, len(ws), nd + 1).astype(int); docs += [ws[b[i]:b[i + 1]] for i in range(nd)]
    lv = {w: i for i, w in enumerate(sorted({w for d in docs for w in d}))}
    A = np.zeros((len(lv), len(docs)))
    for j, d in enumerate(docs):
        for w, c in Counter(d).items(): A[lv[w], j] = c
    ldf = (A > 0).sum(1); keep = ldf >= 2            # L&D: terms need df >= 2
    A = A[keep]; lidf = np.log(len(docs) / ldf[keep]); lv = {w: i for i, w in enumerate(np.array(sorted(lv, key=lv.get))[keep])}
    U, S, Vt = np.linalg.svd(A * lidf[:, None], full_matrices=False); Uk = U[:, :75]
    D = np.zeros((npg, len(lv)))
    for i, p in enumerate(pages):
        for w, c in Counter(w for w in p if w not in stop).items():
            if w in lv: D[i, lv[w]] = c
    R['lsa'] = (D * lidf) @ Uk
    info = dict(mean_page=float(np.mean([len(p) for p in pages])), pages=npg, sheets=npg // 4, stop=len(stop), docs=len(docs), lsa_terms=len(lv))
    return R, info

def simf(m): return jacm if m == 'jaccard' else cosm

def eval_window(R, m, s0):
    sheets = list(range(s0, s0 + n))
    if m == 'tfidf_sheet':
        M = R['tfidf']; SV = np.stack([M[4 * s:4 * s + 4].sum(0) for s in sheets]); T = cosm(SV, SV)
        first = last = None
    else:
        M = R[m]; first = M[[4 * s for s in sheets]]; last = M[[4 * s + 3 for s in sheets]]; T = simf(m)(last, first)
    sc = all_scores(T); top = np.flatnonzero(sc >= sc.max() - 1e-12); best = int(rng.choice(top))   # random tie-break
    rank_true = float((sc > sc[TRUE] + 1e-12).sum() + 1 + 0.5 * ((np.abs(sc - sc[TRUE]) <= 1e-12).sum() - 1))  # mid-rank on ties
    bo = ORD[best]; links = sum(1 for i in range(n - 1) if bo[i + 1] == bo[i] + 1) / (n - 1)
    out = dict(rank_true=rank_true, top1=bool(best == TRUE), links=links, gain=float(sc.max() - np.median(sc)))
    if NNULL and first is not None:
        slots = np.vstack([first, last]); f = simf(m); null = np.empty(NNULL)
        for r in range(NNULL):
            pm = rng.permutation(2 * n); s2 = all_scores(f(slots[pm[n:]], slots[pm[:n]]))
            null[r] = s2.max() - np.median(s2)
        out['p_null'] = float((1 + (null >= out['gain']).sum()) / (NNULL + 1))
    return out

res = {}
for name in only:
    R, info = build(texts[name]); ns = info['sheets']
    wins = list(range(0, ns - n + 1, stride))
    res[name] = dict(info=info, windows=len(wins), independent=ns // n, metrics={})
    for m in ['tfidf', 'jaccard', 'cosine_raw', 'lsa', 'tfidf_sheet']:
        rows = [eval_window(R, m, s0) for s0 in wins]
        res[name]['metrics'][m] = rows
        rk = np.array([r['rank_true'] for r in rows]); N = len(ORD)
        ps = np.array([r['p_null'] for r in rows if 'p_null' in r])
        print(f"{name:16s} {MODE[:3]}{'-SCR' if SCR else ''} W={W} n={n} {m:11s} win={len(rows):3d} (indep {ns//n:2d}) top1={np.mean([r['top1'] for r in rows]):.2f} "
              f"(chance {1/N:.4f}) median rank of true {np.median(rk):.0f}/{N} (chance {(N+1)/2:.0f}) "
              f"true in top5% {np.mean(rk <= 0.05*N):.2f} links {np.mean([r['links'] for r in rows]):.2f} (chance {1/n:.2f})"
              + (f" | null p<0.06: {np.mean(ps < 0.06):.2f}, p<0.05: {np.mean(ps < 0.05):.2f}" if len(ps) else ''), flush=True)
json.dump(dict(mode=MODE, scrambled=SCR, W=W, n=n, stride=stride, nnull=NNULL, results=res), open(OUT, 'w'))
