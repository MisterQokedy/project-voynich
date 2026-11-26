# Catalogue of free one-off words (paper Appendix E)

This catalogue lists every "free" one-off word in the ZL3b-n transcription (EVA) for anyone who wants to examine these words directly. A free one-off occurs once in the manuscript and is at least three edits away from every frequent word (count 10 or more) and from each of the 40 words before it. There are 1,328 of them, 24% of the 5,526 one-offs. Classification, controls and statistics come from the earlier OO studies (the OO, OO-SP and OO-N entries in `results/CONSOLIDATED_FINDINGS.md`). Nothing was refitted for this catalogue; the only new computation is the word split and the pair lookup described below.

## Files

- `free_oneoffs_catalogue.csv`: one row per free one-off, with page, line, section, Currier language (blank where ZL gives none, 197 words), scribe (Davis hand), quire, position in the line, placement (paragraph 1,038; label 138; circle 127; radial 25), length, the split into prefix, core and ending, the number of gallows, the character positions of p and f, any doubled e or i, the start glyph and last two letters, a flag for start–ending pairs found only in one-offs, and the nearest frequent word with its edit distance.
- `oneoff_only_pairs.csv`: start–ending pairs that occur in free one-offs and in no word that appears twice or more, with counts and up to five example words.
- `code/build.py`: rebuilds both files from the one-off table (`work/oneoffs/oneoffs_table.csv`, made by `tools/tests/oneoffs/`) and the ZL transcription.

## How words are split

The split is a descriptive convention and makes no claim about morphology. Glyphs are read as EVA units, with cth, ckh, cph, cfh, ch and sh each counted as one unit. The **core** runs from the first gallows (k, t, p, f or a benched gallows) or bench (ch, sh) to the last one, and takes in any e or h that follows it. Everything before the core is the **prefix** and everything after it is the **ending**. For example, chepchefy splits into an empty prefix, the core chepchef and the ending y, and fachys into core fach and ending ys. Words with no gallows or bench (132 of them) get a short prefix from {qo, q, o, y, d, s, l, r} and the rest as ending. Long prefixes such as ydarai- in ydaraishy show that some free one-offs put most of their letters before the first bench.

p occurs in 250 free one-offs and f in 100; 218 have two or more gallows.

## Start–ending pairs found only in one-offs

Using the OO definition (first glyph plus last two letters), 157 free one-offs (12%) carry a pair that never appears in a recurring word, spread over 133 distinct pairs. Most pairs occur once. The commonest are p…ry (4 words) and r…ty, o…sh, t…ry, d…ed (3 each). The OO report's 30% figure is higher because it compared against frequent words only (count 10 or more); here the comparison set is every word seen at least twice.

## Known patterns with their controls

All rates below are taken from the earlier reports. Spelling rates are length-weighted to free one-off lengths 6–11, with 95% bootstrap intervals where reported.

**Doubled e or i (OO-SP, P2)**

| group | share with a doubled glyph | ee per 100 words | ii per 100 words |
|---|---|---|---|
| real free one-offs | 0.30 [0.28, 0.33] | 26 | 11 |
| real EDIT2 one-offs | 0.48 [0.44, 0.51] | 21 | 10 |
| unit-shuffled free one-offs | 0.38 [0.36, 0.41] | | |
| S6-Z generator free one-offs | 0.44 [0.42, 0.47] | 36 | 23 |
| German herbal free one-offs (own lengths) | 0.23 | | |

**Two or more gallows (OO-SP, P5)**

| group | share with 2+ gallows |
|---|---|
| real free one-offs | 0.16 [0.14, 0.18] |
| real EDIT2 one-offs | 0.085 [0.06, 0.11] |
| S6-Z generator free one-offs | 0.107 [0.09, 0.12] |

The p and f pairs are over-represented in free one-offs against all tokens more strongly than in generator one-offs: ep 7.7× (generator 3.4×), po 4.6× (2.3×), fch 3.8× (1.8×), of 3.6× (1.7×). Of the 218 multi-gallows words, 113 are mid-line, so these are not only paragraph-initial words. Unit shuffling keeps the gallows count fixed, so it is not a control for this row.

**Label enrichment (OO, C1, Holm-corrected)**

| comparison | free share of one-offs | shuffled-placement null | p |
|---|---|---|---|
| labels vs paragraphs | 0.33 vs 0.23 (+0.10) | +0.04 | 0.0015 (length-stratified 0.0005) |
| circle/radial text vs paragraphs | +0.045 | +0.031 | 0.23, not significant |
| line-first vs rest | +0.069 | −0.005 | 0.0005 (length-stratified 0.06) |

The label excess survives length control. The line-first excess mostly reflects length. The follow-up OO-L test found that label one-offs are no closer to each other across pages than matched paragraph one-offs (0.320 vs 0.323, p 0.32), so the excess does not show a shared stock of names.

## Limits

These are regularities of spelling and placement. The meaning tests on the same words failed: free one-offs do not recur as near-variants on pages with similar plant drawings (p 0.71), and their tie to same-section pages matches other one-offs of equal length. The noun-profile comparison with German herbals did no better than generated text. The catalogue is offered as material for further study and does not argue for any reading.
