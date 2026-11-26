"""Bundle 9: read every traced page with the bundle-7 Kraken ensemble (3 seeds, mean posteriors, greedy, no LM).

Reads each image in the row-trace index with two row groupings (v1 = bundle 7, v2 = rows2.py), scores both
against ZL where ZL has paragraph text, picks the primary grouping by the PREREG rule (validation pages only),
and writes a per-page and a combined IVTFF-like machine transliteration with per-line confidence.
"""
import argparse, json, math, random, re, sys, time
from pathlib import Path
import numpy as np
import torch
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import common as C, rows as R1, rows2 as R2, lineimg as LI

SMOKE_PAGES = ['f1v', 'f48v', 'f13r', 'f2r', 'f105r', 'f67r1', 'f10v']
REPLICATE_B7 = 0.107      # bundle-7 ensemble3 page CER on the test pages (v1 rows)
TOL_B7 = 0.005


class Reader:
    def __init__(self, path, device):
        from kraken.models import load_models
        from kraken.lib.dataset import ImageInputTransforms
        self.net = load_models(path)[0]; self.net.eval().to(device); self.dev = device
        b, c, h, w = self.net.input
        self.tf = ImageInputTransforms(1, h, w, c, (16, 0), valid_norm=True)
        self.codec = self.net.codec

    @torch.inference_mode()
    def probs(self, im):
        x = self.tf(im).unsqueeze(0).to(self.dev)
        logits, olens = self.net.nn(x, torch.LongTensor([x.shape[3]]))
        return logits.softmax(1).squeeze(2)[0, :, :int(olens[0])].float().cpu().numpy()   # (C, W)

    def decode(self, P):
        """greedy CTC -> (text, per-character confidence = max posterior over the character's frames)."""
        from kraken.lib.ctc_decoder import greedy_decoder
        out = self.codec.decode(greedy_decoder(torch.as_tensor(P))[0])   # [(char, start, end, max posterior)]
        return ''.join(c for c, *_ in out), [float(x[3]) for x in out]


def page_cer(rows_txt, ref):
    hyp = '\n'.join(rows_txt)
    return C.lev(hyp, ref) / max(len(ref), 1)


def mean_ci(v, n=10000, seed=20261125):
    return C.boot_ci(v, n, seed) if len(v) else None


