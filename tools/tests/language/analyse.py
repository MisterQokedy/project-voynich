"""Score per PREREG.md. Usage: analyse.py res.json"""
import sys, json, numpy as np
R = json.load(open(sys.argv[1]))
NAT = ['latin_isidore', 'latin_caesar', 'ME_cury', 'EME_culpeper', 'italian_dante', 'german_faust']
OTH = ['C1_verbose_latin', 'C2_sorted_latin', 'G1_timm', 'G2_rugg', 'N1_uniform_noise', 'N2_freq_noise', 'ctrl_voynich_shuffled', 'voynich_A', 'voynich_B']
S = list(R['voynich'][0]); CORE = S[:10]
a = lambda k, s: np.array([x[s] for x in R[k]])
def z(k, s, ref='voynich'):
    v, c = a(ref, s), a(k, s); return abs(v.mean() - c.mean()) / np.sqrt(v.std(ddof=1) ** 2 + c.std(ddof=1) ** 2 + 1e-12)
print('stat'.ljust(13), 'voynich'.rjust(8), '| lang band | in?', ' '.join(k[:8].rjust(8) for k in NAT + OTH))
inband = {}
for s in S:
    m = [a(k, s).mean() for k in NAT]; sd = np.sqrt(np.mean([a(k, s).var(ddof=1) for k in NAT]))
    lo, hi = min(m) - 2 * sd, max(m) + 2 * sd; v = a('voynich', s).mean(); inband[s] = lo <= v <= hi
    print(s.ljust(13), f'{v:8.3f} | {lo:6.2f}..{hi:6.2f} | {"Y" if inband[s] else "N"}  ',
          ' '.join((f'{a(k, s).mean():7.3f}' + ('*' if z(k, s) < 2 else ' ')) for k in NAT + OTH))
print('\n* = matches Voynich (z<2).  Match counts over S1-S10 (S5 excluded for all, since generators were tuned on it):')
cnt = {k: sum(z(k, s) < 2 for s in CORE if s != 'S5_types') for k in NAT + OTH}
for k, c in sorted(cnt.items(), key=lambda x: -x[1]): print(f'  {k:24s} {c}/9')
nb = sum(inband[s] for s in CORE); print(f'\nVoynich inside language band on {nb}/10 core stats; outside on:', [s for s in CORE if not inband[s]])
bestnat = max(cnt[k] for k in NAT); gen = max(cnt['G1_timm'], cnt['G2_rugg'])
print('verdict (a) behaves like language:', nb >= 8 and gen <= bestnat)
print('verdict (b) a generator fits at least as well:', gen >= bestnat, f'(best natural {bestnat}, best generator {gen})')
print('verdict (c) cipher rescues:', [s for s in CORE if not inband[s] and (z("C1_verbose_latin", s) < 2 or z("C2_sorted_latin", s) < 2)])
print('sanity: shuffle control loses (z>=2):', {s: bool(z('ctrl_voynich_shuffled', s) >= 2) for s in ['S6_orderMI', 'S7_burst', 'S8_nearcopy', 'S9_localrep', 'S10_immrep', 'S12_order']})
print('noise separated from Voynich on compression S11:', {k: round(z(k, 'S11_bpc'), 1) for k in ['N1_uniform_noise', 'N2_freq_noise']})
