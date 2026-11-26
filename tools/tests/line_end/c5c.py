import sys, json, random, collections, numpy as np
sys.path.insert(0, './work/line_end/code'); from parse import parse, gg
V = './work/'
def finals_pages(pages_lines, flags=None):
    """returns list of pages; each page list of (paragraph id, final word)"""
    out = []
    for pi, p in enumerate(pages_lines):
        q = []; par = 0
        for li, l in enumerate(p):
            l = [w for w in l if w]
            if len(l) >= 2: q.append((par, l[-1]))
            if flags and flags[pi][li]: par += 1
        if len(q) >= 3: out.append(q)
    return out
def rr(a, b, k): ga, gb = gg(a), gg(b); return len(ga) >= k and len(gb) >= k and ga[-k:] == gb[-k:]
def stat(F, d):
    s1 = s2 = n = 0
    for q in F:
        for i in range(len(q) - d):
            if q[i][0] != q[i + d][0]: continue
            n += 1; s1 += rr(q[i][1], q[i + d][1], 1); s2 += rr(q[i][1], q[i + d][1], 2)
    return (s1 / n, s2 / n, n) if n else (np.nan, np.nan, 0)
def null(F, d, r):
    s1 = s2 = n = 0
    for q in F:
        for i in range(len(q) - d):
            if q[i][0] != q[i + d][0]: continue
            j = r.randrange(len(q) - 1); j += j >= i
            n += 1; s1 += rr(q[i][1], q[j][1], 1); s2 += rr(q[i][1], q[j][1], 2)
    return s1 / n, s2 / n
def test(F, NP=1000, seed=1):
    r = random.Random(seed); out = {}
    for d, nm in ((1, 'adj'), (2, 'alt')):
        o = stat(F, d); N = np.array([null(F, d, r) for _ in range(NP)])
        out[nm] = dict(r1=o[0], r2=o[1], n=o[2], ratio1=o[0] / N[:, 0].mean(), ratio2=o[1] / N[:, 1].mean(),
                       p1=(1 + np.sum(N[:, 0] >= o[0])) / (NP + 1), p2=(1 + np.sum(N[:, 1] >= o[1])) / (NP + 1))
    return out
def show(name, t): print(f"{name:42s} " + ' | '.join(f"{k}: r2 {v['r2']:.3f} x{v['ratio2']:.2f} p {v['p2']:.4f}; r1 x{v['ratio1']:.2f} p {v['p1']:.4f} (n {v['n']})" for k, v in t.items()), flush=True)
res = {}
VP = parse(V + 'transcriptions/ZL3b-n.txt')
for tag, sel in (('voynich all', lambda p: True), ('voynich A', lambda p: p['L'] == 'A'), ('voynich B', lambda p: p['L'] == 'B')):
    P = [p for p in VP if sel(p)]; F = finals_pages([[l['w'] for l in p['lines']] for p in P], [[l['pe'] for l in p['lines']] for p in P])
    res[tag] = test(F); show(tag, res[tag])
b8 = json.load(open(V + 'regional/comparison/comparison_pages_b8.json')); TX = {k: b8[k] for k in b8 if '_ms' in k}
for f in ('mhg_pages', 'htr_pages'): TX.update(json.load(open(V + f'regional/{f}.json')))
for k, pages in TX.items(): res[k] = test(finals_pages(pages), NP=300); show(k, res[k])
occ = res['occitan']; cal = min(occ['adj']['p2'], occ['alt']['p2']) < 0.01 and max(occ['adj']['ratio2'], occ['alt']['ratio2']) > 1
pv = lambda t: min(1, 2 * min(t['adj']['p2'], t['alt']['p2']))
present = cal and all(pv(res[t]) < 0.01 for t in ('voynich all', 'voynich A', 'voynich B'))
absent = res['voynich all']['adj']['p2'] > 0.05 and res['voynich all']['alt']['p2'] > 0.05
v = 'CALIBRATION FAIL' if not cal else 'RHYME PRESENT' if present else 'RHYME ABSENT' if absent else 'UNCLEAR'
print('calibration (Occitan verse) ok:', cal, '| verdict:', v); res['verdict'] = v
json.dump(res, open(V + 'c5/c5c.json', 'w'), indent=1, default=float)
