"""Shared fingerprint helpers extracted from p1.py (same code)."""
"""Step 1: gibberish vs Voynich fingerprint (see ../PREREG.md). Usage: p1.py GIBDIR MEANDIR > ../p1.out"""
import sys, os, re, glob, json, random, collections, math
import numpy as np
_pf = np.polyfit
def _safe(x, y, d):
    try: return _pf(x, y, d)
    except Exception: return np.array([np.nan, np.nan])
np.polyfit = _safe
sys.path.insert(0, './work/language_test/code'); sys.path.insert(0, './work/timm_generator/code')
from stats import stats
from common import VLINES, idx
import pos as P
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.')
def m2(lines, r, nsh=20):
    end = lambda w: w[-2:]; toks = [w for l in lines for w in l]
    top = {e for e, _ in collections.Counter(map(end, toks)).most_common(15)}
    E = [[end(w) if end(w) in top else '~' for w in l] for l in lines]
    c = collections.Counter(e for l in E for e in l); N = sum(c.values()); H = -sum(v / N * math.log2(v / N) for v in c.values())
    def mi(PP):
        pairs = [(l[i], l[i + 1]) for l in PP for i in range(len(l) - 1) if l[i] != l[i + 1]]; n = len(pairs)
        if not n: return 0
        pc = collections.Counter(pairs); a = collections.Counter(x for x, _ in pairs); b = collections.Counter(y for _, y in pairs)
        return sum(v / n * math.log2(v * n / (a[x] * b[y])) for (x, y), v in pc.items())
    sh = np.mean([mi([r.sample(l, len(l)) for l in E]) for _ in range(nsh)])
    return (mi(E) - sh) / max(H, 1e-9)
def h2g(toks, eva):
    if not eva: return stats.__globals__['H2'](toks)
    return stats.__globals__['H2'](['|'.join(GL.findall(w)) for w in toks]) if False else stats.__globals__['H2'](toks)
def fp(lines, r, eva):
    lines = [l for l in lines if l]
    n = sum(map(len, lines)); k = max(2, n // 100); pages, cur, c = [], [], 0
    for l in lines:
        cur.append(l); c += len(l)
        if c >= n / k and len(pages) < k - 1: pages.append(cur); cur, c = [], 0
    pages.append(cur); pages = [q for q in pages if q]
    while len(pages) > 2 and sum(map(len, pages[-1])) < 30: pages[-2] += pages.pop()
    s = stats(pages, r); T = [w for l in lines for w in l]
    if not eva: P.g = lambda w: list(w)
    else: P.g = lambda w: GL.findall(w)
    fi, fm, la, lm = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter(); li, lmid = [], []
    for l in lines:
        if len(l) < 3: continue
        G = [P.g(w) or ['?'] for w in l]; fi[G[0][0]] += 1; la[G[-1][-1]] += 1; li.append(len(G[0]))
        for q in G[1:-1]: fm[q[0]] += 1; lm[q[-1]] += 1; lmid.append(len(q))
    e = dict(E1=P.js(fi, fm), E2=P.js(la, lm), E3=np.mean(li) - np.mean(lmid))
    return dict(h2=s['S1_h2'], mlen=s['S2_meanlen'], sdlen=s['S3_sdlen'], ttr=len(set(T)) / len(T), orderMI=s['S6_orderMI'],
                near=s['S8_nearcopy'], lrep=s['S9_localrep'], imm=s['S10_immrep'], E1=e['E1'], E2=e['E2'], E3=e['E3'], M2=m2(lines, r))
KEYS = ['h2', 'mlen', 'sdlen', 'ttr', 'orderMI', 'near', 'lrep', 'imm', 'E1', 'E2', 'E3', 'M2']
clean = lambda s: [w for w in re.sub(r"[^a-zà-ÿ\s]", " ", s.lower()).split() if w]
def readlines(f, art=False):
    txt = open(f, encoding='utf-8', errors='ignore').read()
    L = [clean(l) for l in txt.splitlines()]; L = [l for l in L if l]
    if art or (L and np.mean([len(l) for l in L]) > 25):
        T = [w for l in L for w in l]; L = [T[k:k + 9] for k in range(0, len(T), 9)]
    return L
def cut(L, n):
    out, cur, c = [], [], 0
    for l in L:
        cur.append(l); c += len(l)
        if c >= n: out.append(cur); cur, c = [], 0
    return out
