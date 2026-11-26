import sys, os, json, time, numpy as np
VARIANT, R_, SW, T0_, STAGES, NGo = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), [float(x) for x in sys.argv[5].split(',')], int(sys.argv[6])
P = '/tmp/w/naibbe_greshko/s16b/s16b.py'
sys.argv = [P, VARIANT, '/tmp/w/ext/naibbe-cipher', '/dev/null']
__file__ = P
src = open('/tmp/w/s16e/base.py').read().replace("R, ITERS, NG, T0, T1, WE = 16,", f"R, ITERS, NG, T0, T1, WE = {R_},").replace("ITERS, NG, T0, T1, WE = %d, 20_000_000, 3" % R_, "ITERS, NG, T0, T1, WE = %d, 20_000_000, %d" % (R_, NGo))
exec(compile(src, P, 'exec'))
sys.path.insert(0, '/tmp/w/s16e'); import hb
t1 = time.time()
keys, scores = hb.staged(seq, ptr, idx, nsym, lp, A, NG, R, np.arange(R) + 100, keys0, WE, STAGES, SW, T0_, 1.0)
b = int(np.argmax(scores))
accs = [metrics.accuracy(S.decode_units(sT, seg, symix, k, ALPHA), truthT) for k in keys]
print(dict(NG=NG, best_obj=float(scores[b]), acc_best=round(accs[b], 3), accs=sorted(round(a, 3) for a in accs), secs=round(time.time() - t1)), flush=True)
