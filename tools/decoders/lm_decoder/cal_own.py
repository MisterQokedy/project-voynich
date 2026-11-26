import sys, os, json, time, numpy as np
sys.path.insert(0, '/tmp/w/d1'); sys.path.insert(0, '/tmp/w/s16e')
import cipher, metrics, sa_decoder as S, hb
lang, OUT = sys.argv[1], sys.argv[2]
C = json.load(open(f'/tmp/w/d1/corpora/{lang}.json')); ALPHA = metrics.alphabet(C['lm']); A = len(ALPHA)
plain = ''.join(c for c in C['plain'] if c in ALPHA)
shF = cipher.shapes_of(cipher.V['fit']); shT = cipher.shapes_of(cipher.V['test'])
key = cipher.build_key(ALPHA, seed=11)
cF, tF, used = cipher.encrypt(plain, key, shF, seed=1); cT, tT, _ = cipher.encrypt(plain[used:], key, shT, seed=2)
sF = S.strip_nulls(cF); sT = S.strip_nulls(cT); seg = S.Segmenter(sF)
truthT = [u for p in tT for l in p for u in l]
symix = {}; seq, _ = S.symbols(sF, seg, symix, grow=True); nsym = len(symix); ptr, idx = S.positions(seq, nsym)
lp = S.ngram_table(C['lm'], ALPHA, n=3); R = 16
keys0 = S.freq_init(seq, nsym, C['lm'], ALPHA, R, seed=3); t1 = time.time()
keys, scores = hb.staged(seq, ptr, idx, nsym, lp, A, 3, R, np.arange(R) + 100, keys0, 1.0, [0.1, 0.25, 0.5, 1.0], 200, 3.0, 1.0)
b = int(np.argmax(scores)); outT = S.decode_units(sT, seg, symix, keys[b], ALPHA)
accs = [metrics.accuracy(S.decode_units(sT, seg, symix, k, ALPHA), truthT) for k in keys]
res = dict(lang=lang, nsym=nsym, TEST_acc=metrics.accuracy(outT, truthT), TEST_acc_all_restarts=sorted(round(a, 3) for a in accs),
           restart_agreement=float(np.mean([(k == keys[b]).mean() for k in keys])), secs=round(time.time() - t1), TEST_sample=''.join(outT)[:200])
print(json.dumps(res, indent=1)); json.dump(res, open(OUT, 'w'), indent=1)
