"""Compression stats per chunk; merges into res.json. Usage: compress.py corp_full.json res.json"""
import sys, json, lzma, bz2, random
import numpy as np
sys.path.insert(0, './work/language_test/code'); from stats import chunks
C = json.load(open(sys.argv[1])); R = json.load(open(sys.argv[2])); r = random.Random(5)
def sz(t): b = t.encode(); return min(len(lzma.compress(b, preset=9 | lzma.PRESET_EXTREME)), len(bz2.compress(b, 9)))
for k, pp in C.items():
    for ch, st in zip(chunks(pp), R[k]):
        T = [w for p in ch for l in p for w in l][:5000]; txt = ' '.join(T)
        sh = T[:]; r.shuffle(sh)
        st['S11_bpc'] = 8 * sz(txt) / len(txt); st['S12_order'] = 1 - sz(txt) / sz(' '.join(sh))
    print(k, round(np.mean([x['S11_bpc'] for x in R[k]]), 3), round(np.mean([x['S12_order'] for x in R[k]]), 4))
json.dump(R, open(sys.argv[2], 'w'))
