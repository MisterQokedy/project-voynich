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
