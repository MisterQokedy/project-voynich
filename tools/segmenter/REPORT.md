# GS: trained per-glyph segmenter (26 Nov 2026, PC GPU): PASSES validation (n marginal)

Pre-registration `PREREG.md`; code `code/` (harvest.py, train.py, infer.py, gsfeat.py, view.py); rendered eval `eval_render.json`;
by-eye montages `val_model_f0/f1.png` (model), `val_base_f0/f1.png` (H10g baseline, same tiles); exemplar check `smoke_clean.png`;
rendered-scene check `render0.png`. Work data and masks in WSL `~/glyphseg_work/` (masks_model.npy, cross-fitted, one per letter window).

- **Training data:** 82,155 letter windows (U = 20 px). 37,086 clean exemplars (o 7,302 ... k 129, t 48, ckh 47, cth 23). By eye the
  exemplar masks are whole glyphs (first k exemplars kept the attached e; a neighbour-core rule was added before the full harvest).
  Gallows exemplars are few, because k and t usually touch the next glyph.
- **Model:** U-Net (32-256 channels), 3 input channels (grey, target box, other boxes), 30 epochs x 600 steps x 64 rendered scenes per fold,
  ~11 min per fold on the RTX 5060. Two sheet folds, cross-fitted.
- **Gate 1, rendered held-out scenes (IoU, model / baseline):** fold-0 model: k 0.954 / 0.814, t 0.953 / 0.805, n 0.977 / 0.874;
  fold-1 model: k 0.942 / 0.826, t 0.933 / 0.825, n 0.979 / 0.882 (other classes 0.97-0.98 / 0.77-0.90). PASS (>= 0.80, >= +0.05).
- **Gate 2, by eye on real held-out letters (48 per class per fold, my scoring of each tile):**

| class | model fold 0 | model fold 1 | baseline fold 0 | baseline fold 1 |
|---|---|---|---|---|
| k | ~44/48 (92 %) | ~45/48 (94 %) | ~38/48 | ~40/48 |
| t | ~44/48 (92 %) | ~44/48 (92 %) | ~41/48 | ~41/48 |
| word-final n after i | ~42/48 (88 %) | ~40/48 (83 %) | ~37/48 | ~36/48 |

  PASS for all three (>= 80 %, above baseline). Model failures: misplaced P2-W boxes (the mask follows the box), a truncated gallows loop
  now and then, and for n speckled masks on noisy vellum or a stray stroke from the line above. Baseline failures are mostly line-above
  ink inside gallows masks and truncated, faint n's.
- Gate 3 (stroke-measure montages) is checked in H10h.
- **Caveat:** the scoring is my own by-eye judgement of each tile, not an independent hand annotation; counts are approximate (+-2).
