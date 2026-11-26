import sys, random, collections, numpy as np
sys.path.insert(0, './work/timm_generator/code')
from common import VLINES, idx
import pos as P
g = P.g
def lines(I): return [l for i in I for l in VLINES[i] if len(l) >= 3]
FIT, TEST = lines(idx(None, 'fit')), lines(idx(None, 'test'))
def e1(L):
    fi, fm = collections.Counter(), collections.Counter()
    for l in L:
        G = [g(w) or ['?'] for w in l]; fi[G[0][0]] += 1
        for q in G[1:-1]: fm[q[0]] += 1
    return P.js(fi, fm), fi, fm
r = random.Random(5)
def null99(L): return np.percentile([e1([r.sample(l, len(l)) for l in L])[0] for _ in range(100)], 99)
E0, fi, fm = e1(FIT); ni, nm = sum(fi.values()), sum(fm.values())
ratio = {x: (fi[x] / ni) / (fm[x] / nm + 1e-9) for x in fi}
print('FIT first-glyph line-initial/mid ratio (top):', ', '.join(f'{x} {ratio[x]:.1f} ({fi[x]})' for x in sorted(ratio, key=lambda x: -ratio[x])[:10]))
print('under-represented at line start:', ', '.join(f'{x} {ratio[x]:.2f}' for x in sorted(ratio, key=lambda x: ratio[x])[:8]))
M = {x for x in ratio if ratio[x] >= 2 and fi[x] >= 10}; print('marker set M =', sorted(M))
midvocab_fit = collections.Counter(w for l in FIT for w in l[1:])
mp = {}
for x in M:
    c = collections.Counter()
    for l in FIT:
        G = g(l[0])
        if G and G[0] == x:
            rest = ''.join(G[1:])
            for y in set(q[0] for q in (g(w) for w in midvocab_fit) if q):
                if midvocab_fit.get(y + rest, 0): c[y] += midvocab_fit[y + rest]
            if rest and midvocab_fit.get(rest): c[''] += midvocab_fit[rest]
    mp[x] = c.most_common(1)[0][0] if c else ''
    print(f'  map {x} -> {mp[x]!r}  top candidates', c.most_common(4))
def apply(L, f): return [[f(l[0])] + l[1:] for l in L]
def strip(w):
    G = g(w); return ''.join(G[1:]) if G and G[0] in M and len(G) > 1 else w
def subst(w):
    G = g(w); return (mp[G[0]] + ''.join(G[1:])) if G and G[0] in M and len(G) > 1 else w
midT = collections.Counter(w for l in TEST for w in l[1:])
def attest(L):
    a = np.mean([midT[l[0]] > 0 for l in L])
    lens = [len(g(l[0])) for l in L]; pool = collections.defaultdict(list)
    for l in L:
        for k, w in enumerate(l[1:-1]): pool[len(g(w))].append(w)
    ctl = []
    for _ in range(20):
        ws = [r.choice(pool[n]) if pool[n] else '' for n in lens]
        ctl.append(np.mean([midT[w] - 1 > 0 for w in ws]))   # exclude its own occurrence
    return a, np.mean(ctl)
E_T = e1(TEST)[0]; n99 = null99(TEST); print(f'\nTEST E1 original {E_T:.3f}, shuffle 99th pct {n99:.3f}, excess {E_T-n99:.3f}')
for name, f in (('original', lambda w: w), ('strip M', strip), ('substitute', subst)):
    L = apply(TEST, f); e = e1(L)[0]; a, c = attest(L)
    print(f'{name:11} E1 {e:.3f}  remaining excess {100*(e-n99)/(E_T-n99):5.1f}%   attested line-initial {a:.3f} vs length-matched mid-line control {c:.3f}')
# what fraction of line-initial words start with M, and paragraph-initial vs other
print('\nshare of TEST line-initial words starting with M:', np.mean([bool(g(l[0])) and g(l[0])[0] in M for l in TEST]))
# Control: does stripping M from MID-line words starting with M also give attested words? (if yes, the gain is trivial)
def strip_att(ws):
    s = [strip(w) for w in ws]; return np.mean([midT[x] > 0 for x in s]), len(ws)
li = [l[0] for l in TEST if g(l[0]) and g(l[0])[0] in M]
mi = [w for l in TEST for w in l[1:-1] if g(w) and g(w)[0] in M]
a1, n1 = strip_att(li); a2, n2 = strip_att(mi)
print(f'\nstripped line-initial M-words attested {a1:.3f} (n={n1}) vs stripped mid-line M-words attested {a2:.3f} (n={n2})')
print('unstripped attested: line-initial M-words', np.mean([midT[w] > 0 for w in li]), ' mid-line M-words (minus self)', np.mean([midT[w] - 1 > 0 for w in mi]))
for x in sorted(M):
    a = [w for w in li if g(w)[0] == x]; b = [w for w in mi if g(w)[0] == x]
    if a and b: print(f'  {x}: line-init n={len(a)} stripped attested {strip_att(a)[0]:.2f} | mid n={len(b)} stripped attested {strip_att(b)[0]:.2f}')
# Bootstrap CI for attestation difference after strip vs control
L = apply(TEST, strip); bs = []
for _ in range(200):
    S = [L[r.randrange(len(L))] for _ in L]; bs.append(np.mean([midT[l[0]] > 0 for l in S]))
print('strip attestation 95% CI', np.percentile(bs, [2.5, 97.5]))
def e3(L): return np.mean([len(g(l[0])) for l in L]) - np.mean([len(g(w)) for l in L for w in l[1:-1]])
sh = [e3([r.sample(l, len(l)) for l in TEST]) for _ in range(50)]
print(f'\nE3 (line-initial minus mid length, glyphs): original {e3(TEST):+.2f}, after strip {e3(apply(TEST, strip)):+.2f}, shuffle {np.mean(sh):+.2f}')
nm_ = [l for l in TEST if not (g(l[0]) and g(l[0])[0] in M)]; mm_ = [l for l in TEST if g(l[0]) and g(l[0])[0] in M]
print(f'E3 lines starting with M {e3(mm_):+.2f} ; lines not starting with M {e3(nm_):+.2f}')
