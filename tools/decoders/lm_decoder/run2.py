"""S16e attempt 2 (frozen): python run2.py SRC OUT   SRC = Greshko variant or own_LANG"""
import sys, os, json, time, collections, numpy as np
SRC, OUTF = sys.argv[1], sys.argv[2]
R2, SW, T0_, STAGES, NG2 = 64, 1000, 3.0, [1.0], 4
sys.path.insert(0, '/tmp/w/d1'); sys.path.insert(0, '/tmp/w/s16e')
import cipher, metrics, sa_decoder as S, hb
if SRC.startswith('own_'):
    lang = SRC[4:]
    C = json.load(open(f'/tmp/w/d1/corpora/{lang}.json')); ALPHA = metrics.alphabet(C['lm']); A = len(ALPHA)
    plain = ''.join(c for c in C['plain'] if c in ALPHA)
    shF = cipher.shapes_of(cipher.V['fit']); shT = cipher.shapes_of(cipher.V['test'])
    key = cipher.build_key(ALPHA, seed=11)
    cF, tF, used = cipher.encrypt(plain, key, shF, seed=1); cT, tT, _ = cipher.encrypt(plain[used:], key, shT, seed=2)
    sF = S.strip_nulls(cF); sT = S.strip_nulls(cT); seg = S.Segmenter(sF)
    truthF = [u for p in tF for l in p for u in l]; truthT = [u for p in tT for l in p for u in l]
    symix = {}; seq, _ = S.symbols(sF, seg, symix, grow=True); nsym = len(symix); ptr, idx = S.positions(seq, nsym)
else:
    P = '/tmp/w/naibbe_greshko/s16b/s16b.py'; sys.argv = [P, SRC, '/tmp/w/ext/naibbe-cipher']; __file__ = P
    exec(compile(open('/tmp/w/s16e/base2.py').read(), P, 'exec'))
lp = S.ngram_table(C['lm'], ALPHA, n=NG2)
keys0 = S.freq_init(seq, nsym, C['lm'], ALPHA, R2, seed=3); t1 = time.time()
keys, scores = hb.staged(seq, ptr, idx, nsym, lp, A, NG2, R2, np.arange(R2) + 100, keys0, 1.0, STAGES, SW, T0_, 1.0)
b = int(np.argmax(scores)); outT = S.decode_units(sT, seg, symix, keys[b], ALPHA)
accs = [metrics.accuracy(S.decode_units(sT, seg, symix, k, ALPHA), truthT) for k in keys]
ix = {a: i for i, a in enumerate(ALPHA)}; toksF = [w for p in sF for l in p for w in l]
votes = [collections.Counter() for _ in range(nsym)]
for w, u in zip(toksF, truthF):
    a = seg.segment(w)
    if a is None: continue
    ms = [('W', a[1])] if a[0] == 'W' else [('P', a[1]), ('S', a[2])]
    if len(ms) == len(u):
        for m, c in zip(ms, u):
            if m in symix and c in ix: votes[symix[m]][c] += 1
tk = np.array([ix[v.most_common(1)[0][0]] if v else 0 for v in votes], dtype=np.int64)
top = np.argsort(-scores)[:8]
res = dict(src=SRC, nsym=nsym, TEST_acc=metrics.accuracy(outT, truthT), TEST_acc_all_restarts=sorted(round(a, 3) for a in accs),
           restart_agreement=float(np.mean([(k == keys[b]).mean() for k in keys])),
           top8_agreement=float(np.mean([(keys[t] == keys[b]).mean() for t in top[1:]])),
           obj_best=float(scores[b]), obj_truth_key=float(S.objective(seq, ptr, nsym, tk, lp, A, NG2, 1.0)),
           acc_truth_key=metrics.accuracy(S.decode_units(sT, seg, symix, tk, ALPHA), truthT), secs=round(time.time() - t1),
           TEST_sample=''.join(outT)[:200], truth_sample=''.join(truthT)[:200])
print(json.dumps(res, indent=1)); json.dump(res, open(OUTF, 'w'), indent=1)
