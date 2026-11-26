"""Build the line datasets for bundle 7. Test pages: images cut for every row, never written to any training list."""
import argparse, json, os, random, shutil, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import common as C, rows as R, lineimg as LI

VAL_SHARE, VAL_SEED, SHUF_SEED = 0.10, 20261125, 20261126


def link(src, dst):
    try:
        os.link(src, dst)
    except OSError:
        shutil.copyfile(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True); ap.add_argument('--scans', default='')
    ap.add_argument('--source', choices=['scan', 'display'], default='scan')
    ap.add_argument('--zl', required=True); ap.add_argument('--it', required=True)
    ap.add_argument('--split', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--max-pages', type=int, default=0, help='smoke: limit pages per split')
    a = ap.parse_args()
    out = Path(a.out); (out / 'rows').mkdir(parents=True, exist_ok=True)
    ZL, sect = C.parse_ivtff(a.zl); IT, _ = C.parse_ivtff(a.it)
    train, test = C.load_split(a.split)
    idx = {e['folio']: e for e in json.load(open(Path(a.repo) / 'data' / 'index.json')) if e.get('kind') == 'page'}
    if a.max_pages:
        train, test = train[:a.max_pages], test[:max(2, a.max_pages // 4)]
    r = random.Random(VAL_SEED); tr = sorted(train); r.shuffle(tr)
    val = set(tr[:round(VAL_SHARE * len(tr))])
    report = {'train_pages': len(train), 'test_pages': len(test), 'val_pages': sorted(val), 'pages': {}}
    lines = {'train': [], 'val': []}; testdata = {}
    reg_warn = []
    for page in sorted(set(train) | set(test)):
        e = idx.get(page)
        info = {'split': 'test' if page in test else ('val' if page in val else 'train')}
        report['pages'][page] = info
        if e is None or page not in ZL:
            info['skip'] = 'no row traces' if e is None else 'no P text'; continue
        rows, xh = R.page_rows(a.repo, e['image'])
        if not rows:
            info['skip'] = 'no rows'; continue
        if a.source == 'scan':
            im = Image.open(Path(a.scans) / e['scan']); s, ox, oy = 1.0, 0.0, 0.0
            d = e['display']
            need_w, need_h = d['scan_x0'] + d['w'] / d['scale'], d['scan_y0'] + d['h'] / d['scale']
            if im.size[0] + 2 < need_w * 0.99 or im.size[1] + 2 < need_h * 0.99:
                raise SystemExit(f'{page}: scan {e["scan"]} is {im.size}, smaller than the traced region ({need_w:.0f}x{need_h:.0f})')
        else:
            d = e['display']; im = Image.open(Path(a.repo) / d['file']); s, ox, oy = d['scale'], d['scan_x0'], d['scan_y0']
        g = LI.gray(im)
        pdir = out / 'rows' / page; pdir.mkdir(exist_ok=True)
        paths = []
        for k, row in enumerate(rows):
            p = pdir / f'{page}_{k:03d}.png'
            if not p.exists():
                LI.row_image(g, row, xh, s, ox, oy).save(p)
            paths.append(str(p))
        loci = ZL[page]; labels = [t for _, t, _ in loci]
        pairs, pinfo = R.pair_rows(rows, xh, labels)
        info.update(rows=len(rows), loci=len(loci), pairs=len(pairs), r=pinfo['r'], kept=pinfo['kept'])
        itmap = {lid: t for lid, t, _ in IT.get(page, [])}
        if page in test:
            testdata[page] = {
                'rows': paths, 'section': sect.get(page, '?'),
                'ref_zl': '\n'.join(labels),
                'ref_it': '\n'.join(t for _, t, _ in IT.get(page, [])),
                'pairs': [{'row': ri, 'locus': loci[li][0], 'zl': loci[li][1], 'it': itmap.get(loci[li][0])}
                          for ri, li in pairs]}
        else:
            for ri, li in pairs:
                lid, t, nu = loci[li]
                if nu:
                    continue
                lines['val' if page in val else 'train'].append(
                    {'img': paths[ri], 'page': page, 'locus': lid, 'zl': t, 'it': itmap.get(lid)})
    # leak guard: no test page in any training/validation list
    assert not {l['page'] for v in lines.values() for l in v} & set(test), 'test page leaked into training data'

    def write_arm(name, items_tr, items_val):
        d = out / 'arms' / name
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        man = {}
        for part, items in (('train', items_tr), ('val', items_val)):
            ps = []
            for i, (img, txt) in enumerate(items):
                dst = d / f'{part}_{i:05d}.png'
                link(img, dst); (d / f'{part}_{i:05d}.gt.txt').write_text(txt + '\n', encoding='utf-8')
                ps.append(str(dst))
            (d / f'{part}.txt').write_text('\n'.join(ps) + '\n'); man[part] = len(ps)
        return man

    tr_zl = [(l['img'], l['zl']) for l in lines['train']]; va_zl = [(l['img'], l['zl']) for l in lines['val']]
    arms = {'main': write_arm('main', tr_zl, va_zl)}
    rs = random.Random(SHUF_SEED)
    lt = [t for _, t in tr_zl]; rs.shuffle(lt); lv = [t for _, t in va_zl]; rs.shuffle(lv)
    arms['shuflab'] = write_arm('shuflab', [(i, t) for (i, _), t in zip(tr_zl, lt)], [(i, t) for (i, _), t in zip(va_zl, lv)])
    two = tr_zl + [(l['img'], l['it']) for l in lines['train'] if l['it'] and '?' not in l['it']]
    arms['twolab'] = write_arm('twolab', two, va_zl)
    (out / 'test.json').write_text(json.dumps(testdata))
    report['arms'] = arms
    (out / 'prep_report.json').write_text(json.dumps(report, indent=1))
    # training-page text for the synthetic lines and the side LM (train pages only, never test)
    with open(out / 'train_text.txt', 'w') as f:
        for p in sorted(set(train) - set(test)):
            for _, t, nu in ZL.get(p, []):
                if not nu:
                    f.write(t + '\n')
    kept = sum(1 for p in report['pages'].values() if p.get('kept'))
    print(f"prep: train lines {arms['main']['train']}, val lines {arms['main']['val']}, "
          f"test pages {len(testdata)} ({sum(len(v['pairs']) for v in testdata.values())} paired test lines), "
          f"pages paired {kept}/{len(report['pages'])}")


if __name__ == '__main__':
    main()
