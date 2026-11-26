# Appendix E: catalogue of free one-off words {.appendix .unnumbered}

This appendix summarises a catalogue of the one-off words that the generator fails to reproduce (Section 6.2). A **free one-off** occurs once in the ZL3b-n transliteration (EVA) and is at least three edits away from every frequent word (count 10 or more) and from each of the 40 words before it. There are 1,328 of them, 24% of the 5,526 one-offs. Classification, controls and statistics come from the earlier one-off studies (OO, OO-SP, OO-N, OO-L in Appendix A). Nothing was refitted for the catalogue; the only new computation is a descriptive word split and a pair lookup.

**Full lists in the repository.** The complete data are in `data/oneoff_catalogue/` at https://github.com/MisterQokedy/project-voynich:

- `free_oneoffs_catalogue.csv`: all 1,328 free one-offs, one row each, with page, line, section, Currier language, scribe (Davis hand), quire, position in the line, placement (paragraph 1,038; label 138; circle 127; radial 25), length, a prefix–core–ending split, gallows count, positions of p and f, doubled e or i, start glyph and last two letters, a flag for start–ending pairs found only in one-offs, and the nearest frequent word with its edit distance.
- `oneoff_only_pairs.csv`: the 133 start–ending pairs (first glyph plus last two letters) that occur in free one-offs and in no word seen twice or more, with counts and up to five example words.
- `code/build.py`: rebuilds both files from the one-off table and the ZL transliteration.

The prefix–core–ending split is a descriptive convention, not a claim about morphology: the core runs from the first gallows or bench (ch, sh) to the last, and takes in any e or h that follows. Of the free one-offs, 250 contain p, 100 contain f and 218 have two or more gallows. 157 (12%) carry a start–ending pair that never appears in a recurring word; most pairs occur once, and the commonest are p…ry (4 words) and r…ty, o…sh, t…ry and d…ed (3 each).

## E.1 Doubled e or i {.unnumbered}

Spelling rates are length-weighted to free one-off lengths 6–11, with 95% bootstrap intervals.

| Group | Share with a doubled glyph | ee per 100 words | ii per 100 words |
|---|---|---|---|
| Real free one-offs | 0.30 [0.28, 0.33] | 26 | 11 |
| Real one-offs within two edits of a recent word | 0.48 [0.44, 0.51] | 21 | 10 |
| Unit-shuffled free one-offs (control) | 0.38 [0.36, 0.41] | | |
| S6-Z generator free one-offs (control) | 0.44 [0.42, 0.47] | 36 | 23 |
| German herbal free one-offs, own lengths (control) | 0.23 | | |

## E.2 Stacked gallows {.unnumbered}

| Group | Share with two or more gallows |
|---|---|
| Real free one-offs | 0.16 [0.14, 0.18] |
| Real one-offs within two edits of a recent word | 0.085 [0.06, 0.11] |
| S6-Z generator free one-offs (control) | 0.107 [0.09, 0.12] |

The p and f pairs are over-represented in free one-offs, against all tokens, more strongly than in generator one-offs: ep 7.7× (generator 3.4×), po 4.6× (2.3×), fch 3.8× (1.8×), of 3.6× (1.7×). Of the 218 multi-gallows words, 113 are mid-line, so these are not only paragraph-initial words. Unit shuffling keeps the gallows count fixed, so it is not a control for this table.

## E.3 Placement: label enrichment {.unnumbered}

Holm-corrected; the null shuffles placement labels.

| Comparison | Free share of one-offs | Shuffled-placement null | p |
|---|---|---|---|
| Labels vs paragraphs | 0.33 vs 0.23 (+0.10) | +0.04 | 0.0015 (length-stratified 0.0005) |
| Circle and radial text vs paragraphs | +0.045 | +0.031 | 0.23, not significant |
| Line-first vs rest of line | +0.069 | −0.005 | 0.0005 (length-stratified 0.06) |

The label excess survives length control; the line-first excess mostly reflects length. Label one-offs are no closer to each other across pages than matched paragraph one-offs (0.320 vs 0.323, p 0.32), so the excess does not point to a shared stock of names.

## E.4 Limits {.unnumbered}

These are regularities of spelling and placement. Tests of meaning on the same words failed: free one-offs do not recur as near-variants on pages with similar plant drawings (p 0.71), their tie to same-section pages matches other one-offs of equal length, and a noun-profile comparison with German herbals did no better than generated text. The catalogue is offered as material for further study and does not argue for any reading.
