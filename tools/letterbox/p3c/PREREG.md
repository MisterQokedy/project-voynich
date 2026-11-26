# P3-c: line-edge vs mid-line pen form with GS masks clipped at neighbours (pre-registered 26 Nov 2026, ~20:55 UTC, before the masks exist)

P3-b passed (L vs M AUC 0.613, RL vs RM 0.583) but most of the signal sat in mask extent, possibly from neighbour or line-above ink.
P3-c reruns P3-b's analysis (`p3.py` unchanged: placement matching on box width / height / vertical offset, HOG + mask geometry classifier,
grouped CV by page, 200 permutations, placebo) with the GS segmenter masks (cross-fitted by sheet fold), further **clipped at neighbours**:
mask columns beyond the centre of the previous / next same-line letter box are cleared (`gsfeat.py ... clip`).

**Arms and pass rule as P3-b:** an arm passes if real AUC - 0.5 >= 2 x (box-render AUC - 0.5) and perm p < 0.01. Box-render control: the P3-b
matched, uncleaned rendered-ellipse control (out_box_noclean) is reused as the reference (it does not depend on masks).
**Extra, to address the P3-b caveat:** the same classifier with HOG only (no mask-extent geometry) is reported; if the HOG-only AUC is < 0.55
in an arm, that arm's result is called "extent only".
**By-eye check (required before the verdict):** montage of 16 L and 16 M masks per class (`montage_LM.png`) and a real-window montage of
24 random L and 24 random M glyphs with the clipped mask in red. If masks visibly include neighbour or line-above ink in more than 1 in 5 tiles,
or the L and M rows differ only by such contamination, the verdict is NOT ROBUST.
**Prerequisite:** GS passes its validation (glyphseg/PREREG.md); if GS fails for all classes, P3-c is not run.
