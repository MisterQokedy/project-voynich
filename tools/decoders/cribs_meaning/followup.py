# (1) D2a: 2,000-permutation p for every dependency (the pre-registered 200 cannot reach the Bonferroni level 0.0025; min p = 1/201).
# (2) D3b sensitivity k = 2 and 20 (pre-registered as reported). (3) Exploratory: A4 conditional on the middle word's onset (skip link vs chain).
exec(open('./work/meaning_procedure/code/d3b_d2a.py').read().split("\nif __name__ == '__main__':")[0])
def cond_A4(FS, TS, nx):
    # gain of on_i for predicting on_{i+2} given on_{i+1}, held-out, add-0.5
    def trip(S):
        ok = (S.line[2:] == S.line[:-2]); return S.on[:-2][ok], S.on[1:-1][ok], S.on[2:][ok]
    a, m, c = trip(FS); J3 = np.zeros((nx, nx, nx)); np.add.at(J3, (a, m, c), 1); J2 = J3.sum(0)
    at, mt, ct = trip(TS); n = nx + 1
    p1 = (J2[mt, ct] + 0.5) / (J2[mt].sum(1) + 0.5 * n); p2 = (J3[at, mt, ct] + 0.5) / (J3[at, mt].sum(1) + 0.5 * n)
    return float((np.log2(p2) - np.log2(p1)).mean())
if __name__ == '__main__':
    S = load_all(); OUT = {}
    for name, (F, T, sp, en) in S.items():
        voc = {'on': {}, 'en': {}}; FS, TS = Seq(slot_seqs(F, sp, en), voc), Seq(slot_seqs(T, sp, en), voc); nx = {'on': len(voc['on']), 'en': len(voc['en'])}
        rng = np.random.default_rng(7); r = {}
        for dn, (d, fx, fy) in DEPS.items():
            g = dep_gain(FS, TS, d, fx, fy, nx[fx], nx[fy]); nl = np.array([dep_gain(FS, TS.shuffled(rng), d, fx, fy, nx[fx], nx[fy]) for _ in range(2000)])
            r[dn + '_p2000'] = float((1 + (nl >= g).sum()) / 2001)
        c = cond_A4(FS, TS, nx['on']); cs = [cond_A4(FS.shuffled(rng), TS.shuffled(rng), nx['on']) for _ in range(20)]
        r['A4_cond_os'] = c - float(np.mean(cs)); r['A4_cond'] = c
        for k in (2, 20):
            x = d3b(F, T, sp, k=k, nperm=50); r[f'd3b_k{k}'] = {s: x[s]['G'] for s in x}
        OUT[name] = r; print(name, json.dumps(r), flush=True)
    json.dump(OUT, open('./work/meaning_procedure/followup.json', 'w'), indent=1)
