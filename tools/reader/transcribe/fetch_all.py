"""Download every archive.org scan (item 'voynich') that has row traces, skipping scans already present.
Reuses bundle 7's scan folder, so only the pages outside the bundle-7 split are new."""
import argparse, json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from fetch import get   # same downloader and checks as bundle 7


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True); ap.add_argument('--out', required=True); ap.add_argument('--smoke', action='store_true')
    a = ap.parse_args()
    idx = [e for e in json.load(open(Path(a.repo) / 'data' / 'index.json')) if e.get('kind') in ('page', 'foldout panel')]
    if a.smoke:
        from transcribe import SMOKE_PAGES
        idx = [e for e in idx if e['folio'] in SMOKE_PAGES]
    names = sorted({e['scan'] for e in idx})
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    print(f'fetch_all: {len(idx)} traced images on {len(names)} scans', flush=True)
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda n: get(n, out), names))
    bad = [n for n, s in res if s == 'FAILED']
    print(f'fetch_all: {sum(s == "cached" for _, s in res)} already present, {sum(s == "ok" for _, s in res)} downloaded, '
          f'{len(bad)} failed {bad[:10]} (failed pages are read from the 1800 px display images and flagged)')


if __name__ == '__main__':
    main()
