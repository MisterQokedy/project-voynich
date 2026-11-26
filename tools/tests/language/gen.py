"""Ciphers and generators. Imported by run.py."""
import re, random, collections
GL = re.compile(r'cth|ckh|cph|cfh|ch|sh|.')
def glyphs(w): return GL.findall(w)
# ---------- ciphers of Latin
def verbose_map(seed=1):
    r = random.Random(seed); units = ['o','e','y','a','d','l','r','k','ch','sh','in','iin','ee','ol','or','ar','al','qo','t','s','dy','ai','ok','ot','am','p','f','cth','ckh','eo','os','od']
    letters = 'eaitusrnomclpdbvqgfhxyjkzw'; r.shuffle(units)
    return {L: units[i % len(units)] for i, L in enumerate(letters)}
def cipher_verbose(pages, m):
    return [[[''.join(m.get(c, c) for c in w) for w in l] for l in p] for p in pages]
def cipher_sorted(pages):
    return [[[''.join(sorted(w)) for w in l] for l in p] for p in pages]
# ---------- Timm & Schinner self-citation
SUB = {'o':['a','y'], 'a':['o','y'], 'y':['o','a'], 'k':['t'], 't':['k'], 'p':['f'], 'f':['p'], 'ch':['sh'], 'sh':['ch'],
       'ckh':['cth'], 'cth':['ckh'], 'cph':['cfh'], 'cfh':['cph'], 'r':['l','s'], 'l':['r'], 's':['r','d'], 'd':['s'], 'e':['ee',''], 'i':['ii',''], 'n':['r']}
PRE = ['q', 'o', 'qo', 'ch', 'd', 'y', 's', 'sh']; SUF = ['y', 'dy', 'n', 'in', 'l', 'r', 'ey']
def mutate(w, r, rate):
    g = glyphs(w)
    while r.random() < rate:
        op = r.random()
        if op < 0.6:
            i = r.randrange(len(g));
            if g[i] in SUB: g[i] = r.choice(SUB[g[i]])
        elif op < 0.8:
            w0 = ''.join(g); have = [p for p in PRE if w0.startswith(p) and len(w0) > len(p) + 1]
            if have and r.random() < 0.5: g = glyphs(w0[len(r.choice(have)):])      # drop an existing prefix
            else: g = glyphs(r.choice(PRE)) + g
        else:
            w0 = ''.join(g); have = [x for x in SUF if w0.endswith(x) and len(w0) > len(x) + 1]
            if have and r.random() < 0.5: g = glyphs(w0[:-len(r.choice(have))])     # drop an existing suffix
            else: g = g + glyphs(r.choice(SUF))
        g = [x for x in g if x]
        if not g: g = ['o']
    return ''.join(g)
def timm(voy_pages, rate, seed=0, back=0.1):
    r = random.Random(seed); seedline = [w for l in voy_pages[0][:1] for w in l]
    LD = collections.Counter(len(w) for p in voy_pages for l in p for w in l); hist = []
    BG = collections.Counter(b for p in voy_pages for l in p for w in l for b in zip('^' + w, w + '$'))
    ok = lambda m: all(BG[b] >= 5 for b in zip('^' + m, m + '$'))     # only glyph pairs the Voynich itself uses
    out, prev = [], [seedline]
    for vp in voy_pages:                       # same page/line shape as the Voynich
        page = []
        for vl in vp:
            pool = [l for l in (page[-3:] if page else prev[-3:])]
            if hist and r.random() < back: pool = [r.choice(r.choice(hist))]   # occasional reach back to an earlier page
            line = []
            for j in range(len(vl)):
                src_line = r.choice(pool)
                w = src_line[min(j, len(src_line)-1) if r.random() < 0.5 else r.randrange(len(src_line))]
                m = mutate(w, r, rate)       # Metropolis step: word lengths keep the Voynich distribution
                if not ok(m) or r.random() > min(1, (LD.get(len(m), 0) / LD.get(len(w), 1)) ** 2): m = w
                line.append(m)
            page.append(line)
        out.append(page); prev = page; hist.append(page)
    return out
# ---------- Rugg table + grille
def rugg(voy_pages, rows, seed=0):
    r = random.Random(seed); W = [w for p in voy_pages for l in p for w in l]
    parts = [[], [], []]
    for w in W:
        g = glyphs(w); n = len(g)
        if n < 3: a, b = 0, n
        else: a, b = sorted(r.sample(range(1, n), 2))
        parts[0].append(''.join(g[:a])); parts[1].append(''.join(g[a:b])); parts[2].append(''.join(g[b:]))
    table = [[r.choice(parts[c]) for c in range(3)] for _ in range(rows)]
    out, pos = [], 0
    for vp in voy_pages:
        page = []
        for vl in vp:
            line = []
            for _ in vl:
                pos = (pos + r.randint(1, 3)) % rows          # grille slides down; holes sit at varying offsets
                w = table[pos][0] + table[(pos + r.randint(0, 4)) % rows][1] + table[(pos + r.randint(0, 4)) % rows][2]
                line.append(w or 'o')
            page.append(line)
        out.append(page)
    return out
