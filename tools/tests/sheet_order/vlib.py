import json, re, itertools
from collections import Counter, defaultdict
import numpy as np

def load(path='pages2.json'):
    P = json.load(open(path))
    for p in P:
        p['words'] = [w for l in p['lines'] for w in l['w']]
    return P

def structure(P):
    """sheets: (Q,B) -> (X,Y) leaves; leafinfo"""
    leafq = {}
    for p in P: leafq.setdefault(p['leaf'], (p.get('Q'), p.get('B'), p.get('F')))
    sh = defaultdict(set)
    for L, (q, b, f) in leafq.items(): sh[(q, b)].add(L)
    sheets = {k: tuple(sorted(v)) for k, v in sh.items()}
    return sheets, leafq

def stopwords(P, w=6, v=3.0):
    tf = Counter(x for p in P for x in p['words'])
    f = [c for _, c in tf.most_common()]
    x = 0
    while True:
        win = f[x:x + w]
        d = np.mean(-np.diff(win))
        if d < v: break
        x += 1
    n = w + x - 1
    return set(t for t, _ in tf.most_common(n))

def tfidf_matrix(docs, vocab=None, sublinear=True):
    if vocab is None:
        vocab = sorted({w for d in docs for w in d})
    V = {w: i for i, w in enumerate(vocab)}
    X = np.zeros((len(docs), len(V)))
    for i, d in enumerate(docs):
        for w, c in Counter(d).items():
            if w in V: X[i, V[w]] = c
    df = (X > 0).sum(0); df[df == 0] = 1
    idf = np.log(len(docs) / df)
    M = (np.log1p(X) if sublinear else X) * idf
    return M, V, idf, X

def cos_sim(M):
    n = np.linalg.norm(M, axis=1, keepdims=True); n[n == 0] = 1
    A = M / n; return A @ A.T

def lsa_space(P, k=75, chunk=40, minlen=20, stop=None):
    """Layfield&Davis-style: per page and unit type, ~40-word documents; TF-IDF; SVD rank k.
    Returns function mapping a word list -> k-dim vector (fold-in scaled by S, i.e. U_k^T d)."""
    docs = []
    for p in P:
        byu = defaultdict(list)
        for l in p['lines']:
            byu[l['u']].extend([w for w in l['w'] if w not in stop])
        for u, ws in byu.items():
            if len(ws) < minlen: continue
            nd = max(1, round(len(ws) / chunk)); sz = len(ws) / nd
            for i in range(nd):
                docs.append(ws[int(i * sz):int((i + 1) * sz)])
    vocab = sorted({w for d in docs for w in d})
    V = {w: i for i, w in enumerate(vocab)}
    A = np.zeros((len(V), len(docs)))
    for j, d in enumerate(docs):
        for w, c in Counter(d).items(): A[V[w], j] = c
    df = (A > 0).sum(1); idf = np.log(len(docs) / df)
    W = A * idf[:, None]
    U, s, Vt = np.linalg.svd(W, full_matrices=False)
    Uk = U[:, :k]
    def vec(words):
        d = np.zeros(len(V))
        for w, c in Counter(words).items():
            if w in V: d[V[w]] = c
        d = d * idf
        return d @ Uk      # = (d^T U S^-1) S
    return vec, len(docs)

def page_sim(P, keys, metric, stop=None, lsa=None):
    words = {p['page']: p['words'] for p in P}
    if metric == 'tfidf':
        docs = [words[k] for k in keys]
        M, *_ = tfidf_matrix(docs); return cos_sim(M)
    if metric == 'lsa':
        vec = lsa
        M = np.array([vec([w for w in words[k] if w not in stop]) for k in keys]); return cos_sim(M)
    if metric == 'jaccard':
        sets = [set(words[k]) for k in keys]
        n = len(keys); S = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                S[i, j] = len(sets[i] & sets[j]) / max(1, len(sets[i] | sets[j]))
        return S
