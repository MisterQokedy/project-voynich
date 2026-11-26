# Exploratory: what makes the distance-2 onset repeat? Whole-word repeats (x y x), same onset different word, or two-word chunk repeats (x y ... x y)?
exec(open('./work/meaning_procedure/code/texts.py').read())
import numpy as np
S = load_all(want_lang=False, want_gib=False)
def parts(P, rng=None):
    L = [l for p in P for l in p]
    if rng: L = [rng.sample(l, len(l)) for l in L]
    n = same_w = same_on = mid_same_on = 0
    for l in L:
        for i in range(len(l) - 2):
            a, b, c = l[i], l[i + 1], l[i + 2]; n += 1
            if a == c: same_w += 1
            elif gg(a)[0] == gg(c)[0]:
                same_on += 1
                if gg(b)[0] == gg(a)[0]: mid_same_on += 1
    return np.array([same_w, same_on, mid_same_on]) / n
import random
for name in ['voynich', 'timm_21', 'timm_22', 'pure_proc_900', 'hybrid_full_900', 'd3cu_mhg_megenberg']:
    F, T, sp, en = S[name]; r = random.Random(1)
    for half, P in (('TEST', T), ('ALL', F + T)):
        real = parts(P); sh = np.mean([parts(P, r) for _ in range(10)], 0)
        print(f'{name:20} {half}: x?x same word {real[0]:.4f} (shuf {sh[0]:.4f})  same onset, other word {real[1]:.4f} (shuf {sh[1]:.4f})  of which middle also same onset {real[2]:.4f} (shuf {sh[2]:.4f})')
# Voynich by Currier language, all pages
M = json.load(open('./work/manuscript_wide/pages2.json'))
for lang in 'AB':
    P = [VLINES[i] for i in range(len(VLINES)) if M[i].get('L') == lang]; r = random.Random(1); real = parts(P); sh = np.mean([parts(P, r) for _ in range(10)], 0)
    print(f'Voynich {lang}: same word {real[0]:.4f} ({sh[0]:.4f})  same onset other word {real[1]:.4f} ({sh[1]:.4f})  middle same {real[2]:.4f} ({sh[2]:.4f})')
