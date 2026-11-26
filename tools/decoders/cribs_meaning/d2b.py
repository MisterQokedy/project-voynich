# D2b: a constructed language (category prefixes, agreeing role endings, a category grammar) written through the frozen hybrid procedure.
import sys, json, random, collections
sys.path.insert(0, './work/meaning_procedure/code')
from hybrid import *
P0 = json.load(open('./work/hybrid_gen/final_test.json'))['params']
for k in INTS: P0[k] = int(round(P0[k]))
CATS = sorted({CL(f) for f in allf}); ONS = {c: collections.Counter({f: n for f, n in allf.items() if CL(f) == c}) for c in CATS}
ENDS = sorted({split3(w)[2] for w in WC})
def grammar(gs):
    r = random.Random(gs); G = {c: r.sample(CATS, 2) for c in CATS}; perm = ENDS[:]; r.shuffle(perm); M = dict(zip(ENDS, perm)); return G, M
def gen_cl(shapes, prm, seed, rho, gam, G, M):
    r = random.Random(seed); out = []; hist = []
    for p in shapes:
        q = []; page = list(hist[-prm['carry']:]) if prm['carry'] else []; pend = [split3(x)[2] for x in page]
        for li, l in enumerate(p):
            words = []
            for k in range(len(l)):
                if k == 0: w = draw(dist(PGw if li == 0 else LIw, prm['tauL'], ('L', li == 0)), r)
                else:
                    prev = words[-1]; pd = onset_probs(prev, prm); src = page[-prm['W']:]
                    if r.random() < prm['pw']:
                        # grammar step: category from the conlang grammar (strength rho) or the procedure; role ending agrees (gamma)
                        if r.random() < rho: c = r.choice(G[CL(gg(prev)[0])]); f = draw(dist(ONS[c], 1.0, ('ons', c)), r)
                        else: f = draw((list(pd), list(pd.values())), r)
                        b = draw(dist(bf[f], prm['taub'], ('b', f)), r) if bf[f] else ''
                        pe = split3(prev)[2]
                        e = M.get(pe, pe) if (r.random() < gam and pe in M) else new_ending(b, f, pe, r, prm)
                        w = f + b + e
                    elif src and r.random() < prm['pc']:
                        cand = [src[r.randrange(len(src))] for _ in range(prm['K'])]
                        wt = [(pd.get(gg(c)[0], 0) + 1e-4) ** prm['beta'] for c in cand]
                        w = r.choices(cand, wt)[0]
                        if r.random() < prm['mu']: w = mutate(w, r, prm)
                        if r.random() < 1 - prm['keepE']:
                            f, b_, e = split3(w); w = f + b_ + new_ending(b_, f, split3(prev)[2], r, prm)
                    else:
                        f = draw((list(pd), list(pd.values())), r); w = fresh(f, prev, page, pend, r, prm)
                    if not w: w = prev
                words.append(w); page.append(w); pend.append(split3(w)[2])
            q.append(words)
        hist = page
        out.append(rule([q], prm['q'], r)[0] if prm['q'] > 0 else q)
    return out
def z(g, ref): return sum(abs(g[k] - ref[k]) / SD[k] for k in KEYS)
def fitrun(a):
    rho, gam, pw, gs = a; G, M = grammar(gs); pages = gen_cl(FITSH, dict(P0, pw=pw), 11, rho, gam, G, M); g, ok, loss = score_on(pages, FITREF)
    return dict(rho=rho, gam=gam, pw=pw, gs=gs, n=int(sum(ok.values())), z=z(g, FITREF), misses=[k for k in ok if not ok[k]], lastlast=g['lastlast'], d1d2=g['d1d2'], S6=g['S6_orderMI'])
if __name__ == '__main__':
    import multiprocessing as mp
    grid = [(rho, gam, pw, gs) for rho in (0, 0.5, 0.9) for gam in (0, 0.3, 0.6) for pw in (0.2, 0.41) for gs in (1, 2)]
    with mp.Pool(int(sys.argv[1]) if len(sys.argv) > 1 else 2) as pool: rows = pool.map(fitrun, grid)
    for x in rows: print(f"FIT rho {x['rho']} gam {x['gam']} pw {x['pw']} g{x['gs']}: {x['n']}/24 |z| {x['z']:.1f} lastlast {x['lastlast']:.4f} d1d2 {x['d1d2']:+.4f} S6 {x['S6']:.3f} misses {x['misses']}", flush=True)
    best = max(rows, key=lambda x: (x['n'], -x['z'])); b0 = max([x for x in rows if x['rho'] == 0 and x['gam'] == 0], key=lambda x: (x['n'], -x['z']))
    bg = max([x for x in rows if x['rho'] > 0 or x['gam'] > 0], key=lambda x: (x['n'], -x['z']))
    print('chosen', best, '\nbest no-grammar', b0, '\nbest with grammar', bg, flush=True)
    G, M = grammar(best['gs']); prm = dict(P0, pw=best['pw']); test = []; npass = 0; keep = {}
    for sd in range(900, 905):
        T = gen_cl(TESTSH, prm, sd, best['rho'], best['gam'], G, M); g, ok, loss = score_on(T, REF); n = int(sum(ok.values())); p_ = n >= 20 and ok['R'] and ok['d1d2']; npass += p_
        test.append(dict(seed=sd, n=n, R_ok=bool(ok['R']), d1d2_ok=bool(ok['d1d2']), misses=[k for k in ok if not ok[k]]))
        print(f'TEST seed {sd}: {n}/24 R {ok["R"]} d1d2 {ok["d1d2"]} misses {[k for k in ok if not ok[k]]}', flush=True)
    # outputs for D2a detection: chosen setting and a strong-grammar setting (rho 0.9, gam 0.6, pw 0.41)
    for tag, (rho, gam, pw, gs) in (('chosen', (best['rho'], best['gam'], best['pw'], best['gs'])), ('strong', (0.9, 0.6, 0.41, 1))):
        G, M = grammar(gs); prm = dict(P0, pw=pw)
        keep[tag] = dict(FIT=gen_cl(FITSH, prm, 1900, rho, gam, G, M), TEST=gen_cl(TESTSH, prm, 900, rho, gam, G, M))
        g, ok, loss = score_on(keep[tag]['TEST'], REF); print(tag, 'TEST seed 900', int(sum(ok.values())), [k for k in ok if not ok[k]], flush=True)
    json.dump(keep, open('./work/meaning_procedure/cache/d2b_pages.json', 'w'))
    json.dump(dict(grid=rows, chosen=best, best_nogrammar=b0, best_grammar=bg, test=test, npass=npass), open('./work/meaning_procedure/d2b.json', 'w'), indent=1)
    print(f'seeds passing {npass}/5 ->', 'PASS' if npass >= 3 and (best['rho'] > 0 or best['gam'] > 0) else 'FAIL')
