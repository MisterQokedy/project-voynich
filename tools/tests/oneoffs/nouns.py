import sys, glob, os; sys.path.insert(0, './work/oneoffs/code')
from oo import *
RD = V + 'regional/comparison/raw/bundle8/ridges/'
WORKS = ['1482_vonMegenberg', '1487_vonCuba|1487_Cuba', '1532_Tallat', '1532_Brunfels', '1539_Bock', '1543_Fuchs', '1550_Schellenbe', '1557_vonBodenstein']
def load_work(pat):
    pages, cur, line = [], None, 0
    for f in sorted(glob.glob(RD + '*.tsv')):
        if f.endswith('.meta.tsv') or not re.search(pat, os.path.basename(f)): continue
        cur = dict(panel=os.path.basename(f), meta={}, toks=[], pos=[]); pages.append(cur); li = []
        for row in list(csv.reader(open(f, encoding='utf-8'), delimiter='\t'))[1:]:
            row += [''] * 13
            if row[8] == 'pb' and cur['toks']:
                cur = dict(panel=cur['panel'], meta={}, toks=[], pos=[]); pages.append(cur)
            w = re.sub(r'[^a-zäöüßæœſ]', '', row[2].lower())
            if row[7] == 'lb': line += 1; ipos = 0
            else: ipos = 1
            if not w or row[4].startswith('$'): continue
            cur['toks'].append((w, 'L' if row[10] == 'head' else 'P', '', str(line), ipos, 2)); cur['pos'].append(row[4])
    return [p for p in pages if p['toks']]
# fix ipos: line-first = first kept token after lb
def fixfirst(pages):
    for p in pages:
        last = None; T = []
        for t in p['toks']:
            T.append((t[0], t[1], t[2], t[3], 0 if t[3] != last else 1, 2)); last = t[3]
        p['toks'] = T
    return pages
def classify_n(pages, N):
    return classify(pages, freq_min=max(3, round(10 * N / 38600)))
def feats(pages):
    N = sum(len(p['toks']) for p in pages); rows, c, freq = classify_n(pages, N)
    T = [t for p in pages for t in p['toks']]; ml = np.mean([len(t[0]) for t in T])
    fr = [r for r in rows if r['cls'] == 'FREE']; e2 = [r for r in rows if r['cls'] == 'EDIT2']
    pairs = {(onset(f), ending(f)) for f in freq}
    nov = lambda R: np.mean([(onset(r['word']), ending(r['word'])) not in pairs for r in R]) if R else np.nan
    tok = lambda r: pages[r['pi']]['toks'][r['i']]
    def enr(sel):
        a = [r['cls'] == 'FREE' for r in rows if sel(tok(r))]; b = [r['cls'] == 'FREE' for r in rows if not sel(tok(r))]
        return (np.mean(a) / np.mean(b)) if len(a) >= 10 and np.mean(b) > 0 else np.nan
    longt = [t[0] for t in T if len(t[0]) >= 1.5 * ml]
    lt = [w for w in set(longt) if c[w] >= 2]
    pg = collections.defaultdict(set)
    for pi, p in enumerate(pages):
        for t in p['toks']: pg[t[0]].add(pi)
    return dict(F1=len(rows) / N, F2=len(fr) / len(rows), F3=np.mean([len(r['word']) for r in fr]) / ml, F4=nov(fr) - nov(e2),
                F5=enr(lambda t: t[4] == 0), F6=enr(lambda t: t[1] == 'L'), F7=np.mean([c[w] == 1 for w in longt]),
                F8=np.mean([len(pg[w]) == 1 for w in lt]) if lt else np.nan), rows
def window(pages, N, rng):
    T = [(pi, t) for pi, p in enumerate(pages) for t in p['toks']]; s = rng.randrange(0, len(T) - N); seg = T[s:s + N]
    out = collections.OrderedDict()
    for pi, t in seg: out.setdefault(pi, dict(panel=pages[pi]['panel'], meta=pages[pi]['meta'], toks=[]))['toks'].append(t)
    return list(out.values())
def shuffle(pages, rng):
    W = [t[0] for p in pages for t in p['toks']]; rng.shuffle(W); k = 0; out = []
    for p in pages:
        q = dict(p); q['toks'] = [] 
        for t in p['toks']: q['toks'].append((W[k],) + t[1:]); k += 1
        out.append(q)
    return out
rng = random.Random(7)
ZL = parse(V + 'transcriptions/ZL3b-n.txt'); GENS = [gen_pages(s) for s in range(900, 905)]
res = {}; KEYS = ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8']
print('Noun share (NN+NE) by one-off class, German:')
for pat in WORKS:
    P = fixfirst(load_work(pat)); N = sum(len(p['toks']) for p in P)
    f, rows = feats(P); allpos = [x for p in P for x in p['pos']]
    nn = lambda R: np.mean([P[r['pi']]['pos'][r['i']] in ('NN', 'NE') for r in R])
    cl = {k: [r for r in rows if r['cls'] == k] for k in ('FREE', 'EDIT2', 'EDIT1')}
    print('  %-22s N %5d  all %.2f  FREE %.2f  EDIT2 %.2f  EDIT1 %.2f   (latin share of FREE %.2f)' % (pat, N, np.mean([x in ('NN', 'NE') for x in allpos]), nn(cl['FREE']), nn(cl['EDIT2']), nn(cl['EDIT1']),
          0))
    vz = [feats(window(ZL, N, rng))[0] for _ in range(10)]; vg = [feats(window(GENS[k % 5], N, rng))[0] for k in range(10)]
    vs = [feats(shuffle(window(ZL, N, rng), rng))[0] for _ in range(5)]
    res[pat] = dict(DE=f, VOY={k: float(np.nanmedian([v[k] for v in vz])) for k in KEYS}, GEN={k: float(np.nanmedian([v[k] for v in vg])) for k in KEYS},
                    SHUF={k: float(np.nanmedian([v[k] for v in vs])) for k in KEYS}, N=N, nn=dict(all=float(np.mean([x in ('NN', 'NE') for x in allpos])), **{k: float(nn(v)) for k, v in cl.items()}))
print('\nProfiles (German work | Voynich windows of same N, median | GEN | token-shuffled Voynich):')
for k in KEYS:
    de = [res[w]['DE'][k] for w in WORKS]
    print('%s  DE %s | VOY %s | GEN %s | SHUF %s' % (k, ' '.join('%.2f' % x for x in de), ' '.join('%.2f' % res[w]['VOY'][k] for w in WORKS),
          ' '.join('%.2f' % res[w]['GEN'][k] for w in WORKS), ' '.join('%.2f' % res[w]['SHUF'][k] for w in WORKS)))
    lo, hi = np.nanmin(de), np.nanmax(de)
    inside = lambda src: np.mean([lo <= res[w][src][k] <= hi for w in WORKS])
    print('    inside German range: VOY %.2f  GEN %.2f  SHUF %.2f' % (inside('VOY'), inside('GEN'), inside('SHUF')))
json.dump(res, open(OUT + 'nouns.json', 'w'), indent=1, default=float)
