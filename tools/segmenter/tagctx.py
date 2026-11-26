"""Tag word-final n after i (ctx='fin') in meta.json. python -I tagctx.py <data dir> <voynich-letters repo>"""
import csv, json, os, sys
from collections import defaultdict
from pathlib import Path
D, REPO = Path(sys.argv[1]), Path(sys.argv[2])
meta = json.load(open(D / 'meta.json'))
COMP = [("cth", "T"), ("ckh", "K"), ("cph", "P"), ("cfh", "F"), ("ch", "C"), ("sh", "S")]
enc = lambda s: [s := s.replace(a, b) for a, b in COMP][-1]
NL = defaultdict(int)
for r in csv.DictReader(open(REPO / 'data/letters/letters.csv')): NL[r['line']] += 1
fin = set()
for r in csv.DictReader(open(REPO / 'data/lines/lines.csv')):
    stem = r['file'][:-4]; ws = [enc(w) for w in r['label'].split()]
    if sum(map(len, ws)) != NL.get(stem, -1): continue
    i = 0
    for w in ws:
        if len(w) >= 2 and w[-1] == 'n' and w[-2] == 'i': fin.add((stem, i + len(w) - 1))
        i += len(w)
n = 0
for m in meta:
    if (m['line'], m['letter']) in fin: m['ctx'] = 'fin'; n += 1
json.dump(meta, open(D / 'meta.tmp', 'w')); os.replace(D / 'meta.tmp', D / 'meta.json')
print('tagged', n)
