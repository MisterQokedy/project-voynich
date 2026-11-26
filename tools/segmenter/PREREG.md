# GS: trained per-glyph segmenter (pre-registered 26 Nov 2026, ~19:50 UTC, before any training)

**Why.** H10f, H10g, P3-b and P4-L-c stalled because threshold-and-cut masks pick up neighbour ink and line-above ink, or cut the glyph short.
GS trains a small segmenter that, given a letter window and its P2-W box, returns the ink of that letter only.

## Data
- Every P2-W letter (82,272 boxes, 166 pages) is cut into a window normalised to x-height U = 20 px: box centre +-1.6 U wide,
  band top - 2.2 U to band bottom + 1.6 U (96 x 64 px). Inputs: grey window, target-box channel, other-boxes channel.
- **Clean exemplars** (`code/harvest.py`): letters whose Otsu components touching the box core lie >= 80 % inside the box (+0.2 U),
  enter no other box beyond 15 % of their ink, cover >= 95 % of the box's ink, are not window-clipped, are >= 0.6 U tall, and take
  <= 20 % of the ink in any other box's core. Their masks are taken as true glyph masks. Checked by eye on a montage before training.
- **Training scenes are rendered, so the true mask is known:** a real letter context (the classes and box positions of all letters in a
  real window, including the line above and below) is re-drawn with clean exemplars of the same classes, each placed at its context box,
  on a paper background made from a real window with its ink closed out. Ink combines multiplicatively, so neighbours can touch and overlap
  the target as in real writing. The target's true mask is its exemplar mask. Augmentation: box jitter +-0.15 U, ink strength,
  contrast, blur, noise.
- **Sheet folds:** sheets (quire-bifolium) are split at random (seed 0) into 2 folds. Model A trains on fold-0 exemplars and contexts only and
  is applied to fold-1 pages; model B the reverse. Every downstream mask comes from the model that never saw that sheet.

## Model
Small U-Net (4 levels, 32-256 channels), BCE + Dice loss, AdamW, mixed precision, on the RTX 5060.

## Validation gates (all must pass, for each fold model, on the held-out fold)
1. **Rendered held-out scenes** (exemplars and contexts from held-out sheets): mean IoU >= 0.80, and >= 0.05 higher than the
   H10g threshold-and-cut baseline on the same scenes. Reported separately for k, t, n.
2. **By eye on real held-out letters** (the main gate): montages of 48 random held-out k, 48 t and 48 word-final n after i, model mask in red
   over the real window. A tile is acceptable if the mask covers the whole letter and no more than a small sliver of other ink
   (no neighbour letter, no line-above ink, no truncated stroke). Gate: >= 80 % acceptable for each of k, t and n, and higher than the
   H10g baseline on the same tiles (baseline montage scored the same way).
3. The k-crossbar and n-tail measure montages (16 lowest vs 16 highest) must show visibly shorter vs longer crossbars / tails.

If gate 1 or 2 fails for a class, the segmenter is reported as **failed for that class**, and tests that need that class stop there.
If it fails for all of k, t and n, GS is reported as FAILED and H10h, P3-c, P4-L-d are not run with it.

## Downstream (each pre-registered in its own folder before running): H10h, P3-c, P4-L-d.
