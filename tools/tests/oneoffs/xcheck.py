import sys; sys.path.insert(0, './work/oneoffs/code')
from oo import *
P = parse(V + 'transcriptions/ZL3b-n.txt'); rows, c, freq = classify(P)
def keyed(P, rows):
    m = {}
    for r in rows:
        p = P[r['pi']]; t = p['toks'][r['i']]; m[(p['panel'], t[3], t[4], t[5])] = r
    return m
zl = keyed(P, rows)
for nm in ('IT2a-n', 'RF1b-e'):
    Q = parse(V + f'transcriptions/{nm}.txt'); qr, qc, qf = classify(Q)
    allq = {(p['panel'], t[3], t[4], t[5]): t[0] for p in Q for t in p['toks']}
    qk = keyed(Q, qr)
    tab = collections.Counter(); n = 0
    for k, r in zl.items():
        if k not in allq: continue
        w2 = allq[k]; n += 1
        st = qk[k]['cls'] if k in qk else ('not-hapax' if qc[w2] > 1 else '?')
        tab[(r['cls'], st)] += 1; tab[(r['cls'], 'same' if w2 == r['word'] else 'diff')] += 1
    print(f'\n{nm}: hapax share {len(qr)/sum(len(p["toks"]) for p in Q):.3f}, classes', dict(collections.Counter(r["cls"] for r in qr)), f'; ZL hapaxes matched: {n}')
    for a in ('FREE', 'EDIT2', 'EDIT1'):
        tot = sum(tab[(a, b)] for b in ('FREE', 'EDIT2', 'EDIT1', 'not-hapax'))
        print('  ZL %-5s -> ' % a + '  '.join('%s %.3f' % (b, tab[(a, b)] / tot) for b in ('FREE', 'EDIT2', 'EDIT1', 'not-hapax')) + f'   same word {tab[(a,"same")]/tot:.3f}  (n {tot})')
# X2 collapse a/o r/s
Pc = parse(V + 'transcriptions/ZL3b-n.txt', collapse=True); rc, cc, fc = classify(Pc)
kc = keyed(Pc, rc); tab = collections.Counter()
for k, r in zl.items():
    st = kc[k]['cls'] if k in kc else 'not-hapax'; tab[(r['cls'], st)] += 1
print('\nX2 a->o, r->s collapsed: hapax', len(rc), dict(collections.Counter(r['cls'] for r in rc)))
for a in ('FREE', 'EDIT2', 'EDIT1'):
    tot = sum(v for (x, _), v in tab.items() if x == a)
    print('  ZL %-5s -> ' % a + '  '.join('%s %.3f' % (b, tab[(a, b)] / tot) for b in ('FREE', 'EDIT2', 'EDIT1', 'not-hapax')))
# length-matched structure (exploratory, added after seeing FREE are longer)
M = Tri([w for w, n in c.items() if n >= 2])
out = collections.defaultdict(dict)
G = []; 
for s in range(900, 905):
    g = gen_pages(s); gr, gc, gf = classify(g); gm = Tri([w for w, n in gc.items() if n >= 2])
    G += [(r['word'], r['cls'], f) for r, f in zip(gr, struct_feats([r['word'] for r in gr], gf, gm))]
RF = [(r['word'], r['cls'], f) for r, f in zip(rows, struct_feats([r['word'] for r in rows], freq, M))]
print('\nLength-matched (len 7-10 pooled with per-length weights equal to real FREE) lp / recomb / oe / rare:')
lens = collections.Counter(len(w) for w, cl, f in RF if cl == 'FREE')
def wmean(S, key):
    tot = 0; W = 0
    for L in range(7, 11):
        v = [f[key] for w, cl, f in S if len(w) == L]
        if v: tot += lens[L] * np.mean(v); W += lens[L]
    return tot / W
for nm, S in (('real FREE', [x for x in RF if x[1] == 'FREE']), ('real EDIT2', [x for x in RF if x[1] == 'EDIT2']), ('real EDIT1', [x for x in RF if x[1] == 'EDIT1']),
              ('GEN FREE', [x for x in G if x[1] == 'FREE']), ('GEN EDIT2', [x for x in G if x[1] == 'EDIT2'])):
    print('  %-11s n %5d  ' % (nm, sum(7 <= len(x[0]) <= 10 for x in S)) + '  '.join('%s %.3f' % (k, wmean(S, k)) for k in ('lp', 'recomb', 'oe', 'rare', 'run3')))
print('\nFREE share by length, real vs GEN:')
for L in range(4, 13):
    a = [cl == 'FREE' for w, cl, f in RF if len(w) == L]; b = [cl == 'FREE' for w, cl, f in G if len(w) == L]
    print('  len %2d real %.3f (n %4d)  GEN %.3f (n %5d)' % (L, np.mean(a) if a else 0, len(a), np.mean(b) if b else 0, len(b)))
print('\nHapax share of tokens by length, real vs GEN:')
TR = collections.Counter(len(t[0]) for p in P for t in p['toks']); HR = collections.Counter(len(r['word']) for r in rows)
TG = collections.Counter(); HG = collections.Counter(len(w) for w, cl, f in G)
for s in range(900, 905): TG.update(len(t[0]) for p in gen_pages(s) for t in p['toks'])
print('  ' + '  '.join('%d: %.3f/%.3f' % (L, HR[L] / TR[L], HG[L] / TG[L]) for L in range(3, 13)))
