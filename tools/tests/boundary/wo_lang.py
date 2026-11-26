import sys, json, random, re, math, collections, numpy as np
exec(open('./work/word_order/code/wo.py').read().split("V = [l for i in TI")[0])
C = json.load(open('./work/decipherment_harness/corpora.json')); X = '/tmp/claude-0/-home-user/18d6effa-14be-52f6-88bb-dce5a4bed879/scratchpad/ext'
tok = lambda t: re.findall(r'[a-z]+', t.lower())
L = {k: C[k][:20000] for k in ('latin', 'italian', 'english')}
L['german_herb'] = tok(open(X + '/mean/texts/Historical - German - Technical - German Herbarium.txt', encoding='utf-8', errors='ignore').read())[:20000]
g = lambda w: list(w) or ['?']
for k, T in L.items():
    lines = [T[i:i + 9] for i in range(0, len(T), 9)]; e = excess(lines)
    print(f'{k:12} edge {e["edge"]:.4f}  first_first {e["first_first"]:.4f}  last_last {e["last_last"]:.4f}  word200 {e["word200"]:.4f}')
G = []
import glob
for f in sorted(glob.glob(X + '/gib/*.txt')): G += [tok(l) for l in open(f, encoding='utf-8', errors='ignore') if len(tok(l)) >= 2]
e = excess(G); print(f'{"gibberish":12} edge {e["edge"]:.4f}  first_first {e["first_first"]:.4f}  last_last {e["last_last"]:.4f}  word200 {e["word200"]:.4f}')
