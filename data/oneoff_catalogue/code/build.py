"""Build the free one-off catalogue from oneoffs/oneoffs_table.csv (no new analysis)."""
import csv, re, collections, sys
sys.path.insert(0, 'tools/tests/oneoffs')
from oo import parse, onset, ending
V = 'work/'; OUT = 'data/oneoff_catalogue/'  # run from the repository root
GLY = re.compile(r'cth|ckh|cph|cfh|ch|sh|.')
GAL = {'k','t','p','f','cth','ckh','cph','cfh'}; BEN = {'ch','sh'}
def split(w):
    g = GLY.findall(w); core_i = [i for i, x in enumerate(g) if x in GAL or x in BEN]
    if not core_i:
        m = re.match(r'(qo|q|o|y|d|s|l|r)?', w); p = m.group(0) or ''; return p, '', w[len(p):]
    a, b = core_i[0], core_i[-1]
    while b + 1 < len(g) and g[b+1] in ('e', 'h'): b += 1
    return ''.join(g[:a]), ''.join(g[a:b+1]), ''.join(g[b+1:])
rows = [r for r in csv.DictReader(open(V + 'oneoffs/oneoffs_table.csv')) if r['class'] == 'FREE']
# start+ending pairs (OO definition: first glyph, last two letters) in words that recur
cnt = collections.Counter(t[0] for p in parse(V + 'transcriptions/ZL3b-n.txt') for t in p['toks'])
rec_pairs = {(onset(w), ending(w)) for w, c in cnt.items() if c >= 2}
out = []
for r in rows:
    w = r['word']; pre, core, end = split(w); g = GLY.findall(w)
    ng = sum(x in GAL for x in g)
    pos = lambda ch: ';'.join(str(i+1) for i, c in enumerate(w) if c == ch)
    dbl = sorted({m.group(0) for m in re.finditer(r'(e)\1+|(i)\2+', w)})
    pair = (onset(w), ending(w))
    out.append(dict(word=w, page=r['panel'], line=r['line'], section=r['section'], currier=r['currier'], scribe=r['hand'],
        quire=r['quire'], line_pos=r['line_pos'], word_in_line=r['word_in_line'], words_in_line=r['words_in_line'],
        placement=r['label_or_drawing_text'], length=r['length'], prefix=pre, core=core, ending=end,
        n_gallows=ng, p_positions=pos('p'), f_positions=pos('f'), doubled_e_i='|'.join(dbl),
        start=pair[0], end2=pair[1], pair_only_in_oneoffs=int(pair not in rec_pairs),
        nearest_frequent=r['nearest_frequent'], dist_frequent=r['dist_frequent']))
with open(OUT + 'free_oneoffs_catalogue.csv', 'w', newline='') as fh:
    wr = csv.DictWriter(fh, fieldnames=list(out[0])); wr.writeheader(); wr.writerows(out)
pc = collections.Counter((o['start'], o['end2']) for o in out if o['pair_only_in_oneoffs'])
with open(OUT + 'oneoff_only_pairs.csv', 'w', newline='') as fh:
    wr = csv.writer(fh); wr.writerow(['start', 'end2', 'n_free_oneoffs', 'examples'])
    for (s, e), n in pc.most_common():
        wr.writerow([s, e, n, ' '.join([o['word'] for o in out if (o['start'], o['end2']) == (s, e)][:5])])
N = len(out); np_ = sum(bool(o['p_positions']) for o in out); nf = sum(bool(o['f_positions']) for o in out)
print('free', N, 'pairs only in one-offs: words', sum(o['pair_only_in_oneoffs'] for o in out), 'distinct', len(pc))
print('with p', np_, 'with f', nf, 'no core', sum(o['core']=='' for o in out), '2+ gallows', sum(o['n_gallows']>=2 for o in out))
print('top pairs', pc.most_common(8)); print(collections.Counter(o['placement'] for o in out))
print(collections.Counter(o['section'] for o in out).most_common()); print(collections.Counter(o['currier'] for o in out))
for o in out[:6]: print(o['word'], o['prefix'], o['core'], o['ending'], o['p_positions'], o['f_positions'])
