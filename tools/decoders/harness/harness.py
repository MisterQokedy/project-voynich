"""Calibrated decipherment harness. A key maps EVA glyph units -> plaintext strings ('' = dropped).
Metrics on mapped text (all vs a target-language corpus):
  M1 char 4-gram LM, bits/char incl. word end (lower = more language-like)
  M2 dictionary token hit rate (mapped tokens of length >= 3 that are corpus types with count >= 2)
  M4 attested-bigram rate: share of adjacent in-dictionary token pairs that occur as a bigram in the corpus"""
import json, re, math, random, collections
H = './work/decipherment_harness'
CORP = json.load(open(f'{H}/corpora.json'))
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|[a-z]')
def units(w): return tuple(GL.findall(re.sub(r'[^a-z]', '', w)))
class LM:
    def __init__(self, toks, n=4, d=0.75):
        self.n, self.d = n, d; self.c = [collections.Counter() for _ in range(n + 1)]; self.ctx = [collections.Counter() for _ in range(n + 1)]
        self.fol = [collections.defaultdict(set) for _ in range(n + 1)]
        tc = collections.Counter(toks); self.V = set('$')
        for w, k in tc.items():
            s = '^' * (n - 1) + w + '$'; self.V |= set(w)
            for i in range(n - 1, len(s)):
                for o in range(1, n + 1):
                    h = s[i - o + 1:i]; self.c[o][h + s[i]] += k; self.ctx[o][h] += k; self.fol[o][h].add(s[i])
        self.lex = {w for w, k in tc.items() if k >= 2}; self.cache = {}
        bg = collections.Counter(zip(toks, toks[1:])); self.bigr = {b for b, k in bg.items() if k >= 1}
    def p(self, h, ch):
        pr = 1.0 / (len(self.V) + 30)   # floor: uniform over a slightly larger alphabet
        for o in range(1, self.n + 1):
            hh = h[len(h) - o + 1:] if o > 1 else ''; t = self.ctx[o][hh]
            if t: pr = max(self.c[o][hh + ch] - self.d, 0) / t + self.d * len(self.fol[o][hh]) / t * pr
        return pr
    def wbits(self, w):
        if w in self.cache: return self.cache[w]
        s = '^' * (self.n - 1) + w + '$'; b = -sum(math.log2(self.p(s[i - self.n + 1:i], s[i])) for i in range(self.n - 1, len(s)))
        self.cache[w] = (b, len(w) + 1); return self.cache[w]
_LM = {}
def lm(lang):
    if lang not in _LM: _LM[lang] = LM(CORP[lang])
    return _LM[lang]
def apply(key, uw): return ''.join(key.get(u, '') for u in uw)
def score(key, lines, lang):
    """lines: list of lists of unit-tuples. Returns M1, M2, M4."""
    L = lm(lang); b = n = hit = el = pairs = att = 0; tc = collections.Counter(u for l in lines for u in l)
    mp = {u: apply(key, u) for u in tc}
    for u, k in tc.items():
        w = mp[u]
        if not w: continue
        bb, nn = L.wbits(w); b += k * bb; n += k * nn
        if len(w) >= 3: el += k; hit += k * (w in L.lex)
    for l in lines:
        ws = [mp[u] for u in l if mp[u]]
        for a, c in zip(ws, ws[1:]):
            if a in L.lex and c in L.lex: pairs += 1; att += (a, c) in L.bigr
    return dict(M1=b / max(n, 1), M2=hit / max(el, 1), M4=att / max(pairs, 1), npairs=pairs)
def fit_key(lines, lang, inv, vals, fixed=None, iters=2500, seed=0, top=2500):
    """Hill-climb a key (unit -> value from vals) minimising M1 on `lines`. `fixed` units are not changed."""
    r = random.Random(seed); L = lm(lang); fixed = fixed or {}
    tc = collections.Counter(u for l in lines for u in l).most_common(top)
    free = [u for u in inv if u not in fixed]; key = dict(fixed); key.update({u: r.choice(vals) for u in free})
    def obj(k):
        b = n = 0
        for u, c in tc:
            w = apply(k, u)
            if w: bb, nn = L.wbits(w); b += c * bb; n += c * nn
        drop = sum(c for u, c in tc if not apply(k, u))
        return b / max(n, 1) + 3.0 * drop / sum(c for _, c in tc)   # penalty: dropping whole words is not allowed to win
    cur = obj(key); T = 0.05
    for it in range(iters):
        u = r.choice(free); old = key[u]; key[u] = r.choice(vals); new = obj(key)
        if new <= cur or r.random() < math.exp((cur - new) / max(T * (1 - it / iters), 1e-4)): cur = new
        else: key[u] = old
    return key
# ---------- Voynich data and controls
D = json.load(open('./work/manuscript_wide/pages2.json'))
SP = json.load(open('./work/timm_generator/split.json'))
SHEET = [p['Q'] + p['B'] for p in D]; HALF = ['fit' if s in SP['fit'] else 'test' for s in SHEET]
VL = [[[units(w) for w in L['w']] for L in p['lines'] if L['w'] and L['u'] != 'L'] for p in D]
TIMM = {s: [[[units(w) for w in l] for l in p] for p in v] for s, v in json.load(open(f'{H}/timm_pages.json')).items()}
def leaf(i): return D[i]['leaf']
def lines_of(pages, idx): return [l for i in idx for l in pages[i] if l]
def wshuffle(lines, seed):
    """Glyph-shuffle inside each word (keeps glyph counts and word lengths, destroys word structure)."""
    r = random.Random(seed); out = []
    for l in lines:
        nl = []
        for u in l: u = list(u); r.shuffle(u); nl.append(tuple(u))
        out.append(nl)
    return out
def inventory(lines, mn=10):
    c = collections.Counter(g for l in lines for u in l for g in u); return [g for g, k in c.most_common() if k >= mn]
