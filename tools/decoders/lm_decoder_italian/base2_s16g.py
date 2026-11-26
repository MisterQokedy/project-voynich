"""S16b: frozen D1 decoder on Greshko's real N52 Naibbe tables (see PREREG.md).
Usage: s16b.py VARIANT GRESHKO_REPO out.json   VARIANT: macer | pliny | dante | macer_nospace | macer_shuf"""
import os, sys, json, time, random, unicodedata, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D1 = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'd1')
sys.path.insert(0, D1)
import cipher, metrics, sa_decoder as S
VAR, REPO = sys.argv[1], sys.argv[2]
R, ITERS, NG, T0, T1, WE = 16, 20_000_000, 3, 200.0, 1.0, 1.0      # calib_sa.py attempt 5 settings

# ---- his tables and rules (re-implemented from naibbe.py, N52) ----
GLY = {r['code'].lstrip('﻿'): r['glyphs'] for r in csv.DictReader(open(os.path.join(REPO, 'references/naibbe_tables.csv'), encoding='utf-8-sig'))}
UNI = {g for c, g in GLY.items() if c.startswith('unigram_')}
HIS = sorted({c.rsplit('_', 1)[1] for c in GLY})
WEIGHTS = {'alpha': 20, 'beta1': 8, 'beta2': 8, 'beta3': 8, 'gamma1': 4, 'gamma2': 4}
RESP = 17 / 36; DROP = 0.0 if VAR == 'macer_nospace' else 0.03
def clean(text):
    t = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    rep = {'æ': 'ae', 'Æ': 'ae', 'œ': 'oe', 'Œ': 'oe', 'ð': 'd', 'Ð': 'd', 'þ': 'th', 'Þ': 'th', 'ł': 'l', 'Ł': 'l', 'ß': 'ss', 'ø': 'o', 'Ø': 'o'}
    t = ''.join(rep.get(c, c) for c in t); t = ''.join(c for c in t if c.isalpha()).upper()
    return t.replace('W', 'UU').replace('J', 'I').replace('K', 'C').lower()
class Enc:
    def __init__(self, seed): self.r = random.Random(seed); self.deck = []; self.i = 0
    def card(self):
        if self.i >= len(self.deck):
            self.deck = [t for t, n in WEIGHTS.items() for _ in range(n)]; self.r.shuffle(self.deck); self.i = 0
        self.i += 1; return self.deck[self.i - 1]
    def units(self, text, start):
        """yield (unit, token) from text[start:], wrapping; respacing 17/36 unigram"""
        i = start
        while True:
            if i >= len(text) - 1: i = 0
            if self.r.random() < RESP: u = text[i]; i += 1
            else: u = text[i:i + 2]; i += 2
            if len(u) == 1: tok = GLY[f'unigram_{self.card()}_{u}']
            else:
                while True:
                    tok = GLY[f'prefix_{self.card()}_{u[0]}'] + GLY[f'suffix_{self.card()}_{u[1]}']
                    if tok not in UNI: break
            yield u, tok, i
def encrypt(text, shapes, seed, start=0):
    e = Enc(seed); g = e.units(text, start); out, truth = [], []; used = start
    for p in shapes:
        pq, pt = [], []
        for n in p:
            toks = [next(g) for _ in range(n)]; used = toks[-1][2] if toks else used
            line, tl = [toks[0][1]] if toks else [], [toks[0][0]] if toks else []
            for u, t, _ in toks[1:]:
                if e.r.random() < DROP: line[-1] += t; tl[-1] += u
                else: line.append(t); tl.append(u)
            pq.append(line); pt.append(tl)
        out.append(pq); truth.append(pt)
    return out, truth, used

# ---- plaintext and LM ----
lang = 'italian' if VAR in ('dante', 'itplain', 'dante_shuf') else (VAR if VAR in ('mhg', 'occitan') else 'latin')
C = json.load(open(os.path.join(D1, 'corpora', lang + '.json'), encoding='utf-8')); ALPHA = metrics.alphabet(C['lm']); A = len(ALPHA)
if VAR in ('macer', 'macer_nospace', 'macer_shuf', 'mhg', 'occitan', 'itplain'): raw = C['plain']
elif VAR == 'pliny': raw = open(os.path.join(REPO, 'input/examples/nathist_book16.txt'), encoding='utf-8').read()
else: raw = open(os.path.join(REPO, 'input/examples/divina_commedia.txt'), encoding='utf-8').read()
plain = ''.join(c for c in clean(raw) if c in ALPHA and c in HIS)
shF = cipher.shapes_of(cipher.V['fit']); shT = cipher.shapes_of(cipher.V['test'])
cF, tF, used = encrypt(plain, shF, seed=1); cT, tT, used2 = encrypt(plain, shT, seed=2, start=used)
wrap = used2 < used
if VAR in ('macer_shuf', 'dante_shuf'):   # token+truth pairs shuffled within FIT and within TEST (kills LM context, keeps emissions)
    def shuf(c, t, s):
        rr = random.Random(s); pairs = [(w, u) for p, q in zip(c, t) for l, m in zip(p, q) for w, u in zip(l, m)]; rr.shuffle(pairs); it = iter(pairs)
        cc = [[[None] * len(l) for l in p] for p in c]; tt = [[[None] * len(l) for l in p] for p in c]
        for pi, p in enumerate(c):
            for li, l in enumerate(p):
                for k in range(len(l)): cc[pi][li][k], tt[pi][li][k] = next(it)
        return cc, tt
    cF, tF = shuf(cF, tF, 5); cT, tT = shuf(cT, tT, 6)
t0 = time.time()
sF = S.strip_nulls(cF); sT = S.strip_nulls(cT); seg = S.Segmenter(sF)
truthF = [u for p in tF for l in p for u in l]; truthT = [u for p in tT for l in p for u in l]
toksT = [w for p in sT for l in p for w in l]
ok = kn = 0
for w, u in zip(toksT, truthT):
    a = seg.segment(w)
    if a is None: continue
    kn += 1; ok += (a[0] == 'W') == (len(u) == 1)
symix = {}; seq, _ = S.symbols(sF, seg, symix, grow=True); nsym = len(symix)
ptr, idx = S.positions(seq, nsym); lp = S.ngram_table(C['lm'], ALPHA, n=NG)
keys0 = S.freq_init(seq, nsym, C['lm'], ALPHA, R, seed=3)
print(f'{VAR}: plain {len(plain)} letters, wrap={wrap}, FIT tokens {len(truthF)}, TEST {len(truthT)}, merged FIT {sum(len(u) > 2 for u in truthF)}, symbols {nsym}, seg {time.time() - t0:.0f}s', flush=True)
