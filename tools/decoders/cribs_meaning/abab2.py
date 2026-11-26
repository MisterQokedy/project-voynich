# Exploratory: which onsets carry the distance-2 same-onset excess (Voynich all pages, real vs within-line shuffled)?
exec(open('./work/meaning_procedure/code/texts.py').read())
import random, numpy as np
M = json.load(open('./work/manuscript_wide/pages2.json'))
for lang in 'AB':
    L = [l for i in range(len(VLINES)) if M[i].get('L') == lang for l in VLINES[i]]
    def cnt(L):
        c = collections.Counter(); n = 0
        for l in L:
            for i in range(len(l) - 2):
                n += 1
                if l[i] != l[i + 2] and gg(l[i])[0] == gg(l[i + 2])[0]: c[gg(l[i])[0]] += 1
        return c, n
    real, n = cnt(L); r = random.Random(1); sh = collections.Counter()
    for _ in range(20):
        c, _ = cnt([r.sample(l, len(l)) for l in L]); sh.update(c)
    ex = {k: (real[k] - sh[k] / 20) / n for k in set(real) | set(sh)}
    print(lang, 'total excess', round(sum(ex.values()), 4), 'top:', [(k, round(v, 4), real[k]) for k, v in sorted(ex.items(), key=lambda x: -x[1])[:6]])
    # example triples with qo...qo
    ex_tr = [' '.join(l[i:i + 3]) for l in L for i in range(len(l) - 2) if gg(l[i])[0] == gg(l[i + 2])[0] == 'q' and gg(l[i+1])[0] != 'q'][:8]
    print('  e.g.', ex_tr)
