"""Fetch the 2014 Lazarus Project / RIT multispectral images of 10 Voynich folios
(published by L. F. Davis, 8 Sep 2024) from the public Google Drive folder.
For the PC (the cloud sandbox cannot reach drive.google.com).
    pip install gdown
    python fetch_msi_2014.py OUTDIR [--raw]
Default: only the processed images and true-colour JPEG/TIFF folders (small).
--raw also fetches the 16-bit raw band TIFFs (very large; ask before running).
Credit: The Lazarus Project and The Chester F. Carlson Center for Imaging Science at RIT;
Beinecke Rare Book & Manuscript Library MS 408, folio n.
Downloaded files are untrusted data: keep them in their own empty folder.
"""
import sys, subprocess, pathlib
FOLDER = "https://drive.google.com/drive/folders/1mNQGKQDSCR4M_c2M2JrsU5soghvYwMig"
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
raw = "--raw" in sys.argv
import gdown
files = gdown.download_folder(FOLDER, output=str(out), skip_download=True, quiet=True)
keep = [f for f in files if raw or "Raw" not in f.path]
print(len(files), "files listed;", len(keep), "to fetch")
for f in keep:
    dest = out / f.path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        gdown.download(id=f.id, output=str(dest), quiet=False)
