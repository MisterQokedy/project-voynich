import sys, os, json, time, numpy as np
VARIANT, OUT = sys.argv[1], sys.argv[2]
P = '/tmp/w/naibbe_greshko/s16b/s16b.py'
sys.argv = [P, VARIANT, '/tmp/w/ext/naibbe-cipher', '/dev/null']; __file__ = P
exec(compile(open('/tmp/w/s16e/base.py').read(), P, 'exec'))
sys.path.insert(0, '/tmp/w/s16e'); import hb, collections
t1 = time.time()
keys, scores = hb.staged(seq, ptr, idx, nsym, lp, A, NG, R, np.arange(R) + 100, keys0, WE, [0.1, 0.25, 0.5, 1.0], 200, 3.0, 1.0)
b = int(np.argmax(scores))
outT = S.decode_units(sT, seg, symix, keys[b], ALPHA)
accs = [metrics.accuracy(S.decode_units(sT, seg, symix, k, ALPHA), truthT) for k in keys]
# truth-majority key objective for reference
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
res = dict(variant=VARIANT, nsym=nsym, TEST_acc=metrics.accuracy(outT, truthT), TEST=metrics.score(outT, truthT, C),
           TEST_acc_all_restarts=sorted(round(a, 3) for a in accs), restart_agreement=float(np.mean([(k == keys[b]).mean() for k in keys])),
           obj_best=float(scores[b]), obj_truth_key=float(S.objective(seq, ptr, nsym, tk, lp, A, NG, WE)),
           acc_truth_key=metrics.accuracy(S.decode_units(sT, seg, symix, tk, ALPHA), truthT),
           secs=round(time.time() - t1), TEST_sample=''.join(outT)[:200], truth_sample=''.join(truthT)[:200])
print(json.dumps(res, indent=1)); json.dump(res, open(OUT, 'w'), indent=1)
