# P3-e resume note
State is in WSL ~/p3e_work (img/, alto/, data/, model_f*/, feat_*/). Pipeline: `wsl bash $VOYNICH_DIR/p3e/code/run.sh <step>`,
steps in order: ocr, harvest, train (2 folds ~25 min + infer), feat, p3 (or `all`; each step skips nothing except finished OCR pages).
Logs: ~/p3e_run1.log (ocr+harvest), ~/p3e_run2.log (train..p3). Results land in p3e/out/gs and p3e/out/box (p3.out, p3_result.json).
Deviation from PREREG noted for the report: Kraken ALTO glyphs are CTC peak points (width ~1 px), so letter cuts = midpoints between
consecutive peaks within each word (word box at the ends), then tightened to Otsu ink.
Deviation 2 (26 Nov ~20:50 UTC, decided from group counts only, no outcomes seen): the every-7th sample gave 48 text pages, 541 clean
exemplars and at most 30 line-initial lowercase glyphs per class (verse lines start with capitals), so ALL 621 canvases are used
(code/fetch2.sh, log ~/p3e_run1b.log ends with group counts from code/cnt.py). Then run `run.sh train`, `feat`, `p3` (P3_MINN=40 if needed).
After results: by-eye check out/montage_real_LM.png, write REPORT.md, update CONSOLIDATED_FINDINGS.md + UNTESTED_DIRECTIONS.md entries
(send to coordinator; report/repo updated later).
