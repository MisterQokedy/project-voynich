# P3-e: control hand for P3-c (pre-registered 26 Nov 2026, ~20:45 UTC, before any control data are processed)

**Question.** P3-c found line-initial / line-final Voynich glyphs differ in pen form from the same glyph mid-line (AUC 0.641 L vs M,
0.587 RL vs RM, HOG-only 0.633 / 0.586). Is this a generic property of 15th-century hands, or unusual?

**Control.** BSB Clm 5905 (Ebersberg, 1479, Vitus Auslasser; Macer *de viribus herbarum* and Latin herbal / remedy prose), Latin,
gothic cursive book hand, IIIF from api.digitale-sammlungen.de (bsb00092488). One manuscript only (credit limit).
Pages: canvases 10..600, every 7th (about 85 images, full resolution); pages with no text lines simply contribute nothing.

**Boxes.** Kraken 7.1 baseline segmentation (default blla) + recognition with the CATMuS-Medieval model; letter boxes = Kraken
per-character cut polygons (bounding box), words = OCR text split on spaces. Only lowercase letter classes are used (a capital is a
different class, so verse capitals at line start never enter a comparison). Abbreviation marks / punctuation are dropped from classes
but kept for word position counts.
**Masks.** Windows cut exactly as glyphseg/harvest.py (x-height band fitted from a, o, e, i, n, u, m, c boxes; U = 20 px; 96 x 64).
GS segmenter retrained from scratch on this manuscript's own clean exemplars with the identical recipe (train.py, 2 folds by page parity,
cross-fitted infer.py). Features: gsfeat.py logic with neighbour clipping ("clip"), identical feature set and HOG.
**Analysis.** p3c/code/p3.py unchanged (placement matching on box w / h / dy, HOG + geometry, page-grouped CV, 200 permutations,
placebos W2 and RP, HOG-only and geometry-only reports). pstart = first line of each text block is excluded (no paragraph mark data);
lines with < 4 words excluded by p3.py as before.
**Box control.** Same p3.py on features from an ellipse inscribed in each letter box instead of the GS mask.

**Outcomes (decided now).**
- An arm "shows the effect" if it passes P3-c's rule: perm p < 0.01 and real AUC - 0.5 >= 2 x (box-control AUC - 0.5), placebo below half the effect.
- If the control shows an effect with HOG-only AUC within 0.05 of the Voynich value (or above it) in an arm: the Voynich line-edge effect
  is **ordinary scribal behaviour** for that arm (P3-c becomes uninformative about the script).
- If the control arm fails, or its HOG-only AUC is >= 0.07 below the Voynich value: Voynich line-edge marking is **stronger than in a
  normal hand** for that arm.
- In between: **inconclusive** for that arm.
- If fewer than 3 classes reach p3.py's minimum (80 per group; lowered to 40 via P3_MINN only if needed, stated in the report), or the GS
  validation montage shows the masks fail on this hand (> 1 in 5 tiles contaminated): **NOT TESTABLE**.

**Caveats fixed in advance.** Kraken CTC cuts are less exact than the Voynich letter model's boxes (adds noise, biases towards no effect);
cursive ligatures make clean exemplars rarer; one manuscript, one hand family.
