# P3-c: line-edge vs mid-line pen form with trained-segmenter masks clipped at neighbours (26 Nov 2026, PC): PASS, ROBUST, pen form (not extent)

Pre-registration `PREREG.md`; masks GS (cross-fitted) clipped at the neighbouring same-line box centres (`glyphseg/code/gsfeat.py ... clip`);
analysis `code/p3.py` (P3-b's, plus a HOG-only run); output `out/p3.out`, `out/p3_result.json`; montages `out/montage_LM.png`,
`out/montage_real_LM.png`; unclipped check `out_noclip/`, `out_noclip.log` (50 perms).

| arm | real AUC | perm p | perm-null mean | HOG only | geometry only | placebo | box control (P3-b, matched) | P3-b real |
|---|---|---|---|---|---|---|---|---|
| L vs M | **0.641** | 0.005 | 0.552 | 0.633 | 0.602 | 0.482 (word 2) | 0.514 | 0.613 |
| RL vs RM | **0.587** | 0.005 | 0.520 | 0.586 | 0.566 | 0.524 (word n-1, p 0.06) | 0.518 | 0.583 |

Per class (L): t 0.90 (n 49), sh 0.72, o 0.66, s 0.65, y 0.62, q 0.61, d 0.58. (RL): n 0.66, l 0.60, y 0.57, r 0.49.
Placement matching kept |std diff| <= 0.014 on box width / height / offset.

- Pass rule (real - 0.5 >= 2 x (box - 0.5), p < 0.01): L 0.141 vs 0.028, R 0.087 vs 0.036. **Both arms pass, robust.**
- **Not extent only:** HOG-only AUC (shape of the mask, centred, extent removed) is 0.633 / 0.586, about the full AUC. In P3-b mask geometry carried
  most of the signal; with clean masks it is the pen form.
- **Clipping does not drive it:** unclipped GS masks give 0.640 / 0.579 (HOG 0.632 / 0.578).
- **By eye:** masks are clean (no line-above ink, no neighbour letters) in all but about 3-4 of 48 real-window tiles, and those are spread over both
  groups. Visible differences: line-initial y often has a long tail sweeping down-left; line-initial gallows (t) differ strongly.
- **Verdict: PASS, ROBUST.** Glyphs at the start and end of a line are drawn differently from the same glyphs mid-line, once box size and placement
  are matched and neighbour / line-above ink is removed. Caveat: the permutation null is centred above 0.5 (0.55 / 0.52) because of how pages group;
  the real AUCs beat it by 0.09 / 0.07. No claim about meaning; a pen-form habit at line edges (flourished first and last strokes) fits.

## Add-ons (26 Nov, approved by the user): split by scribe / section, and P3-d figure
Code `code/subsets.py`, `code/run_sub.sh` (p3.py unchanged, 100 perms, min 30 per class), outputs `subsets/`, `subsets_run.log`; figure `p3d_line_edge_masks.png` (`code/p3d.py`).

| subset | L vs M AUC (p) | HOG only | placebo W2 | RL vs RM AUC (p) | HOG only |
|---|---|---|---|---|---|
| Scribe 1 | 0.608 (0.06) | 0.603 | 0.419 | 0.570 (0.05) | 0.574 |
| Scribe 2 | 0.604 (0.01) | 0.601 | 0.446 | 0.547 (0.06) | 0.550 |
| Scribe 3 | 0.564 (0.05) | 0.560 | 0.427 | 0.642 (0.01) | 0.646 |
| Biological (B) | 0.586 (0.03) | 0.586 | 0.461 | 0.563 (0.04) | 0.568 |
| Herbal (H) | 0.601 (0.03) | 0.590 | 0.496 | 0.531 (0.38) | 0.528 |
| Stars (S) | 0.604 (0.03) | 0.601 | 0.441 | 0.622 (0.01) | 0.624 |

(p floor 0.0099 with 100 perms; Scribe 4/5, pharma and text-only sections too small.) **The line-initial effect is present in every scribe and section**
(AUC 0.56-0.61, all placebos <= 0.50, carried by HOG). The line-final effect is strongest in Scribe 3 and Stars, weak in Scribe 2 and absent in Herbal.
Within subsets most p values sit at 0.01-0.06, so single subsets are underpowered, but the direction never reverses.

**P3-d (descriptive):** mean masks of line-edge vs mid-line glyphs (y, t, sh, q line-initial; n, y line-final). Line-edge glyphs are more diffuse
and their ink sits higher relative to the band (red above, blue on the mid-line body in every row); line-final n has extra ink inside the upper bowl.
Caveat: the window is anchored to a band fitted along the line, which is extrapolated at line ends, so part of the higher / blurrier look may be
band-fit error; the classifier's HOG crops are centred on each mask and are not affected by this. The figure shows placement and spread more than
a single clean stroke difference.
