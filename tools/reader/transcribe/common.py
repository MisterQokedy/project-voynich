"""Shared helpers for bundle 7 (Kraken line reader). Pure Python + numpy."""
import json, re, os, random
from pathlib import Path
import numpy as np

UNK = '?'          # one unreadable glyph in a reference; the model never outputs it, so it always costs one error
LOC = re.compile(r'^<(f\d+[rv]\d*)\.(\d+[a-z]?),(.)(\w)(\w*)>\s*(.*)$')
HDR = re.compile(r'^<(f\d+[rv]\d*)>\s*(.*)$')


def clean(t):
    """IVTFF line text -> (EVA text with single spaces, n_unreadable). Rules fixed in PREREG.md."""
    t = re.sub(r'<!.*?>', '', t)                 # inline comments
    t = t.replace('<%>', '').replace('<$>', '')  # paragraph start/end marks
    t = t.replace('<->', '.')                    # gap for a drawing -> word space
    t = re.sub(r'<[^>]*>', '', t)                # any other tag
    t = re.sub(r'\[([^:\]]*)(:[^\]]*)?\]', r'\1', t)   # [a:b] alternatives -> first reading
    t = re.sub(r'@\d+;', UNK, t)                 # rare glyph codes -> unreadable
    t = t.replace('{', '').replace('}', '').replace("'", '')
    t = t.replace('*', UNK).replace('!', '').replace('%', '')
    t = re.sub(r'[.,]+', ' ', t)                 # certain and uncertain word spaces -> space
    t = re.sub(r'[^a-z? ]', '', t.lower())
    t = re.sub(r' +', ' ', t).strip()
    return t, t.count(UNK)


def parse_ivtff(path):
    """-> (loci: {page: [(locus_id, text, n_unk)] in file order, P loci only}, section: {page: $I})."""
    loci, sect = {}, {}
    for raw in open(path, encoding='utf-8', errors='ignore'):
        raw = raw.rstrip('\n')
        m = HDR.match(raw)
        if m:
            s = re.search(r'\$I=(\w)', m.group(2))
            if s:
                sect[m.group(1)] = s.group(1)
            continue
        m = LOC.match(raw)
        if not m:
            continue
        page, num, _pos, typ, _sub, text = m.groups()
        if typ != 'P':
            continue
        txt, nu = clean(text)
        if txt:
            loci.setdefault(page, []).append((f'{page}.{num}', txt, nu))
    return loci, sect


def norm_folio(x):
    if isinstance(x, dict):
        for k in ('folio', 'page', 'id', 'name', 'image', 'file', 'path'):
            if k in x:
                return norm_folio(x[k])
        return None
    s = Path(str(x)).stem.lower()
    m = re.search(r'f?(\d+[rv]\d*)', s)
    return 'f' + m.group(1) if m else None


def load_split(path):
    """data\\split.json -> (train folios, test folios). Accepts the common layouts; fails loudly otherwise."""
    d = json.load(open(path))
    if isinstance(d, dict):
        keys = {k.lower(): k for k in d}
        tr = next((d[keys[k]] for k in ('train', 'train_pages', 'fit') if k in keys), None)
        te = next((d[keys[k]] for k in ('test', 'test_pages', 'heldout', 'held_out') if k in keys), None)
        if tr is None or te is None:   # {folio: 'train'|'test'}
            vals = {str(v).lower() for v in d.values()}
            if vals <= {'train', 'test'}:
                tr = [k for k, v in d.items() if str(v).lower() == 'train']
                te = [k for k, v in d.items() if str(v).lower() == 'test']
    else:
        raise SystemExit(f'split.json: unrecognised layout (top level is {type(d).__name__})')
    if tr is None or te is None:
        raise SystemExit(f'split.json: no train/test lists found; keys = {list(d)[:10]}')
    tr = sorted({norm_folio(x) for x in tr} - {None}); te = sorted({norm_folio(x) for x in te} - {None})
    if set(tr) & set(te):
        raise SystemExit(f'split.json: pages in both train and test: {sorted(set(tr) & set(te))[:10]}')
    return tr, te


def lev(a, b):
    """Levenshtein distance between two sequences."""
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def boot_ci(vals, n=10000, seed=20261125, stat=np.mean):
    v = np.asarray(vals, float); r = np.random.default_rng(seed)
    idx = r.integers(0, len(v), (n, len(v)))
    bs = np.array([stat(v[i]) for i in idx]) if stat is not np.mean else v[idx].mean(1)
    return float(stat(v)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def paired_boot(a, b, n=10000, seed=20261125):
    """mean(a-b) with a page-bootstrap 95% CI."""
    return boot_ci(np.asarray(a, float) - np.asarray(b, float), n, seed)


def derange_within(pages, sect, seed=20261121):
    """Fixed derangement of test pages within section; singleton sections are paired across sections."""
    r = random.Random(seed); out = {}
    groups = {}
    for p in sorted(pages):
        groups.setdefault(sect.get(p, '?'), []).append(p)
    left = []
    for s, g in sorted(groups.items()):
        if len(g) < 2:
            left += g; continue
        g = g[:]; r.shuffle(g)
        for i, p in enumerate(g):
            out[p] = g[(i + 1) % len(g)]
    if left:
        pool = sorted(pages)
        for p in left:
            out[p] = r.choice([q for q in pool if q != p])
    return out