def fmt(t):
    return f'{t[0]:.3f} [{t[1]:.3f}, {t[2]:.3f}]' if t else 'n/a'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True); ap.add_argument('--scans', required=True)
    ap.add_argument('--zl', required=True); ap.add_argument('--split', required=True)
    ap.add_argument('--prep-report', default='', help='bundle7 prep_report.json: the record of which pages trained')
    ap.add_argument('--models', required=True, help='bundle7 models.json')
    ap.add_argument('--out', required=True); ap.add_argument('--device', default='cuda:0')
    ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()
    t0 = time.time()
    out = Path(a.out); (out / 'pages').mkdir(parents=True, exist_ok=True); (out / 'samples').mkdir(exist_ok=True)
    dev = a.device if (a.device == 'cpu' or torch.cuda.is_available()) else 'cpu'

    # ---------------- split labels ----------------
    train, test = C.load_split(a.split)
    r = random.Random(20261125); tr = sorted(train); r.shuffle(tr); val = set(tr[:round(0.10 * len(tr))])
    trained_lines = {}
    if a.prep_report and Path(a.prep_report).exists():
        pr = json.load(open(a.prep_report))
        assert sorted(val) == sorted(pr['val_pages']), 'validation pages differ from the bundle-7 record'
        for p, inf in pr['pages'].items():
            trained_lines[p] = inf.get('pairs', 0) if inf['split'] == 'train' else 0
    def split_of(p):
        return 'test' if p in test else 'val' if p in val else 'train' if p in train else 'unseen'

    ZL, sect = C.parse_ivtff(a.zl)
    zl_hdr = {}
    for raw in open(a.zl, encoding='utf-8', errors='ignore'):
        m = C.HDR.match(raw.rstrip('\n'))
        if m:
            zl_hdr[m.group(1)] = m.group(2).strip()
    index = [e for e in json.load(open(Path(a.repo) / 'data' / 'index.json')) if e.get('kind') in ('page', 'foldout panel')]
    if a.smoke:
        index = [e for e in index if e['folio'] in SMOKE_PAGES]
    models = json.load(open(a.models))
    seeds = [models.get(n) for n in ('main_s1', 'main_s2', 'main_s3')]
    if not all(s and Path(s).exists() for s in seeds):
        raise SystemExit(f'missing main_s1/2/3 model files: {seeds}')
    readers = [Reader(s, dev) for s in seeds]
    print(f'transcribe: {len(index)} images, device {dev}, models {[Path(s).parent.name for s in seeds]}', flush=True)

    cache = {}       # fragment signature -> line result (shared by v1/v2 when the row is identical)
    pages = {}       # folio -> {'v1': [line], 'v2': [line], ...}
    for k, e in enumerate(index):
        p = e['folio']
        sp = Path(a.scans) / e['scan']
        if sp.exists():
            im = Image.open(sp); s, ox, oy, src = 1.0, 0.0, 0.0, 'scan'
        else:   # fallback: the repo's 1800 px display image (lower resolution; flagged in the output)
            d = e['display']; im = Image.open(Path(a.repo) / d['file']); s, ox, oy, src = d['scale'], d['scan_x0'], d['scan_y0'], 'display'
        g = LI.gray(im)
        pg = {'image': e['image'], 'scan': e['scan'], 'kind': e['kind'], 'section_traces': e.get('section'),
              'split': split_of(p), 'trained_lines': trained_lines.get(p, 0), 'source': src}
        for ver, R in (('v1', R1), ('v2', R2)):
            rows, xh = R.page_rows(a.repo, e['image'])
            lines = []
            for row in rows:
                sig = (e['image'], tuple((round(f['x0']), round(f['x1']), round(f['y'])) for f in row['frags']))
                if sig not in cache:
                    img = LI.row_image(g, row, xh, s, ox, oy)
                    Ps = [rd.probs(img) for rd in readers]
                    P = np.mean(Ps, 0)
                    txt, cf = readers[0].decode(P)
                    singles = [readers[0].decode(x)[0] for x in Ps]
                    pw = [C.lev(singles[i], singles[j]) / max(len(singles[i]), len(singles[j]), 1)
                          for i in range(3) for j in range(i + 1, 3)]
                    nb = P.argmax(0) != 0
                    cache[sig] = {
                        'text': re.sub(' +', ' ', txt).strip(),
                        'conf': round(float(np.mean(cf)) if cf else 0.0, 4),
                        'minconf': round(float(min(cf)) if cf else 0.0, 4),
                        'agree': round(1 - float(np.mean(pw)), 4),
                        'frames_nonblank': int(nb.sum()),
                        'x0': round(min(f['x0'] for f in row['frags'])), 'x1': round(max(f['x1'] for f in row['frags'])),
                        'y': round(row['y']), 'nfrag': len(row['frags']), 'width_xh': round(row['width'] / xh, 2)}
                if p in ('f1v', 'f48v'):
                    LI.row_image(g, row, xh, s, ox, oy).save(out / 'samples' / f'{p}_{ver}_{len(lines):02d}.png')
                lines.append(dict(cache[sig]))
            pg[ver] = lines
            pg[ver + '_xh'] = xh
            pg[ver + '_rows'] = rows
        pages[p] = pg
        if k % 10 == 0:
            print(f'  {k + 1}/{len(index)} {p} ({time.time() - t0:.0f}s)', flush=True)

    # ---------------- scores vs ZL ----------------
    res = {'n_images': len(pages), 'device': dev, 'models': seeds, 'pages': {}}
    for p, pg in pages.items():
        info = {'split': pg['split'], 'kind': pg['kind'], 'source': pg['source'], 'rows_v1': len(pg['v1']), 'rows_v2': len(pg['v2'])}
        if p in ZL:
            labels = [t for _, t, _ in ZL[p]]; ref = '\n'.join(labels); info['zl_loci'] = len(labels)
            for ver in ('v1', 'v2'):
                info['cer_' + ver] = page_cer([l['text'] for l in pg[ver]], ref)
                pairs, pinfo = R1.pair_rows(pg[ver + '_rows'], pg[ver + '_xh'], labels)
                info['paired_' + ver] = len(pairs)
                for ri, li in pairs:
                    l = pg[ver][ri]; l['zl_locus'] = ZL[p][li][0]
                    l['zl_cer'] = round(C.lev(l['text'], labels[li]) / max(len(labels[li]), 1), 4)
        res['pages'][p] = info
    scored = [p for p in res['pages'] if 'cer_v1' in res['pages'][p]]
    by = lambda s: [p for p in scored if res['pages'][p]['split'] == s]
    S = {}
    for s in ('train', 'val', 'test', 'unseen'):
        ps = by(s)
        S[s] = {'n': len(ps)}
        for ver in ('v1', 'v2'):
            S[s][ver] = mean_ci([res['pages'][p]['cer_' + ver] for p in ps])
        if ps:
            S[s]['v2_minus_v1'] = C.paired_boot([res['pages'][p]['cer_v2'] for p in ps], [res['pages'][p]['cer_v1'] for p in ps])
    res['by_split'] = S
    # PREREG G1: v2 is primary unless it is worse on validation pages (upper CI of v2 - v1 >= 0.005)
    dv = S['val'].get('v2_minus_v1')
    primary = 'v2' if (dv is None or dv[2] < 0.005) else 'v1'
    if a.smoke:
        primary = 'v2'
    res['primary'] = primary
    # replication of bundle 7 (v1 rows, test pages)
    res['replicate_b7'] = S['test']['v1'][0] if S['test']['v1'] else None
    # shuffled-image control on held-out pages (test + unseen with ZL text): another page's reading for this page
    held = [p for p in scored if res['pages'][p]['split'] in ('test', 'unseen')]
    der = C.derange_within(held, {p: sect.get(p, '?') for p in held}) if len(held) > 1 else {}
    own = [res['pages'][p]['cer_' + primary] for p in held]
    shuf = [page_cer([l['text'] for l in pages[der[p]][primary]], '\n'.join(t for _, t, _ in ZL[p])) for p in held]
    res['shuffled_image_minus_real_heldout'] = C.paired_boot(shuf, own) if held else None
    # confidence calibration on paired held-out lines
    pl = [l for p in held for l in pages[p][primary] if 'zl_cer' in l]
    if len(pl) > 10:
        from scipy.stats import spearmanr
        rho = spearmanr([l['conf'] for l in pl], [l['zl_cer'] for l in pl])
        rho_a = spearmanr([l['agree'] for l in pl], [l['zl_cer'] for l in pl])
        q = np.quantile([l['conf'] for l in pl], [0.25, 0.5, 0.75])
        bins = [[l for l in pl if l['conf'] <= q[0]], [l for l in pl if q[0] < l['conf'] <= q[1]],
                [l for l in pl if q[1] < l['conf'] <= q[2]], [l for l in pl if l['conf'] > q[2]]]
        res['calibration'] = {'n_lines': len(pl), 'spearman_conf_vs_cer': float(rho[0]), 'p': float(rho[1]),
                              'spearman_agree_vs_cer': float(rho_a[0]),
                              'conf_quartile_edges': [float(x) for x in q],
                              'line_cer_by_conf_quartile': [float(np.mean([l['zl_cer'] for l in b])) if b else None for b in bins]}

    # ---------------- outputs ----------------
    def ivtff(p, pg, ver):
        hdr = zl_hdr.get(p, '').strip()
        hv = hdr[2:-1].strip() if hdr.startswith('<!') and hdr.endswith('>') else ''
        L = [f'<{p}>      <! {hv} $K={pg["split"]}{" $D=display" if pg["source"] != "scan" else ""} >'.replace('  $K', ' $K')]
        for i, l in enumerate(pg[ver]):
            words = '.'.join(l['text'].split(' '))
            tag = f'c={l["conf"]:.3f},m={l["minconf"]:.3f},a={l["agree"]:.3f}' + (f',zl={l["zl_locus"]}' if 'zl_locus' in l else '')
            L.append(f'<{p}.{i + 1},{"@" if i == 0 else "+"}P0>      {words}<!{tag}>')
        return L
    order = [e['folio'] for e in index]
    head = ['#=IVTFF Eva- 2.0 M 5',
            '# Machine transliteration, project bundle 9: Kraken 7.1.1 ensemble of 3 seeds (bundle 7 main_s1..s3),',
            f'# mean frame posteriors, greedy CTC, no language model. Row grouping {{ver}}. Traces commit in traces_commit.txt.',
            '# Each locus is one machine text row, numbered top to bottom; it is NOT a ZL locus. All rows use type P0;',
            '# labels, ring text and stray marks are not separated (see lines.tsv: width_xh, nfrag, x0, x1, y).',
            '# $K = role of the page in training the reader: train (lines trained on), val (early stopping only),',
            '#      test (held out, scored in bundle 7), unseen (not in the split, never used). Held-out = test + unseen.',
            '# $D=display marks a page read from the lower-resolution display image because its scan was missing.',
            '# Inline <!c=mean char confidence, m=min char confidence, a=3-seed agreement, zl=paired ZL locus>.']
    for ver in ('v1', 'v2'):
        tag = 'primary' if ver == primary else 'alt'
        L = [h.replace('{ver}', ver) for h in head]
        H = list(L)
        for p in order:
            blk = ivtff(p, pages[p], ver)
            L += blk
            if pages[p]['split'] in ('test', 'unseen'):
                H += blk
            if ver == primary:
                (out / 'pages' / f'{p}.txt').write_text('\n'.join(blk) + '\n', encoding='utf-8')
        name = 'voynich_kraken_b9' if ver == primary else f'voynich_kraken_b9_{ver}rows'
        (out / f'{name}.txt').write_text('\n'.join(L) + '\n', encoding='utf-8')
        if ver == primary:
            (out / 'voynich_kraken_b9_heldout.txt').write_text('\n'.join(H) + '\n', encoding='utf-8')
    cols = ['page', 'row', 'split', 'kind', 'grouping', 'text', 'conf', 'minconf', 'agree', 'nfrag', 'width_xh', 'x0', 'x1', 'y', 'zl_locus', 'zl_cer']
    with open(out / 'lines.tsv', 'w', encoding='utf-8') as f:
        f.write('\t'.join(cols) + '\n')
        for p in order:
            for ver in ('v1', 'v2'):
                for i, l in enumerate(pages[p][ver]):
                    d = dict(l, page=p, row=i + 1, split=pages[p]['split'], kind=pages[p]['kind'], grouping=ver)
                    f.write('\t'.join(str(d.get(c, '')) for c in cols) + '\n')
    res['seconds'] = round(time.time() - t0)
    json.dump(res, open(out / 'scores.json', 'w'), indent=1)

    # ---------------- summary ----------------
    M = []
    M.append(f'# Bundle 9 results: machine transliteration of {len(pages)} traced images\n')
    M.append(f'Primary row grouping: **{primary}** (rule: v2 unless worse on validation pages). Device {dev}, {res["seconds"]} s.\n')
    rb = res['replicate_b7']
    if rb is not None and not a.smoke:
        ok = abs(rb - REPLICATE_B7) <= TOL_B7
        M.append(f'- R1 replication of bundle 7 (v1 rows, test pages): {rb:.3f} vs {REPLICATE_B7} → {"met" if ok else "NOT met"}')
    M.append(f'- Shuffled-image control on held-out pages (other page − own): {fmt(res["shuffled_image_minus_real_heldout"])}')
    if 'calibration' in res:
        c = res['calibration']
        M.append(f'- Confidence vs line CER on {c["n_lines"]} paired held-out lines: Spearman {c["spearman_conf_vs_cer"]:.3f} '
                 f'(agreement: {c["spearman_agree_vs_cer"]:.3f}); line CER by confidence quartile (low→high): '
                 + ', '.join(f'{x:.3f}' if x is not None else 'n/a' for x in c['line_cer_by_conf_quartile']))
    M.append('\n| Pages | n | Page CER v1 rows | Page CER v2 rows | v2 − v1 |')
    M.append('|---|---|---|---|---|')
    for s in ('train', 'val', 'test', 'unseen'):
        M.append(f'| {s} | {S[s]["n"]} | {fmt(S[s]["v1"])} | {fmt(S[s]["v2"])} | {fmt(S[s].get("v2_minus_v1"))} |')
    for p in ('f1v', 'f48v'):
        if p in res['pages'] and 'cer_v1' in res['pages'][p]:
            i = res['pages'][p]
            M.append(f'\n{p}: CER v1 {i["cer_v1"]:.3f} ({i["rows_v1"]} rows) → v2 {i["cer_v2"]:.3f} ({i["rows_v2"]} rows), ZL has {i["zl_loci"]} lines')
    worst = sorted(((res['pages'][p]['cer_' + primary], p) for p in held), reverse=True)[:8]
    M.append('\nWorst held-out pages (' + primary + '): ' + ', '.join(f'{p} {c:.2f}' for c, p in worst))
    nd = [p for p in order if pages[p]['source'] != 'scan']
    if nd:
        M.append(f'\nRead from display images (scan missing): {len(nd)}: {", ".join(nd[:20])}')
    nl = sum(len(pages[p][primary]) for p in order)
    M.append(f'\nRows read: {nl} ({primary}); images: {len(pages)}; pages with ZL paragraph text scored: {len(scored)}.')
    (out / 'RESULTS_SUMMARY.md').write_text('\n'.join(M) + '\n', encoding='utf-8')
    print('\n'.join(M))


if __name__ == '__main__':
    main()
