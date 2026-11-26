# D6: a real text carried in the frozen hybrid procedure's word choices (keys H and G), decoded back. See ../PREREG.md
import sys, json, hashlib, heapq, unicodedata, random, collections, itertools
sys.path.insert(0, './work/meaning_procedure/code')
from hybrid import *
P0 = json.load(open('./work/hybrid_gen/final_test.json'))['params']
for k in INTS: P0[k] = int(round(P0[k]))
ALPHA = 'abcdefghijklmnopqrstuvwxyz '
def clean(ws):
    s = ' '.join(ws).lower(); s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    s = ''.join(c if c in ALPHA else ' ' for c in s.replace('ß', 'ss').replace('ſ', 's')); return ' '.join(s.split())
SEC = json.load(open('./work/word_identity/texts/sections.json'))
COR = json.load(open('./work/decipherment_harness/corpora.json'))
PLAIN = {'latin_pliny_herbal': clean(SEC['pliny_herbal'] + SEC['pliny_garden']), 'italian_dante': clean(COR['italian']), 'mhg_megenberg_herbs': clean(SEC['meg_herbs'])}
def huffman(text):
    f = collections.Counter(text); h = [[c, i, {ch: ''}] for i, (ch, c) in enumerate(f.items())]; heapq.heapify(h); n = len(h)
    while len(h) > 1:
        a = heapq.heappop(h); b = heapq.heappop(h)
        d = {k: '0' + v for k, v in a[2].items()}; d.update({k: '1' + v for k, v in b[2].items()}); n += 1; heapq.heappush(h, [a[0] + b[0], n, d])
    return h[0][2]
def hdecode(bits, code):
    rev = {v: k for k, v in code.items()}; out = []; cur = ''
    for b in bits:
        cur += b
        if cur in rev: out.append(rev[cur]); cur = ''
    return ''.join(out)
# ---- keys
def keyH(b):
    return lambda w: int(hashlib.md5(('voy' + w).encode()).hexdigest(), 16) % (1 << b)
CELLM = collections.Counter((gg(w)[0], gg(w)[-1]) for p in FIp for l in p for w in l)
def keyG(b, seed=1):
    cells = list(CELLM.items()); random.Random(seed).shuffle(cells); cells.sort(key=lambda x: -x[1])
    mass = [0] * (1 << b); T = {}
    for c, m in cells:
        j = min(range(1 << b), key=lambda i: (mass[i], i)); T[c] = j; mass[j] += m
    return lambda w: T.get((gg(w)[0], gg(w)[-1]), 0)
VOC = list(WC)
def gen_stego(shapes, prm, seed, bins, b, bits):
    r = random.Random(seed); out = []; hist = []; pos = 0; nfb = 0; nslot = 0
    def need():
        nonlocal pos
        s = bits[pos:pos + b]
        if len(s) < b: s = s + '0' * (b - len(s))
        return int(s, 2)
    for p in shapes:
        q = []; page = list(hist[-prm['carry']:]) if prm['carry'] else []; pend = [split3(x)[2] for x in page]
        for li, l in enumerate(p):
            words = []
            for k in range(len(l)):
                def step():
                    if k == 0: return draw(dist(PGw if li == 0 else LIw, prm['tauL'], ('L', li == 0)), r)
                    prev = words[-1]; pd = onset_probs(prev, prm); src = page[-prm['W']:]
                    if prev in WBI and r.random() < prm['pw']:
                        w = draw(dist(WBI[prev], prm['tauw'], ('wb', prev)), r)
                        if r.random() < prm['mu'] * prm['mw']: w = mutate(w, r, prm)
                    elif src and r.random() < prm['pc']:
                        cand = [src[r.randrange(len(src))] for _ in range(prm['K'])]
                        wt = [(pd.get(gg(c)[0], 0) + 1e-4) ** prm['beta'] for c in cand]
                        w = r.choices(cand, wt)[0]
                        if r.random() < prm['mu']: w = mutate(w, r, prm)
                        if r.random() < 1 - prm['keepE']:
                            f, b_, e = split3(w); w = f + b_ + new_ending(b_, f, split3(prev)[2], r, prm)
                    else:
                        f = draw((list(pd), list(pd.values())), r); w = fresh(f, prev, page, pend, r, prm)
                    return w or prev
                if b == 0 or k == len(l) - 1:
                    w = step()
                else:
                    t = need(); nslot += 1; w = None
                    for _ in range(30 << b):
                        x = step()
                        if bins(x) == t: w = x; break
                    if w is None:
                        nfb += 1; pd = onset_probs(words[-1], prm) if words else {}
                        cand = [x for x in page[-prm['W']:] if bins(x) == t]
                        if not cand: cand = [x for x in VOC if bins(x) == t]
                        wt = [(pd.get(gg(c)[0], 0) + 1e-4) ** prm['beta'] * (WC.get(c, 0) + 1) for c in cand]
                        w = r.choices(cand, wt)[0]
                    pos += b
                words.append(w); page.append(w); pend.append(split3(w)[2])
            q.append(words)
        hist = page
        out.append(rule([q], prm['q'], r)[0] if prm['q'] > 0 else q)
    return out, nfb / max(nslot, 1), pos
def read_bits(pages, bins, b):
    return ''.join(format(bins(w), f'0{b}b') for p in pages for l in p for w in l[:-1])
def run(args):
    pname, key, b, seed = args
    txt = PLAIN[pname]; cut = int(0.6 * len(txt)); code = huffman(txt[:cut]); msg = txt[cut:]
    bits = ''.join(code[c] for c in msg if c in code)
    bins = (keyH(b) if key == 'H' else keyG(b)) if b else (lambda w: 0)
    pages, fb, used = gen_stego(TESTSH, P0, seed, bins, b, bits)
    g, ok, loss = score_on(pages, REF); n = int(sum(ok.values()))
    if b:
        rb = read_bits(pages, bins, b)[:used]; dec = hdecode(rb, code); ref = hdecode(bits[:used], code)
        acc = sum(x == y for x, y in zip(dec, ref)) / max(len(ref), 1); nlet = len(ref)
    else: acc, nlet = None, 0
    return dict(plain=pname, key=key, b=b, seed=seed, n=n, R_ok=bool(ok['R']), d1d2_ok=bool(ok['d1d2']), misses=[k for k in ok if not ok[k]], fallback=fb, acc=acc,
                letters=nlet, bits=used, sample=(hdecode(read_bits(pages, bins, b)[:400], code)[:80] if b else ''), stats={k: float(v) for k, v in g.items()})
if __name__ == '__main__':
    import multiprocessing as mp
    jobs = [(pn, 'H', 0, s) for pn in ['latin_pliny_herbal'] for s in range(900, 905)]
    jobs += [(pn, key, b, s) for b in (1, 2, 3, 4) for key in ('G', 'H') for pn in PLAIN for s in range(900, 905)]
    OUT = []
    with mp.Pool(3) as pool:
        for res in pool.imap_unordered(run, jobs):
            OUT.append(res)
            print(f"{res['plain']:20} key {res['key']} b {res['b']} seed {res['seed']}: {res['n']}/24 R {'ok' if res['R_ok'] else 'MISS'} d1d2 {'ok' if res['d1d2_ok'] else 'MISS'} acc {res['acc']} letters {res['letters']} fallback {res['fallback']:.3f} misses {res['misses']} | {res['sample'][:60]!r}", flush=True)
            json.dump(OUT, open('./work/meaning_procedure/d6.json', 'w'), indent=1)
