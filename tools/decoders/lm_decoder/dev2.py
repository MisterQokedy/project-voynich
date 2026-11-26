"""dev: python dev2.py SRC(VARIANT|own_LANG) R SWEEPS T0 STAGES NG"""
import sys, os, json, time, numpy as np
SRC, R_, SW, T0_, STAGES, NGo = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), [float(x) for x in sys.argv[5].split(',')], int(sys.argv[6])
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
    truthT = [u for p in tT for l in p for u in l]
    symix = {}; seq, _ = S.symbols(sF, seg, symix, grow=True); nsym = len(symix); ptr, idx = S.positions(seq, nsym)
else:
    P = '/tmp/w/naibbe_greshko/s16b/s16b.py'; sys.argv = [P, SRC, '/tmp/w/ext/naibbe-cipher', '/dev/null']; __file__ = P
    exec(compile(open('/tmp/w/s16e/base.py').read(), P, 'exec'))
lp = S.ngram_table(C['lm'], ALPHA, n=NGo); R = R_
keys0 = S.freq_init(seq, nsym, C['lm'], ALPHA, R, seed=3); t1 = time.time()
keys, scores = hb.staged(seq, ptr, idx, nsym, lp, A, NGo, R, np.arange(R) + 100, keys0, 1.0, STAGES, SW, T0_, 1.0)
b = int(np.argmax(scores))
accs = [metrics.accuracy(S.decode_units(sT, seg, symix, k, ALPHA), truthT) for k in keys]
print(SRC, sys.argv[2:] if not SRC.startswith('own') else '', dict(NG=NGo, acc_best=round(accs[b], 3), accs=sorted(round(a, 3) for a in accs), secs=round(time.time() - t1)), flush=True)
