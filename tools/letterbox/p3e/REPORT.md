# P3-e: control hand for P3-c (26 Nov 2026, PC). L arm: ORDINARY (the control shows the same, larger effect); R arm: formally "Voynich stronger", but the gap is small

Pre-registration `PREREG.md` (two deviations, both decided before any outcome was seen, listed in `RESUME.md`: Kraken ALTO glyphs are CTC
peak points, so letter cuts = midpoints between peaks, tightened to ink; all 621 canvases used instead of every 7th, because the sample gave
<= 30 line-initial lowercase letters per class).
Control: BSB Clm 5905 (Ebersberg 1479, Vitus Auslasser; Macer verse + Latin remedy prose, gothic cursive). 336 text pages, 6,047 lines,
157k letters with features; GS retrained on this hand's own clean exemplars (~4,000), rendered validation IoU 0.94-0.98 (baseline 0.70-0.80).
Code `code/` (harvest_ctl.py, gsfeat_ctl.py, run.sh; p3.py, train.py, infer.py unchanged copies). Output `out/gs/`, `out/box/`, montage `out/montage_real_LM.png`.
P3_MINN = 40 (as the prereg allowed); 11 classes in each arm.

| arm | control AUC (p) | HOG only | geometry only | placebo | box control | Voynich P3-c AUC / HOG only |
|---|---|---|---|---|---|---|
| L vs M (line-initial) | **0.681** (0.005) | 0.680 | 0.560 | W2 0.522 (p 0.05) | 0.381 | 0.641 / 0.633 |
| RL vs RM (line-final) | 0.556 (0.005) | 0.554 | 0.545 | RP 0.532 (p 0.015) | 0.432 | 0.587 / 0.586 |

Per class (control L): h 0.92, f 0.87, p 0.81, l 0.71, d 0.68, m 0.66, a 0.63, o 0.63, c 0.59, e 0.57, i 0.55, n 0.55. (R): d 0.68, i 0.61, e 0.60, n 0.59, m 0.58, a 0.57, t 0.55, s 0.54, u 0.50, r 0.47, o 0.44.

- **L arm: PASS in the control** (p 0.005, placebo 0.022 below half the effect, box control below 0.5). Control HOG-only 0.680 is *above* the
  Voynich 0.633. **Pre-registered outcome: the Voynich line-initial effect is ordinary scribal behaviour.** A normal 15th-century Latin
  hand marks line-initial letters at least as strongly. By eye (montage, top 3 rows L): line-initial letters are often enlarged or near-capital
  forms (long-stemmed l, h, f, p; a capital-like a), which OCR still labels lowercase. That is a real scribal habit at line start, and the
  Voynich effect (flourished line-initial y, gallows) looks like the same kind of thing.
- **R arm: FAIL in the control** (p 0.005, but the RP placebo, 0.532, is above half the effect). By the prereg rule that means "Voynich line-final
  marking is stronger than in this hand". But the AUC gap is only 0.03 (HOG 0.586 vs 0.554, below the 0.07 margin), and the control's word n-1
  placebo is raised too, so a fair reading is: both hands show at most a weak line-final effect; Voynich's is a little clearer.
- **Box control** comes out *below* 0.5 (0.38 / 0.43) because 1:1 placement matching on box size leaves ellipse features anti-informative under
  page-grouped CV. It does not threaten the pass rule (the rule only needs real - 0.5 >= 2 x (box - 0.5)), but it is not a clean 0.5 reference.
- **By eye:** masks are clean in about 44 of 48 tiles (a few partial or small); contamination well under 1 in 5, spread over both groups.
- Caveats: one manuscript, cursive, with verse sections (verse lines start with capitals; those are a separate class and never compared, but
  near-capital forms labelled lowercase do enter the L arm); Kraken cuts are coarser than the Voynich letter boxes (that adds noise, so it biases towards no effect).

**Verdict:** P3-c's line-initial result is **not evidence of anything unusual** about the Voynich script. A known-language control hand shows
it as strongly or more. The line-final effect is weak in both hands. Formally the Voynich value is stronger, but only by 0.03 AUC.
