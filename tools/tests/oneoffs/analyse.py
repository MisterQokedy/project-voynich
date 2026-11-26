import sys; sys.path.insert(0, './work/oneoffs/code')
from oo import *
R = {}
rng = random.Random(1)
P = parse(V + 'transcriptions/ZL3b-n.txt'); rows, c, freq = classify(P)
def model_for(c): return Tri([w for w, n in c.items() if n >= 2])
M = model_for(c)
grp = {k: [r['word'] for r in rows if r['cls'] == k] for k in ('FREE', 'EDIT1', 'EDIT2')}
grp['COMMON'] = freq
grp['GLYPHSHUF_FREE'] = [''.join(rng.sample(w, len(w))) for w in grp['FREE']]
# GEN
genfree, genedit, genshare = [], [], []
for s in range(900, 905):
    G = gen_pages(s); gr, gc, gf = classify(G); gm = model_for(gc)
    N = sum(len(p['toks']) for p in G)
    genshare.append((len(gr) / N, collections.Counter(r['cls'] for r in gr)))
    genfree += struct_feats([r['word'] for r in gr if r['cls'] == 'FREE'], gf, gm)
    genedit += struct_feats([r['word'] for r in gr if r['cls'] != 'FREE'], gf, gm)
print('GEN hapax share and classes per seed:'); [print('  %.3f' % a, dict(b), 'free share %.3f' % (b['FREE'] / sum(b.values()))) for a, b in genshare]
F = {k: struct_feats(v, freq, M) for k, v in grp.items()}
F['GEN_FREE'] = genfree; F['GEN_EDIT'] = genedit
print('\nStructure (mean [95% CI]); lp = char-trigram log-prob per char under the own count>=2 model')
keys = ['length', 'lp', 'recomb', 'oe', 'rare', 'irun', 'erun', 'run3']
print('%-15s %6s ' % ('group', 'n') + ' '.join('%-20s' % k for k in keys))
for g, f in F.items():
    print('%-15s %6d ' % (g, len(f)) + ' '.join('%-20s' % ('%.3f [%.3f,%.3f]' % boot([d[k] for d in f])) for k in keys))
    R[g] = {k: boot([d[k] for d in f]) for k in keys}
# onset / ending enrichment FREE vs EDIT
def dist(ws, fn):
    cc = collections.Counter(fn(w) for w in ws); n = len(ws); return {k: v / n for k, v in cc.items()}
edit = grp['EDIT1'] + grp['EDIT2']
for nm, fn in (('onset', onset), ('ending', ending)):
    a, b = dist(grp['FREE'], fn), dist(edit, fn)
    ks = sorted(set(a) | set(b), key=lambda k: -(a.get(k, 0) + b.get(k, 0)))[:14]
    print('\n%s share FREE vs EDIT:' % nm, '  '.join('%s %.3f/%.3f' % (k, a.get(k, 0), b.get(k, 0)) for k in ks))
# genuinely novel onset-ending pairs in FREE: list most common
cc = collections.Counter((onset(w), ending(w)) for w in grp['FREE'])
print('\nTop FREE onset+ending pairs:', cc.most_common(12))
json.dump(R, open(OUT + 'structure.json', 'w'), indent=1)
