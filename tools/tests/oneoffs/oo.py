"""OO: one-off (hapax) words, EDIT vs FREE split, structure and cluster tests. See ../PREREG.md."""
import re, json, random, collections, csv, sys
import numpy as np
from rapidfuzz.distance import Levenshtein
from rapidfuzz import process
V = './work/'
OUT = V + 'oneoffs/'
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.')

def parse(fn, collapse=False):
    """-> list of pages: dict(panel, meta, toks=[(word, unit, locus, lineid, pos_in_line, nline)])"""
    pages, cur = [], None
    for line in open(fn, encoding='latin-1'):
        m = re.match(r'<(f\w+)>\s*<!(.*)>', line)
        if m:
            meta = dict(re.findall(r'\$(\w)=(\w+)', m.group(2)))
            cur = dict(panel=m.group(1), meta=meta, toks=[]); pages.append(cur); continue
        m = re.match(r'<(f\w+)\.(\w+),.(\w)(\w*)>\s+(.*)', line)
        if not m or cur is None: continue
        t = m.group(5).strip()
        t = t.replace('<->', '.')
        t = re.sub(r'\[([^:\]]*)(:[^\]]*)?\]', r'\1', t)
        t = re.sub(r'<[^>]*>', '', t); t = re.sub(r'[{}]', '', t)
        ws = [w for w in re.split(r'[.,\s]+', t) if w]
        ok = [w for w in ws if re.fullmatch(r'[a-z]+', w)]
        if len(ok) != len(ws):  # keep only clean words, but remember positions
            pass
        n = len(ws)
        for i, w in enumerate(ws):
            if not re.fullmatch(r'[a-z]+', w): continue
            if collapse: w = w.replace('a', 'o').replace('r', 's')
            cur['toks'].append((w, m.group(3), m.group(3) + m.group(4), m.group(2), i, n))
    return [p for p in pages if p['toks']]

def gen_pages(seed):
    G = json.load(open(V + f's6z/out/S6Z_reference/orig/gen_{seed}.json'))
    D = json.load(open(V + 'manuscript_wide/pages2.json'))
    out = []
    for slot, p in zip(D, G):
        toks = []
        for l in p:
            for i, w in enumerate(l): toks.append((w, 'P', 'P0', '0', i, len(l)))
        out.append(dict(panel='f' + slot['page'], meta=dict(I=slot.get('I',''), L=slot.get('L',''), H=slot.get('H','')), toks=toks))
    return [p for p in out if p['toks']]

def classify(pages, freq_min=10, win=40):
    allw = [t[0] for p in pages for t in p['toks']]
    c = collections.Counter(allw)
    freq = sorted([w for w, n in c.items() if n >= freq_min], key=lambda w: -c[w])
    rows = []
    hap = [(pi, i) for pi, p in enumerate(pages) for i, t in enumerate(p['toks']) if c[t[0]] == 1]
    hw = [pages[pi]['toks'][i][0] for pi, i in hap]
    D = process.cdist(hw, freq, scorer=Levenshtein.distance, dtype=np.int32, workers=-1)
    am = D.argmin(1)
    for k, (pi, i) in enumerate(hap):
        p = pages[pi]; w = p['toks'][i][0]
        df, sf = int(D[k, am[k]]), freq[am[k]]
        prev = [t[0] for t in p['toks'][max(0, i - win):i]]
        if prev:
            ds = [Levenshtein.distance(w, x) for x in prev]; j = int(np.argmin(ds)); dr, sr = ds[j], prev[j]
        else: dr, sr = 99, ''
        d = min(df, dr)
        cls = 'EDIT1' if d <= 1 else ('EDIT2' if d == 2 else 'FREE')
        rows.append(dict(pi=pi, i=i, word=w, cls=cls, d_freq=df, src_freq=sf, src_freq_n=c[sf], d_recent=dr, src_recent=sr,
                         src=(sf if df <= dr else sr)))
    return rows, c, freq

def onset(w): return GL.match(w).group(0)
def ending(w): return w[-2:]

class Tri:
    def __init__(s, types, k=0.1):
        s.c3 = collections.Counter(); s.c2 = collections.Counter(); s.A = set('$')
        for w in types:
            x = '^^' + w + '$'; s.A.update(w)
            for j in range(2, len(x)): s.c3[x[j-2:j+1]] += 1; s.c2[x[j-2:j]] += 1
        s.k = k; s.n = len(s.A)
    def lp(s, w):
        x = '^^' + w + '$'; t = 0
        for j in range(2, len(x)): t += np.log((s.c3[x[j-2:j+1]] + s.k) / (s.c2[x[j-2:j]] + s.k * s.n))
        return t / (len(w) + 1)

RARE = set('fgxbvjzump')
def comp(w):
    return dict(rare=sum(ch in RARE for ch in w) / len(w), irun=int(bool(re.search('iiii', w))), erun=int(bool(re.search('eee', w))),
                run3=int(bool(re.search(r'(.)\1\1', w))), length=len(w))

def recomb(w, P, S):
    return any(w[:i] in P and w[i:] in S for i in range(2, len(w) - 1))

def struct_feats(words, freq, model):
    P = {f[:i] for f in freq for i in range(2, len(f) + 1)}; S = {f[i:] for f in freq for i in range(0, len(f) - 1)}
    pairs = {(onset(f), ending(f)) for f in freq}
    out = []
    for w in words:
        d = comp(w); d['lp'] = model.lp(w); d['recomb'] = int(recomb(w, P, S)); d['oe'] = int((onset(w), ending(w)) in pairs)
        out.append(d)
    return out

def boot(x, n=1000, rng=np.random.default_rng(0)):
    x = np.asarray(x, float)
    if len(x) == 0: return (np.nan, np.nan, np.nan)
    b = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(n)]
    return (x.mean(), np.percentile(b, 2.5), np.percentile(b, 97.5))
