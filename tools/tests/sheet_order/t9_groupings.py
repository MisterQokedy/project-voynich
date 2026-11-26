import sys, json, itertools
import numpy as np
sys.path.insert(0, 'code'); from vlib import *
exec(open('code/p1_stains.py').read().split("leaves = sorted")[0])
P2 = load(); pg = {p['page']: p for p in P2}
G = {'Q20-G-ZAN (vocabulary)': [[(103,116),(107,112),(108,111)], [(104,115),(105,114),(106,113)]],
     'Q20-G-PEL (vellum colour)': [[(105,114),(104,115),(107,112),(108,111)], [(103,116),(106,113)]],
     'Q13-G-SPLIT (Claston, content)': [[(75,84),(78,81)], [(76,83),(77,82),(79,80)]]}
for name, groups in G.items():
    sh = [s for g in groups for s in g]
    lab = np.array([gi for gi, g in enumerate(groups) for _ in g])
    words = [[w for L in s for x in 'rv' for w in pg.get(f'{L}{x}', {'words': []})['words']] for s in sh]
    M, *_ = tfidf_matrix(words); St = cos_sim(M)
    LM = {L: leafmap(L, 'P80', 6) for s in sh for L in s}
    Ss = np.array([[np.mean([np.corrcoef(LM[a].ravel(), LM[b].ravel())[0,1] for a in s1 for b in s2]) for s2 in sh] for s1 in sh])
    LMb = {L: leafmap(L, 'B', 6) for s in sh for L in s}
    Sb = np.array([[np.mean([np.corrcoef(LMb[a].ravel(), LMb[b].ravel())[0,1] for a in s1 for b in s2]) for s2 in sh] for s1 in sh])
    iu = np.triu_indices(len(sh), 1)
    def stat(S, l): same = (l[:, None] == l[None, :])[iu]; return S[iu][same].mean() - S[iu][~same].mean()
    allp = {tuple(sorted(np.array(x).tolist())) for x in itertools.permutations(lab)}
    out = []
    for S in (St, Ss, Sb):
        o = stat(S, lab); null = [stat(S, np.array(p)) for p in itertools.permutations(lab)]
        out.append(f'{o:+.3f} (p={np.mean(np.array(null) >= o):.2f})')
    print(f'{name:32s} text: {out[0]} | stain brightness: {out[1]} | stain yellowness: {out[2]}')
