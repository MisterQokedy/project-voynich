import sys; sys.path.insert(0, './work/oneoffs/code')
from oo import *
P = parse(V + 'transcriptions/ZL3b-n.txt')
rows, c, freq = classify(P)
N = sum(len(p['toks']) for p in P)
print('tokens', N, 'types', len(c), 'hapax', len(rows), 'share %.3f' % (len(rows) / N), 'freq types', len(freq))
print(collections.Counter(r['cls'] for r in rows))
codes = {}
for l in open(V + 'plant_drawings/page_codes.txt'):
    if l.startswith('#'): continue
    f = l.split(); codes['f' + f[0]] = f[1:]
with open(OUT + 'oneoffs_table.csv', 'w', newline='') as fh:
    W = csv.writer(fh)
    W.writerow(['word', 'class', 'panel', 'line', 'unit', 'locus', 'section', 'currier', 'hand', 'quire', 'line_pos', 'word_in_line', 'words_in_line',
                'label_or_drawing_text', 'page_has_labels', 'plant_coded', 'length', 'onset', 'ending',
                'nearest_frequent', 'nearest_frequent_count', 'dist_frequent', 'nearest_recent40', 'dist_recent40', 'nearest_source'])
    for r in rows:
        p = P[r['pi']]; w, u, loc, lid, i, n = p['toks'][r['i']]; m = p['meta']
        lp = 'only' if n == 1 else ('first' if i == 0 else ('last' if i == n - 1 else 'middle'))
        haslab = any(t[1] == 'L' for t in p['toks'])
        W.writerow([w, r['cls'], p['panel'], lid, u, loc, m.get('I', ''), m.get('L', ''), m.get('H', ''), m.get('Q', ''), lp, i + 1, n,
                    {'L': 'label', 'C': 'circle', 'R': 'radial'}.get(u, 'paragraph'), int(haslab), int(p['panel'] in codes), len(w), onset(w), ending(w),
                    r['src_freq'], r['src_freq_n'], r['d_freq'], r['src_recent'], ('' if r['d_recent'] == 99 else r['d_recent']), r['src']])
print(open(OUT + 'oneoffs_table.csv').read()[:600])
