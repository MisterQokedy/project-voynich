# A4-P: A4 as a 25th statistic; score generators on 25. See ../PREREG3.md
exec(open('./work/meaning_procedure/code/a4g.py').read().split("\nif __name__ == '__main__':")[0])
import collections
def sheet(i): return META[i].get('Q', '?') + str(META[i].get('B', '?'))
if __name__ == '__main__':
    rng = np.random.default_rng(5); V = A4(FITSH, TESTSH, rng)
    sh = collections.defaultdict(list)
    for j, i in enumerate(TI): sh[sheet(i)].append(j)
    keys = list(sh); boots = []
    for b in range(200):
        pick = rng.choice(len(keys), len(keys)); T = [TESTSH[j] for k in pick for j in sh[keys[k]]]; boots.append(A4(FITSH, T, rng, nsh=5))
    sd = max(float(np.std(boots)), 0.1 * abs(V)); lo, hi = V - 2 * sd, V + 2 * sd
    fa, fb = internal(FITSH); vf = A4(fa, fb, rng)
    print(f'Voynich TEST A4 {V:+.4f}, bootstrap sd {np.std(boots):.4f}, band {lo:+.4f} .. {hi:+.4f}; Voynich FIT-internal {vf:+.4f} ({"in" if lo <= vf <= hi else "OUT of"} band)', flush=True)
    OUT = dict(V=V, sd=sd, band=[lo, hi], fit_internal=vf, runs={})
    def score25(F, T, tag):
        g, ok, loss = score_on(T, REF); a4 = A4(F, T, np.random.default_rng(1)); oka = lo <= a4 <= hi; n24 = int(sum(ok.values()))
        r = dict(n24=n24, n25=n24 + int(oka), A4=a4, A4_ok=bool(oka), R_ok=bool(ok['R']), d1d2_ok=bool(ok['d1d2']), misses=[k for k in ok if not ok[k]] + ([] if oka else ['A4']))
        OUT['runs'][tag] = r; print(f'{tag:24} {r["n25"]}/25 (24: {n24})  A4 {a4:+.4f} {"ok" if oka else "MISS"}  misses {r["misses"]}', flush=True); return r
    npass = nmiss0 = 0; d24 = []
    for sd_ in range(900, 905):
        F = gen_a(FITSH, BF, P0, sd_ + 1000, 'onset', 0.05); T = gen_a(TESTSH, BT, P0, sd_, 'onset', 0.05); r1 = score25(F, T, f'habit_{sd_}')
        F0 = gen_a(FITSH, BF, P0, sd_ + 1000, 'onset', 0); T0 = gen_a(TESTSH, BT, P0, sd_, 'onset', 0); r0 = score25(F0, T0, f'hybrid_{sd_}')
        npass += r1['n25'] >= 21 and r1['R_ok'] and r1['d1d2_ok'] and r1['A4_ok']; nmiss0 += not r0['A4_ok']; d24.append(r1['n24'] - r0['n24'])
    Pc = json.load(open('./work/meaning_procedure/cache/proc_controls.json'))
    for s in range(900, 905): score25(Pc[f'pure_proc_{s}']['FIT'], Pc[f'pure_proc_{s}']['TEST'], f'pure_proc_{s}')
    Tm = json.load(open('./work/timm_rules/timm_rules_pages.json'))
    for s in Tm: score25([Tm[s][i] for i in FI], [Tm[s][i] for i in TI], f'timm_{s}')
    rr = random.Random(3); score25(FITSH, [[rr.sample(l, len(l)) for l in p] for p in TESTSH], 'voynich_shuffled_in_lines')
    OUT.update(npass=npass, hybrid_A4_misses=nmiss0, delta24_mean=float(np.mean(d24)))
    print(f'habit seeds passing {npass}/5; hybrid without habit misses A4 on {nmiss0}/5; mean change in 24-stat count {np.mean(d24):+.1f} ->', 'PASS' if npass >= 3 and nmiss0 >= 3 else 'FAIL', flush=True)
    json.dump(OUT, open('./work/meaning_procedure/a4p.json', 'w'), indent=1)
