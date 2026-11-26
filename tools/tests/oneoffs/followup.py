"""Exploratory follow-up (after the pre-registered runs): does the FREE structure pattern survive removing line-first words and labels/circles?"""
import sys; sys.path.insert(0, './work/oneoffs/code')
from oo import *
P = parse(V + 'transcriptions/ZL3b-n.txt'); rows, c, freq = classify(P); M = Tri([w for w, n in c.items() if n >= 2])
F = struct_feats([r['word'] for r in rows], freq, M)
G = []
for s in range(900, 905):
    g = gen_pages(s); gr, gc, gf = classify(g); gm = Tri([w for w, n in gc.items() if n >= 2])
    G += [(r['word'], r['cls'], f, g[r['pi']]['toks'][r['i']][4] == 0) for r, f in zip(gr, struct_feats([r['word'] for r in gr], gf, gm))]
RF = [(r['word'], r['cls'], f, P[r['pi']]['toks'][r['i']][4] == 0, P[r['pi']]['toks'][r['i']][1]) for r, f in zip(rows, F)]
for nm, S, SG in (('all', RF, G), ('mid-line P only', [x for x in RF if not x[3] and x[4] == 'P'], [x for x in G if not x[3]])):
    print(nm)
    for cl in ('FREE', 'EDIT2'):
        a = [x[2] for x in S if x[1] == cl]; b = [x[2] for x in SG if x[1] == cl]
        print('  %-5s real n %4d ' % (cl, len(a)) + ' '.join('%s %.3f [%.3f,%.3f]' % (k, *boot([d[k] for d in a])) for k in ('lp', 'oe', 'rare', 'length')))
        print('  %-5s GEN  n %4d ' % (cl, len(b)) + ' '.join('%s %.3f [%.3f,%.3f]' % (k, *boot([d[k] for d in b])) for k in ('lp', 'oe', 'rare', 'length')))
fr = [x for x in RF if x[1] == 'FREE']
print('\nFREE: line-first share %.3f, label/circle/radial share %.3f' % (np.mean([x[3] for x in fr]), np.mean([x[4] != 'P' for x in fr])))
gch = collections.Counter(ch for x in fr for ch in x[0] if ch in RARE); ech = collections.Counter(ch for x in RF if x[1] == 'EDIT2' for ch in x[0] if ch in RARE)
nf = sum(len(x[0]) for x in fr); ne = sum(len(x[0]) for x in RF if x[1] == 'EDIT2')
print('rare glyphs per 1000 chars FREE vs EDIT2:', {k: (round(1000 * gch[k] / nf, 1), round(1000 * ech[k] / ne, 1)) for k in sorted(RARE)})
pairs = {(onset(f), ending(f)) for f in freq}
nov = collections.Counter((onset(x[0]), ending(x[0])) for x in fr if (onset(x[0]), ending(x[0])) not in pairs)
print('novel onset+ending pairs among FREE (top):', nov.most_common(15))
