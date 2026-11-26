"""Download the archive.org scans (item 'voynich') that the row traces were drawn on, for the split's pages."""
import argparse, json, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import common as C

URL = 'https://archive.org/download/voynich/{}'


def ok(p):
    try:
        with Image.open(p) as im:
            im.verify()
        return True
    except Exception:
        return False


def get(name, out):
    p = out / name
    if p.exists() and ok(p):
        return name, 'cached'
    for i in range(5):
        try:
            req = urllib.request.Request(URL.format(name), headers={'User-Agent': 'research-script/1.0'})
            with urllib.request.urlopen(req, timeout=120) as r, open(p, 'wb') as f:
                f.write(r.read())
            if ok(p):
                return name, 'ok'
        except Exception as e:
            err = e
        time.sleep(5 * (i + 1))
    return name, f'FAILED'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True); ap.add_argument('--split', required=True); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    tr, te = C.load_split(a.split)
    want = set(tr) | set(te)
    idx = [e for e in json.load(open(Path(a.repo) / 'data' / 'index.json')) if e.get('kind') == 'page' and e['folio'] in want]
    names = sorted({e['scan'] for e in idx})
    print(f'fetch: split has {len(tr)} train / {len(te)} test pages; {len(idx)} have row traces; {len(names)} scans to get')
    missing = sorted(want - {e['folio'] for e in idx})
    if missing:
        print(f'fetch: no row traces for {len(missing)} split pages: {missing}')
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda n: get(n, out), names))
    bad = [n for n, s in res if s == 'FAILED']
    print(f'fetch: {len(res) - len(bad)} scans ready, {len(bad)} failed {bad[:10]}')
    if bad:
        sys.exit(2)


if __name__ == '__main__':
    main()
