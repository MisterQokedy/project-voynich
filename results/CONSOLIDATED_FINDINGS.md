<!-- Research log synced from the project's working files (paper v1.1, 26 Nov 2026). Folder names refer to the original working tree, not all of which is in this repository. -->

# Voynich page-order project: consolidated findings (internal reference)

Version 3, 21 Nov 2026 (09:19 UTC); 22 Nov additions include M5, D4, D5 (all negative, §13b), S16 (Greshko's code, FAIL) and H10 (Archetype palaeography, inconclusive) in §13b, and the PC overnight bundle (S4 held-out PASS for split A, S2/S3 PASS, S8-P, S6, S5, M3 FAIL) plus drawings v2 (FAIL) in §13b. Adds plan steps 1–4 (§13b). Adds the final calibration results (§9) and the language and decipherment tests (§13). The plan for next steps is in `plan/DECIPHERMENT_PLAN.md`.

This is an internal reference for later threads, not a publication. It merges every thread's results, organised by question. Each section gives the result, the numbers, the controls, the caveats and where the files are. Where threads disagree, it says so (see also the contradictions list near the end).

**Ground rules (unchanged):** every claim is tested against shuffled or random controls; negative results are stated plainly. Decipherment work is now allowed, but a reading counts only if it holds on held-out pages and beats generated and shuffled text. Nothing so far says anything about what the text means.

## 0. The question, and the short answer

**Hypothesis under test (Layfield & Davis 2026, *Digital Medievalist* 19, doi 10.4000/16k0a):** the manuscript began as loose folded bifolia ("singulions") read in sequence, and was later nested into quires in the wrong order, so the original reading order can be recovered from the text. Timm's review (voynich.ninja thread 5911) accepts that same-sheet pages are similar but says the sequence recovery has no random baseline.

**Short answer so far:**

1. **The bifolium was the unit of writing (confirmed, strong).** Pages on the same sheet share vocabulary far beyond scribe, language and illustration controls, and the four pages of a sheet look written in the order Xr→Xv→Yr→Yv.
2. **The text cannot recover which sheet came next (negative, robust).** No sheet-order search beats a shuffled-page baseline in any of 9 quires. The published Layfield & Davis orders are reproducible but sit at the level random page assignments reach. Quire 20 is the only borderline case (p ≈ 0.06–0.14), and preliminary calibration says a p like that cannot tell "no sequence" from "herbal-like text with a true sequence".
3. **The physical evidence fits the current nesting, which is old.** Leaf-to-leaf stain and discolouration patterns match the current nesting best of all nestings in 6 of 9 quires, and quire 20's water stain is impossible for a stack of loose singulions. That shows the current nesting predates the damage. It does not show the nesting is the author's original.
4. **Two illustration continuities are real** (78v|81r streams, 33v|40r blue petals). They show those two sheets lay flat or open with their inner spread exposed at some point. That fits singulions, but equally fits decoration before sewing.
5. **No physical trace of an earlier, different facing order was found** (paint offsets, gutter paint). This negative is weak because the methods miss most offsets. The literature's quire-20 paint transfers and Dulov's wormholes, checked at full resolution, both fit the current stack (§5d).
6. **Skin side is random with respect to the binding** (no Gregory's rule, no consistent side out). This is consistent with sheets folded one at a time, but does not distinguish loose singulions from a careless quire maker.
7. **Wear measured from photographs is mostly a photography artefact** and cannot be used without position-matched controls.

## 1. Threads and sources

| Thread | Status | Main output |
|---|---|---|
| Test Voynich mis-binding hypothesis | done | `VOYNICH_HANDOFF_v2.md` (findings 8–14); v1 handoff (findings 1–7) is in `uploads/hearth/19f96944-783f-4aae-a432-420dffb662eb`; scripts `voynich_scripts_v2.zip` |
| Analyze reordering across whole manuscript | done | Doc "Voynich: manuscript-wide reordering analysis" ; code and outputs `manuscript_wide/` |
| Apply two evidence-based page reorders | done | `reorder/REORDER_NOTE.md`, `reorder/proposed_reading_order.csv`: current binding with Q13 sheets 78\|81 and 79\|80 swapped (78v faces 81r) and Q5 sheet 33\|40 moved to the quire centre (33v faces 40r) |
| Check claimed illustration continuities | done | `continuity/CONTINUITY_REPORT.md`, panels `continuity/*.jpg`, `gutter_baseline.txt` |
| Map physical evidence of sheet order | done | `physical_offsets/` (code, score matrices, figures); summary in that thread's final reply |
| Review proposed Voynich page orders | done | Doc "Voynich page order: literature review" ; `page-order-review/proposed_orders.csv`, `proposed_orders_pages.csv` |
| Calibrate ordering methods on known texts | done (quire 13 shape finished 22 Nov, S17, §9b) | `calibration/CALIBRATION_RESULTS.md`, `calibration/results/` |
| Study how sheets were composed | done | `sheets_as_units/SHEETS_AS_UNITS.md` |
| Test whether plant type explains sheet links | done | `plant_drawings/PLANT_DRAWINGS.md` |
| Test labels as anchors for word meaning | done | `labels/LABELS_AS_ANCHORS.md` |
| Test whether the text behaves like language | done | `language_test/REPORT.md` |
| Test word families across herbal and pharma | done | `word_families/REPORT.md` |
| Test text against a fitted Timm generator | done | `timm_generator/REPORT.md`, `REPORT2.md` |
| Test grammar-like structure and label captions | done | `grammar_labels/REPORT.md` |
| Score published decipherments on held-out pages | done | `decipherment_harness/REPORT.md`, `KEYS.md` |
| Plan novel routes toward decipherment | done | `plan/DECIPHERMENT_PLAN.md` |

All paths below are relative to `voynich/` unless they start with `page-order-review/` or `uploads/` (relative to ``).

**Data used by all threads**
- Transcription: Zandbergen–Landini ZL3b-n (IVTFF 2.0, v3b, 13 May 2025), from www.voynich.nu. Headers give `$Q` quire (A=1 … M=13, T=20), `$B` bifolium, `$F` leaf position, `$H` Davis hand, `$L` Currier A/B, `$I` illustration type. Parsed: 226 page entries, 38,090 words (202 pages after dropping pages under 20 words in the manuscript-wide thread). Parsed copy: `manuscript_wide/pages2.json`.
- Images: Yale IIIF manifest 2002046, full size (~2,700×3,800 px), 183 single pages in `yale_images/` (fold-outs excluded from physical tests). Folio→URL maps: `manuscript_wide/canvases.tsv`, `canvas.tsv` in the zip. The earlier work (findings 6, 7) used the user's 2006 Beinecke PDF at ~1,100×1,500 px.
- Papers: Layfield & Davis PDF and Timm review PDF in `uploads/hearth/` (the 3-page and 13-page PDFs).
- Calibration text: `forme_of_cury_pg8102.txt` (Gutenberg via the pglaf mirror).
- Network allowlist includes collections.library.yale.edu, www.voynich.nu, gutenberg.org + gutenberg.pglaf.org, archive.org, voynich.ninja, thelatinlibrary.com, la.wikisource.org. Image work needs `pip install opencv-python-headless`.

**Known bug to avoid:** f116v has 2 words, which forces sheet 103|116 to the end of any text-based order. Test with f116r as that sheet's last page as well.

---

## 2. Do pages on the same sheet share text? (same-sheet similarity)

**Result: YES, strongly. CONFIRMED by two threads with independent code.**

Numbers (manuscript-wide, `manuscript_wide/t1.out`; z against stratified null):

| Pair type | n | TF-IDF z | LSA z | Jaccard z |
|---|---|---|---|---|
| Confoliate (Xr\|Xv, Yr\|Yv) | 71 | +7.4 | +6.2 | +6.6 |
| Inner conjoint (Xv\|Yr) | 36 | +5.7 | +7.4 | +3.7 |
| Same sheet, distance 2 (Xr\|Yr, Xv\|Yv) | 71 | +3.8 | +3.9 | +3.0 |
| Outer conjoint (Yv\|Xr) | 35 | +2.0 | +1.9 | +2.1 (p ≈ 0.02–0.04) |
| Facing in binding, different sheets | 72 | −0.4 | −0.6 | 0.0 |

- Earlier (v1 finding 1, TF-IDF, 2006 setup): conjoint z ≈ +4.6, confoliate z ≈ +6.8. Robust to metric and to comma handling.
- By section: herbal confoliate z +5.7, stars +4.1, balneological +2.1. Facing pairs near zero in every section (herbal +1.2, balneo −1.9, stars −0.2).

**Control:** each real pair is compared with random pairs of pages on *different* sheets of the same quire, matched on hand, Currier language and illustration type. This removes Timm's Currier A/B confound.

**Caveat:** this shows a sheet was written as a unit. It does not show the sheets were read as singulions; a scribe filling one folded sheet at a time before nesting gives the same signal (Timm's "unit of production" reading).

## 3. In what order were the four pages of a sheet written? (within-sheet sequence)

**Result: Xr→Xv→Yr→Yv, i.e. written as a folded sheet in reading order. Upgraded from "suggestive" (v1) to "fairly strong" (manuscript-wide).**

- Inner conjoint beats outer conjoint in 27 of 35 sheets with LSA (sign-flip p = 0.0008), TF-IDF p = 0.047, Jaccard p = 0.19 (n.s.).
- Fitting all 12 four-page orders: Xr→Xv→Yr→Yv wins with TF-IDF (bootstrap 52%) and LSA (89%). Jaccard prefers Xr→Xv→Yv→Yr (42%).
- v1 finding 3 had pooled p ≈ 0.01 and paired per-sheet p ≈ 0.06 on 32 sheets.
- Interpretation: if each open spread had been written at one sitting, the outer spread Yv|Xr would be as similar as the inner one; it is not.

**Caveat:** fits singulions and equally fits "fill a folded sheet, then nest it". Cannot separate the two.
Files: `manuscript_wide/t1.out` (T2), `t3.out` (T3); `sheet_pairs.py`, `inner_outer.py` in the zip.

## 4. Can the text recover the order of sheets? (sheet sequence from text)

**Result: NO. NEGATIVE across every quire, metric and thread.**

### 4a. Exhaustive search vs shuffled-page null, all quires with ≥3 complete sheets
(`manuscript_wide/t3.out`, T4; singulion model; null = real pages shuffled into random slots, full search rerun, best-minus-median gap compared)

| Quire | Sheets | Orders | p TF-IDF | p LSA | p Jaccard | Binding rank (TF-IDF) |
|---|---|---|---|---|---|---|
| 1 (A) | 4 | 24 | 0.95 | 0.97 | 0.78 | 3 |
| 2 (B) | 3 | 6 | 0.99 | 0.23 | 0.69 | 1 |
| 3 (C) | 4 | 24 | 0.34 | 0.06 | 0.59 | 9 |
| 4 (D) | 4 | 24 | 0.79 | 0.45 | 0.76 | 22 |
| 5 (E) | 4 | 24 | 0.90 | 0.98 | 0.89 | 3 |
| 6 (F) | 4 | 24 | 0.78 | 0.92 | 0.72 | 14 |
| 7 (G) | 4 | 24 | 0.97 | 0.89 | 0.97 | 2 |
| 13 (M) | 5 | 120 | 0.75 | 0.42 | 0.56 | 81 |
| 20 (T) | 6 | 720 | 0.45 | 0.12 | 0.28 | 384 |
| Fisher combined | | | 0.997 | 0.55 | 0.985 | |

- v1 finding 4 (quires 13 and 20 only): p = 0.26–0.75 over 6 tests; winners unstable across metric and bootstrap. The quire 20 chain 107|112 → 108|111 → 103|116 was bootstrap-stable (75–97%) but its links are not unusual once you allow best-of-30 selection (p > 0.5).
- The binding order is also unremarkable on text (rank anywhere from 1 to 22 of 24). **The text says nothing about whether the current order is right or wrong.**

### 4b. Exact rebuild of Layfield & Davis LSA (mis-binding thread, finding 12)
Pipeline: their stop-word heuristic (w = 6, v = 3 → 29 stop words), ~40-word documents (722; 719 in the manuscript-wide rebuild), TF-IDF, SVD k = 75, pages folded in, cosine. Score = mean cosine at singulion transitions (Yv of sheet i → Xr of sheet i+1). Statistic = best minus median over all orders. `lsa_reorder.py` in the zip.

- **Quire 20:** their order 105|114 → 104|115 → 106|113 → 107|112 → 108|111 → 103|116 comes out exactly #1 of 720, for k = 25–150 and with f116r in place of f116v. Shuffled-page null (3,000 perms): 0.170 vs null 0.135, **p = 0.056** (f116v); 0.158 vs 0.134, **p = 0.14** (f116r).
- **Quire 13:** their order ranks 2 of 120, their second choice 3. Best order here: 77|82 → 75|84 → 78|81 → 76|83 → 79|80. Null: 0.118 vs 0.121, **p = 0.52**.
- Their reported 12–20% "improvement" compares a best-of-720 singulion score with the nested facing score. Different quantities; Timm §4.3 stands.

### 4c. Positive control on Voynich text of known order (manuscript-wide, T5)
- Within a page, adjacent 30-word chunks are slightly more alike than chunks 6+ apart (cosine 0.049 vs 0.036; different-sheet baseline 0.028).
- Pseudo-sheets built from consecutive chunks: the true order ranks first in 7.9% of 63 tests (chance 4.2%); mean percentile 0.41 (chance 0.50, p = 0.005).
- So sequence signal exists in Voynich text but is far too weak to pick out an order. Most similarity is "same page/same sheet", not "next".

### 4d. Are quires textual units? (T6)
- Hand-1 / Currier A herbal sheets (21 sheets, quires 1–7): same-quire minus other-quire similarity −0.0007, p = 0.56. No decay with quire distance (r = −0.10, p = 0.15). Leave-one-out: a sheet's nearest quire is its own for 2 of 21 (null 3.7, p = 0.86).
- The text gives no grouping of sheets into quires, so it cannot confirm or overturn the quires.

### 4e. Timm's Experiment 3, held-out A/B gradient (T7)
- 27 herbal sheets seriated on vocabulary with all <ed> and -dy forms removed. Still splits B from A completely (6 B, then 21 A).
- Held-out <ed> rate falls inside B (Spearman −0.83, n = 6, p = 0.03), flat inside A (+0.13, p = 0.72). A step for A, a possible slope at the B end. Six B sheets is too few to settle it.

**Caveats for section 4:** the methods are weak even on known-order Voynich chunks (4c). A negative here means "not recoverable by these methods", not "no original order existed". Section 9 (calibration) is what decides how much a negative or a borderline p means.

## 5. What does the physical evidence say about sheet order?

### 5a. Stain and discolouration sharing (manuscript-wide, results 7–8; mis-binding finding 11)
**Result: the current nesting fits best, in most quires. CONFIRMED. It cannot recover any earlier order.**

Method: each page cut to its interior, reduced to a 48×64 grid of parchment brightness (80th percentile per cell) and yellowness; versos mirrored to leaf frame; recto and verso averaged to a leaf map; high-passed. Every possible stack is scored by summed correlation of physically touching leaves, over all nestings and all singulion stacks.

| Quire | Sheets | Current nesting rank | Best singulion stack vs current |
|---|---|---|---|
| 1 (A) | 4 | 1/24 | 0.34 vs 1.31 |
| 2 (B) | 3 | 1/6 | 0.49 vs 0.64 |
| 3 (C) | 4 | 1/24 | 1.00 vs 1.36 |
| 4 (D) | 4 | 1/24 | 0.59 vs 1.17 |
| 5 (E) | 4 | 7/24 | 0.81 vs 0.51 |
| 6 (F) | 4 | 16/24 | 0.22 vs 0.31 |
| 7 (G) | 4 | 2/24 | 0.89 vs 0.88 |
| 13 (M) | 5 | 1/120 | 3.02 vs 2.87 |
| 20 (T) | 6 | 1/720 | 4.78 vs 7.03 |

- Mean percentile of current nesting across 9 quires 0.13 (0 = best; p < 0.0001). Holds on all four feature settings (0.13–0.19, p ≤ 0.0003). Quire 20 is rank 1 or 2 of 720 on every setting; quire 13 ranks 1, 4, 6 and 10 of 120. Quires 5 and 6 do not follow the pattern. (`manuscript_wide/p1.out`)
- **Quire boundary control:** neighbouring leaves inside a quire correlate 0.22; neighbouring leaves across a quire boundary 0.11 (p = 0.016; yellowness 0.43 vs 0.29, p = 0.007), lower than leaves four apart inside a quire (0.14). Photo drift or the curve of the open book would carry across boundaries, so the pattern belongs to the quires. (`p1b.out`)
- **Quire 20 water stain (finding 11):** tide line at top centre, faint on f107r, growing through 108–112, peak f113–f115r, gone by f116. Current binding is best of all 46,080 nestings (720 orders × 64 flips); no singulion stack comes close (minimum total variation 20.4 vs 9.1). Stained leaves 107, 108, 111, 112, 113, 114, 115 cover the conjoint halves of 104|115, 105|114 and 106|113 without their partners, which is impossible in a stack of folded singulions. Brown blob f103r/v continues onto f104r/v (binding-adjacent). Controls: random regions elsewhere rank the binding order only modestly (median 5.6% of nestings better; quire 13 random regions 27%). Figures: `figures/q20_stain_maps_*.png`, `figures/q20_top_stain_*.jpg`.
- Mis-binding thread's manuscript-wide tone scan: conjoint leaves not more alike than distance-matched pairs on darkness (p = 0.20), marginally on yellowness (p = 0.04, shared skin likely). No stain links leaves far apart in the binding.

**Caveats:** old is not original. The stains show the current nesting predates the damage; they cannot rule out a short loose-sheet phase before that, or a re-nesting before the damage. The Beinecke shot leaves in foliation order, so an independent image set (e.g. the 2006 scans) would make this firmer. Segmentation is coarse; fold-outs (quires 9–12, 14, parts of 15, 17, 19) are excluded.

### 5b. Paint offsets and show-through (physical-offsets thread; manuscript-wide p3)
**Result: only the current binding is visible. NEGATIVE, and the test is WEAK.**

- Show-through from the next leaf down is visible in 12.9% of neighbouring pairs and never in the reverse direction (the control). Example: f23r visible through f22r. This proves the detector works but is a property of the photography. **Anyone reading ghosts by eye should know a faint image can come from the leaf underneath.** Figure: `physical_offsets/figures/next_leaf_showthrough_f23r_f22r_f27v_f28v.jpg`, `f22r_f22v_f23r.jpg`.
- True offsets from the current facing page: ~3% of facing pairs vs 0.3% of random pairs. Best case: red berries of f17v printed on f18r (`physical_offsets/figures/offset_f17v_f18r.jpg`).
- Non-facing verso|recto pairs score no higher than pairs that can never touch. Each sheet's inner spread scores no higher than its outer spread (p = 0.86); the inner spread is where a loose-sheet phase would leave offsets.
- Manuscript-wide independent detector: vs same-quire random pairs, neither current facing pairs (p = 0.98) nor inner conjoint pairs (p = 0.76) show more transfer. 10v|15r is the top inner-conjoint score (+0.49), but see 7 below. (`manuscript_wide/p3.out`)
- Weakness: even centuries of current binding are mostly undetected, so a short loose-sheet phase cannot be ruled out. Sewing holes and tears are hidden in the gutter in these photos; Beinecke conservation notes or UV imaging would be the next source.
- Reproducibility note: `physical_offsets/code/*.py` hard-code a scratchpad path from that thread (`/tmp/claude-0/.../scratchpad`). Edit the `S=` line to point at `physical_offsets/` before rerunning. Score matrices are saved as `.npy` (`M_m*.npy`, `SH*.npy`, `Z_*.npy`) with `names.json`.

### 5c. Gutter-crossing paint, automated (manuscript-wide, p2)
**Result: INCONCLUSIVE.** Inner conjoint spreads r = +0.24 (n = 6, p = 0.07); current facing spreads +0.14 (n = 21, p = 0.10). Top inner pairs 33v|40r (+0.62), 34v|39r and 25v|32r (+0.51). Ink: nothing (p = 0.29–0.47). Too few pages carry paint at the gutter; the strip method misses 78v|81r, which is clear by eye. See section 7 for the visual check.

### 5d. Literature constraints at full resolution (P7/P9 thread, 22 Nov, `physical_p7p9/REPORT.md`, pre-registered)
**Result: the literature's quire-20 evidence supports the CURRENT stack; nothing shows an earlier order.**
- **What the sources say** (checked 22 Nov): Pelling's quire-20 transfers are f116r→f115v (top two red stars) and f113v→f115r (6th red star, "past the vellum edge flaw on f114"). Both are on pages that touch in the current binding, so the old note that they "contradict Dulov" was an over-reading. No source was found for "84v|78r" or "Q9 knife cuts, never sewn".
- **Q20-a, confirmed:** f115v has two red specks ~7 mm from the gutter at the heights of f116r's top two red stars (current facing pair). **Q20-b, confirmed:** f115r has an orange-red dot at the height of f113v's 6th red star (±0.5 mm), inside the window of a large semicircular flaw in f114's outer edge. The paint crossed the gap in f114, which needs 113–114–115 stacked with the flaw aligned (current order), or 113v facing 115r directly. Figures `physical_p7p9/figures/T2_*`. The four-way decoy blinding failed (wormholes and folio numbers identify the pages), but no decoy showed a matching mark.
- **84v|78r: not seen.** No transfer on f78r or on the decoys. **Q9 (f67/f68) folds: clean**, with no cuts, slits or sewing holes visible.
- **Dulov's wormholes, confirmed and in the current order:** the main track (gutter side, ~22% down) is absent on f111–f112 and grows strictly f113 (pinholes ~1 mm) < f114 (~1.5 mm) < f115 (2–3 mm) < f116 (3–5 mm, tunnels on f116v against the back board), with both faces agreeing. That is a worm entering from the back board through the current stack. A second set (outer edge, ~62% down) is on f115 and **also on f116** (contra the article). On f114 it falls inside the edge flaw, where there is no vellum. Figures `T3_*`.
- **Automated offset scores (T1):** no power. Most of these pages get no score, and the detector finds only 1.7–2.3% of current facing pairs.
- **Round 2 (22 Nov):** **84v|78r** is Pelling's drawing-continuity claim (Q13 centre spread, mirrored "pineapple"). Tested as a continuity: **FAIL**. Automated gutter score P = 0.15, the blinded pick missed, and no line crosses the join; a matching scaly motif sits at the top of both gutters. **Q9:** the "knife cuts" claim has no source (closest: Davis/Zyatts, "sewing in the wrong valley-fold"). The spine thread is visible, but the valley can't be judged from the photos. **P7-F: the f114 edge flaw fixes the stack.** f115r's red dot (≈9 mm from the edge), f113v's 6th red star (same height ±0.5 mm, ≈9 mm) and the second-set wormholes all fall inside f114's ≈14 mm-deep semicircular edge flaw. So f113–f114–f115 lay stacked in the current order, edges aligned, while the paint was fresh. **P9-D:** no published hair/flesh data is reachable (Claston's 2009 list is not online).

## 6. Skin side (hair vs flesh) and Gregory's rule

**Result: the two faces of each sheet differ consistently (CONFIRMED); orientation is random with respect to the binding (NEGATIVE for any planned scheme).**

- Sheet consistency (does Xr−Xv agree with Yv−Yr, the same face?), 41 bifolia, null pairs each leaf difference with another sheet's: grain r = +0.56 (p = 0.0001), yellowness b* r = +0.73 (p < 0.0001, 88% sign agreement), a* r = +0.43 (p = 0.004), L* none. Grainier face is also the yellower face (r = +0.56) → labelled hair side (an inference). (`skin_side_results.txt`)
- Independent follicle-speck count (finding 13; 3–40 px isolated dark specks per megapixel): sheet-consistent r = +0.74, 95% sign agreement; agrees with the grain+colour label on 30/30 classified sheets; r = +0.93 with the label score. By eye on quire G sheet 3 (f51r/f54v) the predicted hair faces are yellower and speckled.
- Manuscript-wide replication with independent code, 42 bifolia: spot density r = +0.78, texture r = +0.76 (both p = 0.0001, 88%), yellowness r = +0.34 (p = 0.013). (`manuscript_wide/p4.out`)
- Recto/verso imaging bias cancels or works against agreement, so it cannot produce the result.

Orientation:

| Run | Classified | Hair side out | Adjacent pairs alternating | Shuffle null | p |
|---|---|---|---|---|---|
| Mis-binding, grain+colour (finding 9) | 30/41 | 17 | 9/16 | 8.4 | 0.48 |
| Mis-binding, 3 features (finding 13) | 41/41 | 22 (binomial p = 0.76) | 15/30 | 15.1 | 0.62 |
| Manuscript-wide (independent) | 37/42 | 18 | 13/24 | 12.2 | 0.43 |

- Gregory's rule is impossible in *any* nesting order for quires 1, 7, 8, 13 and 20 (5 of 10 multi-sheet quires; ~5.6 expected under random orientation). Quire 1 (A) has hair side in on all 4 sheets. Quire 20 in binding order: I O O O I ? (mis-binding) / I O O O I O (manuscript-wide).
- Interpretation: sheets folded one at a time with no attention to skin side. Does not distinguish planned loose singulions from a careless quire maker. Classifier disagreement between features ~27% in the first run (reduced by the follicle feature).
- Hair side is only marginally resolved at ~16 px/mm. Confirming by eye on high-contrast sheets (quire G sheet 3, +4.7; quire T sheet 5, −3.2) or asking Beinecke for a collation with hair/flesh notes would firm it up.
- **By-eye check (P9, 22 Nov, `physical_p7p9/REPORT.md` T5, pre-registered): FAIL.** In a blinded 2AFC on grey, contrast-normalised vellum patches, only 5/16 strong leaves agree with the automated hair label (p = 0.96; 9/14 decided trials opposite, n.s.). Same-face controls drew 1 confident pick in 8. Flaws: the patch picker avoided specks, and control patches repeated main-trial patches. The sheet-consistency measurement stands, but "grainier/yellower = hair" is still unconfirmed by eye at this resolution.
- **P9-B rerun (random patches, fresh controls, pre-registered): FAIL, 3/16**, but 11/14 decided calls are *opposite* the label (two-sided p = 0.057). My picks repeat across the two runs (11/13 leaves the same face, with different patches). So the faces differ visibly and the label tracks that difference, but whether the label's "hair" is truly hair is unresolved. Either the "grainier/yellower = hair" inference is reversed, or contrast normalisation makes the smoother face look rougher. Orientation results (Gregory's rule, random side out) are unaffected, because they only need the faces told apart consistently. Next: P9-C, without normalisation, in colour, or an external hair/flesh call.
- **P9-C (no contrast normalisation, pre-registered): INCONCLUSIVE.** Only 7/16 leaves could be decided (4 agree, 3 against), and the controls drew 0/8 confident picks. The P9-B reversal does not replicate, so it was probably a normalisation artefact. **Overall: by eye at ~16 px/mm the hair side cannot be named.** The automated face difference (which is all the orientation tests need) stands, but "which face is hair" needs external data (a Beinecke collation, or raking light). Further by-eye runs are not worth doing.

## 7. Wear and handling

**Result: the original "wear" finding is mostly a photography artefact. DOWNGRADED.**

- v1 finding 6 (2006 scans, 152 pages): inner sheets' outer faces cleaner at edges (p = 0.005, corners p = 0.002), opposite to the singulion-exposure prediction; outermost sheets darker overall (9/10, p = 0.02) and at top edge (p = 0.03). This was read as "favours long-lived nested quires".
- Replicated on Yale photos (finding 10): inner sheets edge +0.41 (p = 0.026); outermost top edge −1.09 (p = 0.005). Skin side does **not** explain it (hair minus flesh −0.07, p = 0.66; r = −0.14).
- Split by band (finding 14): outer edge +0.67 (p = 0.001), gutter +1.40 (p < 0.001), bottom +0.16 (p = 0.52), top +0.27 (p = 0.22). Rectos are 2.55 L* brighter at the outer edge than versos on every kind of leaf, and the gap changes with position in quire (r = −0.19) and book (r = −0.27). Removing a linear position trend cuts the effect to 0.85 (p = 0.057). The gutter recto−verso difference flips sign at the quire centre (+1.75, +1.78, −0.86, −0.52 by quarter): the gutter shadow of a bound book. The bottom band, least affected by opening geometry, shows nothing.
- The outermost-sheet top-edge result remains, but those faces are also at extreme positions, so position is not ruled out.
- **Practical rule:** wear from photographs of a bound book needs position-matched controls. Raking-light or flat-lit loose-sheet imaging would be needed.

Related: v1 finding 7, Currier A vs B herbal parchment (22 A vs 7 B sheets): B less yellow (b* 5.6 vs 6.4, p = 0.009; marginal after 8 tests); tracks scribe more than language (hand 1 b* 6.5, hand 2 5.7, hand 3 4.9). No ink or wear difference. 2006 scans only; not re-run on Yale images.

## 8. Illustration continuities across the gutter

**Result: 2 of 5 claimed continuities hold up; 1 is contradicted; 2 cannot discriminate.** (`continuity/CONTINUITY_REPORT.md`; claims from Layfield & Davis ¶6–7, after Pelling 2006)

| Claim | Verdict | Evidence |
|---|---|---|
| 78v\|81r streams | **Confirmed** | Pipe/streams from the 78v pool run to the fold; two streams enter 81r at the same height. Nothing on 78v\|79r or 80v\|81r. `continuity/5_78v_81r.jpg` |
| 33v\|40r blue petals | **Confirmed** | 33v's flower is cut at the fold; 40r's inner edge has isolated petal tips in pen outline with blue fill at the same height. On the binding spread 33v\|34r the transfer is a shapeless smudge (ordinary offset). `2_33v_40r.jpg` |
| 10v\|15r splashed stain | **Contradicted** | Nothing on 10v's gutter at the height of 15r's blob. 14v (the binding neighbour) has brown droplets in mirror position, on top of its paint. The splash happened with 14v facing 15r, i.e. in the current binding. `1_10v_15r.jpg` |
| 58v\|65r green leaf | Real, non-discriminating | 58\|65 is the innermost surviving bifolium of quire 8 (f59–64 lost), so 58v faces 65r now as well. `3_58v_65r.jpg` |
| 76v\|83r nymph's arm | Inconclusive | Co-located marks, nothing visibly crosses the fold. `4_76v_83r.jpg` |

Random-pair baseline (8,366 verso×recto combinations, coincident marks at matching height): pigment, 97% of random pairs score 0; 33v|40r scores 7 (P = 0.018); binding spread 14v|15r scores 6 (P = 0.020), agreeing with the visual finding. Ink: 76v|83r P = 0.011 (co-location, not continuity). The metric cannot see shape continuity; treat it as a coincidence rate, not a test.

**Caveat:** drawing across a flat bifolium is also what happens when a quire is decorated before sewing. The two confirmed cases show those sheets were open with their inner spread exposed at some time, not that they were read as singulions.

## 9. Calibration on known texts (final for the quire 20 shape)

`calibration/CALIBRATION_RESULTS.md`. Known-order texts were cut into 470-word pages and grouped into fake quires of quire 20's shape (6 sheets, 720 orders). The pipeline, the search and the shuffled-page null were the same as in §4b. There were two page models. In **run**, the text flows across page breaks. In **aligned**, every page starts on a new entry. Scrambled runs give the false-positive rate.

| Text | best order = true (run / aligned) | median rank of true / 720 | null p < 0.06 (run / aligned) |
|---|---|---|---|
| Forme of Cury | 50% / 20% | 2 / 2 | 75% / 60% |
| Isidore XII, XVI, XVII | 64% / 58% | 1 / 1 | 91% / 8% |
| Gesta Romanorum | 33% / 75% | 2 / 1 | 33% / 0% |
| Culpeper (alphabetical) | 0% / 0% | 84 / 322 | 0% / 5% |
| Scrambled (all) | 0% | 300–640 | 0–25% |

- The search finds the order when content runs on from sheet to sheet. It is at chance in an alphabetical herbal.
- **The shuffled-page test is a poor judge of order.** On aligned pages Isidore's true order ranks first, yet only 8% of fake quires pass p < 0.06; Gesta passes in 0%. Power runs from 0% to 91% depending on the text.
- **Verdict:** quire 20's p = 0.056 and quire 13's p = 0.52 cannot be read either way. Text-based reorderings stay unconfirmed unless physical evidence backs them.

### 9b. S17: quire 13 shape, longer texts, adjacency test (22 Nov, `calibration/s17/REPORT.md`)
- **Quire 13 shape finished.** Same picture as quire 20: the old test finds topical order (aligned LSA, p < 0.06 in 33–45% of windows for Cury, Isidore, Gesta) but not the alphabetical herbal (Culpeper 10%, scrambled 7%).
- **Longer texts** (Isidore I–XX, Darwin, Burton, Pliny NH II+XXXVII; 13–26 independent quires each) show the old best-minus-median test is **conservative**: false positives 1–3% over 1,656 scrambled windows. The earlier "up to 25%" came from texts with 1–2 quires. Power for aligned topical text is 23–29% (LSA) and 28–38% (tf-idf); run-on text 28–47%. Skip control (sheets 3 apart) 2–3.5%, so it responds to adjacency, not topic.
- **Pre-registered adjacency test A1 (residualised best path, cell-permutation null): FAIL as a usable test.** False positives 1.0% (rule met) but power only 7–9% (LSA) / 13–15% (tf-idf) against the required 50%, and below the old test. The residual search itself ranks the true order 3–4/720 (median), so the order information is there; the significance step loses it. A2 (mutual best pairs) is worse.
- **Voynich, A1 (not calibrated, no weight):** all 8 quires with ≥ 4 sheets p 0.23–0.84; the best quire 20 order under the residual search is again exactly Layfield & Davis's.
- **Reading of the old Voynich p-values with the new rates (post hoc):** quire 20's p = 0.056 is ~10× likelier under a topical sheet sequence than under none (0.29/0.028), but the f116r variant (p 0.14) misses, so this is weak support at most. Quire 13 (p 0.52) is uninformative: ~75% of truly ordered quires also miss. Herbal quires are untestable if entries are unrelated, as in Culpeper. The §9 verdict stands.
- **S17-D split-half stability test (added overnight, pre-registered addendum): FAIL.** Agreement of best orders from two halves of each page: false positives 10.9% (LSA; rule ≤ 10%), power 29–37% (rule ≥ 50%). Similar page pairs stay similar in both halves whether or not they are adjacent. The old best-minus-median test remains the best available (FP ≈ 3%, power ≈ 25–30%).
- **S17-F, text × stain agreement on a stacked order (`calibration/s17f/`): FAIL.** If loose singulions once lay stacked and the text ran on, the facing pairs (Yv of one sheet, Xr of the next) should score high on text and on shared stains together. After removing row, column and binding-distance effects, the correlation between the two is null: pooled R +0.34, p 0.38 (LSA × brightness). tf-idf p 0.21, yellowness p 0.06, and on every setting the matched quires fail to beat mismatched ones. Quire 13 r +0.42 (p 0.08), quire 20 r −0.21. The mismatched-quire control centres on 0, as it should. Power is low (8 quires; 4-sheet quires have only 24 relabelings).
- **S17-G, full-resolution stain maps (`calibration/s17g/`): primary FAIL, one near-miss.** Maps rebuilt from the full-size Yale images on the old grid (G1) and a 2× finer grid (G2). §5a holds: the current nesting has a mean percentile of 0.107 / 0.121 (p < 0.0001), and quires 13 and 20 are still rank 1. S17-F brightness × LSA stays null (p 0.48 / 0.47). Yellowness × LSA is a consistent near-miss across thumbnails, G1 and G2 (p 0.060 / 0.050 / 0.054), with all 8 quires positive on G1 and the matched mean just above the mismatched control. It is not pre-registered as primary and is 1 of 6 settings, so it needs independent replication (S17-H).

### 9c. S6-B: which bands judge the hybrid generator? (22 Nov, `bundle/s6b/REPORT.md`): FAIL
The yardstick was the Voynich FIT half scored against TEST. A band set is valid if FIT passes and no control does. Three sets are valid. Under project bands (P) the hybrid passes on 19/20 seeds (19–22/24). Under page-bootstrap bands (B) it passes on 0/20 (12–17/24), and under bootstrap + FIT–TEST difference (H) also on 0/20 (15–19/24). FIT itself still scores 22–24 under B and H. The stricter bands are therefore not too strict: **the hybrid's 20–22/24 depends on bands about twice as wide as the sample.** Under H it misses S3_sdlen, S8_nearcopy, S10_immrep, E1, E2, edge and nearadj, and keeps R and d1d2. Recommended scoring from now on: H, with P reported alongside. Chunk-level scoring (C) is invalid, because FIT fails it on R/d1d2.

### 9d. S17-E: calibration on Voynich-like text with a planted sheet order (26 Nov, PC `s17e/REPORT.md`, pre-registered)
- Texts: hybrid generator (trial 1594) on quire 20's page shapes, pages written in sequence; `carry` (previous page's words kept as copy sources) sets the page-to-page drift. carry 0 and carry 9 with sheets permuted are the nulls; carry 9 (fitted value) is the primary planted order; 50/150/376 dose response. Plus Timm pages (writing order vs permuted). Same best-minus-median test as calib.py (q20 shape, 500 shuffles). 460 windows / 80 independent quires per hybrid condition.
- LSA p<0.06: null 4.1% (both nulls); carry 9 14.8% (p<0.15: 34.8% vs 14.3%); carry 50 46%; carry 150 88%; carry 376 91%. tf-idf p<0.06: null 8.5-8.7%; carry 9 47%; carry >=50 ~100%. Timm: LSA 6.7% vs 5.9% scrambled, tf-idf 8.1% vs 10.4% (true order median rank 172/720 LSA).
- Pre-registered verdict: LSA (the quire 20 metric) "weak" (power 0.15 < 0.25, LR 3.6; LR 2.4 at p<0.15); Timm "blind"; tf-idf hybrid "discriminates" (LR 5.4). Sanity check passed (carry 376 true order rank 1/720). Voynich-likeness passed (quire 20 hubness LSA 0.46 / tf-idf 0.32 inside both null and carry-9 ranges).
- tf-idf false positives are higher on Voynich-like text (8.5-10%) than on natural language (1-3%).
- Post hoc for quire 20: p 0.056 is ~3.6x likelier under a Voynich-like sequence than none (S17 natural-language estimate ~10x); f116r p 0.14 ~2.4x. tf-idf is more sensitive here (47% vs 15%) and quire 20 shows nothing on tf-idf (p 0.45); quire 20 tf-idf hubness 0.32 is outside the carry >=50 range (<=0.26). So quire 20 fits "no or very weak sequence" at least as well as "true sequence"; a Timm-style sequence would be invisible. Section 9 verdict stands: text-based quire 20 reorderings unconfirmed.
- Caveats: overlapping windows; LSA space per run, not whole-Voynich; carry 9 is fitted to statistics that don't measure page carry-over; Timm pages are ~110 words.

### 9e. S17-I: the Voynich's own page carry-over (26 Nov, cloud, `s17i/REPORT.md`, pre-registered)
- Measure: shared rare-type overlap (count 2..10) of consecutive pages / same-section same-hand pages ≥ 6 apart. Voynich same-leaf r→v: **R 2.53 (CI 1.97–3.13)**; cross-sheet 1.97; within-section shuffle null 1.64 (p 0.0005). Generator (trial 1594): carry 0 1.23, **carry 9 5.74**, carry 50–376 8–11.
- The real carry is between 0 and 9 (≈ 3–6 words by interpolation, an upper bound since topic adds to it). No S17-E level matches; the fitted carry 9 is too strong.
- The shape differs: the Voynich drifts slowly (pages 2–5 apart still 1.7–1.8×) with a small extra bump for adjacent pages; the generator makes a one-page spike with no drift.
- **Quire 20 has no measurable carry:** consecutive R 1.15 (CI 0.91–1.42), shuffle p 0.105, at the carry-0 level. S17-E's 15% power is an overestimate for quire 20; at realistic carry the test is near chance. §9 verdict strengthened: quire 20's text cannot judge its order.

### 9f. C3: genre-sensitive tests rerun on period German herbal/medical texts (26 Nov, cloud, `c3/REPORT.md`, pre-registered): all FAIL
- **Section topic words:** genre-matched sections (Brunschwig waters/remedies/surgery, Breslauer herbal/medicine) give r_p 0.50–0.69, *above* Pliny/Megenberg; new 10th pct 0.47/0.57/0.62 vs Voynich 0.18/0.31/0.27. The genre escape is closed; the Voynich's section words stay spelling-driven.
- **Nomenclator held-out:** 0/5 seeds on Gart, Brunschwig, Breslauer (10–12/24). Held-out R 0.8–1.5 vs Voynich 0.32, so the Dante/Megenberg boundary positive does not generalise.
- **Decipherment LMs:** harness uncalibrated on German OCR at 2,500 iterations. At 10,000 the Voynich beats shuffles and Timm against the *Gart*, but the hybrid generator matches it, and the key collapses to e/i/n junk (`eine nin in iin een`). No reading.
- **Order-test calibration on Gart/Brunschwig:** old test FP 0–4%, LSA power 15–31% (tf-idf 32–53%); A1 weaker. Same as S17; §9 unchanged.

## 10. Published orders scored against every alternative

(Manuscript-wide, `manuscript_wide/t8.out`, `t9.out`; proposals from `page-order-review/proposed_orders.csv`.) Each full order is placed among every arrangement of the same sheets: all nestings and all singulion stacks, every sheet order and orientation (7,680 for quire 13; 92,160 for quire 20). Score = share of arrangements at least as good (0.01 = top 1%, 0.5 = typical). Text is ranked among arrangements of the same kind.

| Proposal | Basis | Text LSA | Text TF-IDF | Stains brightness | Stains yellowness |
|---|---|---|---|---|---|
| Q13 current binding | baseline | 0.54 | 0.88 | 0.057 | 0.019 |
| Q13 Layfield & Davis best | LSA | 0.001 | 0.09 | 0.79 | 0.73 |
| Q13 Layfield & Davis 2nd | LSA + initial | 0.001 | 0.002 | 0.15 | 0.71 |
| Q13 mgvtheus | LSA rerun | 0.014 | 0.03 | 0.32 | 0.17 |
| Q13 Pelling 2006 | illustration, paint | 0.018 | 0.22 | 0.17 | 0.88 |
| Q13 Lucian | codicology | 0.014 | 0.27 | 0.15 | 0.26 |
| Q13 Guidoni | none stated | 0.13 | 0.16 | 0.35 | 0.98 |
| Q13 Stolfi singulion | shared words | 0.27 | 0.17 | 0.46 | 0.77 |
| Q13 Stolfi nested | shared words | 0.34 | 0.88 | 0.30 | 0.27 |
| Q20 current binding | baseline | 0.22 | 0.27 | rank 1 of 92,160 | rank 1 of 92,160 |
| Q20 Layfield & Davis (= mgvtheus) | LSA + initial | 0.000 | 0.002 | 0.56 | 0.33 |

- Text scores are circular for text-derived orders (chosen by maximising that score), and section 4 shows top ranks of that size come from random page assignments too. Pelling's and Lucian's good LSA ranks come from putting 78|81 at the centre, making the strongly similar 78v|81r a facing pair.
- On stains, every proposal is typical or worse (0.15–0.98); the current binding is top 6% for quire 13 and first for quire 20.
- Groupings, exact permutation tests: Zandbergen's quire-20 vocabulary split (text p = 0.10, stains 0.6–0.7), Pelling's vellum-colour split (text p = 0.53, stains 0.20), Claston's two-topic quire-13 split (text p = 0.10, stains 0.10–0.50). All fail, but the smallest possible p is ~0.1, so these tests have little power.
- Note: in the 7,680-arrangement space the quire 13 current binding ranks 436 (P80) / 143 (B) on stains, versus 1 of 120 in the nestings-only space of section 5a. The bigger space adds orientations and singulion stacks; the binding is still top 6%.

**Literature context** (review doc): only quires 13 and 20 have full published orders; elsewhere there are constraints and groupings. None of the text-based orders was tested against a random baseline by its author. Per Zandbergen, the disordering predates both the 15th-century quire marks and the foliation, so neither numbering can recover a planned order. CSV caveats: Stolfi's orders were transcribed from a summary (verify against Note 052); Q8-PEL includes lost leaves f59–64 (drop before scoring); Q13-LUC subquire order is assumed.

---

## 11. Contradictions and tensions between threads

1. **"Current binding is not the writing order" (v1 finding 2) is overstated.** v1 inferred this from facing pages being at the random baseline. That shows the sheet, not the spread, was the writing unit; it does not show the binding order is wrong. The manuscript-wide thread finds the binding order unremarkable on text (rank 1–22 of 24) and best on stains. Use the later reading: text is silent on the binding order.
2. **Wear finding 6 vs finding 14.** v1 used finding 6 as evidence for long-lived nested quires; finding 14 shows the inner-sheet effect is mostly imaging geometry. The literature review's closing open question still cites finding 6 as live. Treat finding 6 as downgraded; only the outermost top-edge result survives, with a position caveat.
3. **10v|15r.** The literature (Layfield & Davis, Pelling) lists it as a gutter continuity and a "herbal pair that faced at a centre fold". The continuity thread finds the splash belongs to the current binding spread 14v|15r, and the automated pigment baseline agrees (14v|15r P = 0.020, 10v|15r score 0). The manuscript-wide offset detector ranked 10v|15r top among inner conjoint pairs (+0.49), but that group as a whole is at baseline (p = 0.76). Weight of evidence: not a continuity.
4. **Quire 20 LSA p-value differs by pipeline:** 0.056 (exact L&D rebuild, f116v) / 0.14 (f116r) in the mis-binding thread, 0.12 in the manuscript-wide T4 run. The difference is the transcription handling and document set (722 vs 719 docs) and the f116 page choice. All are borderline-to-null; none survives the calibration caveat.
5. **Skin-side counts differ** (17/30, 22/41, 18/37 hair-out; quire 20's last sheet "?" vs "O"). Different classifiers and thresholds. All three agree orientation is random and Gregory's rule fails.
6. **Within-sheet order strength:** v1 "suggestive only" (p ≈ 0.06) vs manuscript-wide LSA p = 0.0008. Same direction; the later run has more sheets and LSA. Jaccard still disagrees on the last two pages.
7. **Physical evidence points two ways.** Stains, offsets and show-through all fit the current nesting; the two confirmed illustration continuities (78v|81r, 33v|40r) show those sheets were once open with the inner spread exposed. Not a contradiction if decoration happened on flat sheets before nesting, but it is the one positive physical sign of a different past arrangement.
8. **Literature-internal:** ~~Pelling's quire-20 paint transfers contradict Dulov's wormholes.~~ Resolved 22 Nov (§5d): both transfers and the wormhole gradient fit the current stack. Zandbergen's vocabulary split and Pelling's vellum-colour split of quire 20 disagree with each other. Neither split passes our tests.
9. **Quire 13 stain rank** reads as 1/120 (nestings only) or 143–436/7,680 (all arrangements). Both are stated above; they are not in conflict but are easy to quote out of context.

## 12. Open questions and next steps

1. Calibration: the quire 20 shape is done (§9). Still open: finish the quire 13 shape, and design a test aimed at adjacency itself rather than best-minus-median. Decipherment next steps are in `plan/DECIPHERMENT_PLAN.md`.
2. **Physical constraints at full resolution:** DONE 22 Nov (§5d). All fit the current stack, and 84v|78r and the Q9 cuts were not seen (no source found). Left open: measure the f114 edge flaw precisely (P7-F).
3. **Independent image set:** rerun the stain test on the 2006 Beinecke scans to rule out Yale photo-order effects; confirm the quire-boundary drop by eye at a few boundaries.
4. **Beinecke sources:** conservation notes (Zyats 2016), UV images, any collation with hair/flesh notes; sewing holes are not visible in these photos.
5. **Verify Stolfi's Note 052 tables** directly.
6. **Timm's question:** was any "original order" ever a reading order rather than a production order? Everything here (same-sheet similarity, within-sheet Xr→Xv→Yr→Yv, random skin side, flat-sheet continuities) fits a production order of folded sheets as well as a reading order of singulions.
7. Wear questions need raking-light or flat-lit imaging; do not reuse photograph-based wear without position-matched controls.

## 13. Language, generator and decipherment tests (21 Nov, 04:20–08:40 UTC)

All of these use held-out sheets where stated (FIT/TEST split `timm_generator/split.json`) and pre-registered rules.

- **Sheets as units** (`sheets_as_units/`). Hand and section each carry vocabulary independently (p ≤ 0.008). Language adds nothing once hand is known. Sheet-to-sheet affinities beyond metadata replicate across split halves (r +0.37, p = 0.0002), but they do not follow binding position once section is controlled (p = 0.14).
- **Plant drawings** (`plant_drawings/`). A six-feature drawing code does not explain those affinities (split-half r 0.341 → 0.338). Drawing similarity does not predict text similarity (p = 0.46). With one coder and coarse features, an effect of about r ≤ 0.1 remains possible.
- **Labels** (`labels/`, `grammar_labels/`). Labels are mostly one-offs: they are reused 2–4× *less* than length-matched text words (p ≤ 0.008). They do not reappear in their own page's text (E_L 0.93, p = 0.79). 0/126 pharma labels match herbal first words. Weak leads: jar and fragment labels end differently (p = 0.008, one of about 18 tests). **Labels are not captions and cannot serve as cribs.**
- **Language test** (`language_test/`). It is **not like any plain language tested**. Character predictability h2 is 2.07 bits (languages 3.06–3.33), and word-order information is 0.07 (languages 0.19–0.86). Near-copies (1.48×) and exact repeats (1.97×) are above every language. Word length, Zipf, burstiness and compression all fall inside the language range. Compression separates the text from noise (z 10–14), but not from language or generated text. EVA glyph splits may lower h2 somewhat.
- **Word families** (`word_families/`). Pharma has specialised vocabulary that recurs in the herbal text and replicates on a held-out pharma sheet (×3.0, p = 0.002). Whole words do the same, so this is **not evidence of word-building**. Rugg-style text is ruled out for this structure (R ≈ 0). Family co-occurrence does not beat the Timm generator.
- **Fitted Timm generator** (`timm_generator/`, Timm's own Java code, fitted on FIT sheets). The "roots generalise better than words" lead does **not replicate** (G = −0.005). The wider fit matches word-length spread and, at a cost, vocabulary. **Line position separates the real text from the generator.** The first glyph of a line-initial word shifts by 0.213 JS bits against the generator's 0.047–0.060 (z 6.0–6.6). The generator shortens line-final words; the Voynich does not. Word order stays stronger than every generator variant (0.112 vs 0.085–0.093).
- **Grammar-like dependence** (`grammar_labels/`). Ending-to-ending dependence is real (z 11–15) and beats fitted Timm on different-ending pairs (0.006 vs ≤ 0.0035). It is about a third of the weakest language (0.018), so it **fails** the grammar-like rule. The ending-by-line-position effect is reproduced by Timm.
- **Decipherment harness** (`decipherment_harness/`). The harness recovers a true simple-substitution key from about 2,300 words (95–100% correct). **Bax 2014 fails** in all 5 languages. **Cheshire 2019 fails**, even when given its most favourable values: fitted Timm text does as well, and the one Latin "pass" is not robust across seeds. The best key fitted from scratch makes the Voynich no more Latin- or Italian-like than glyph-shuffled text (M1 3.99 vs 3.82). Only context-free substitution was tested. Both keys are our reconstructions.

- **Cribs and keys** (`cribs/REPORT.md`). Five candidate "Rosetta stones" tested; **none holds on held-out text.** Zodiac nymph labels are not numerals (247 forms in 299, 1 same-position match). A weak same-position similarity across signs (p 0.027) is not significant once 4 reading orders are allowed for (p 0.11). The f57v ring is not the text's alphabet: it omits e, a, i, ch and n (37% of glyphs), and as a key it scores M1 6.7, p 0.07. Plant names (92 pages, pre-1960 IDs) are not spelled by any fitted key in the first word or first line, p 0.71 with sheet-grouped cross-validation. **An apparent pass (p 0.02) was leakage from same-sheet and same-name pages: group CV folds by sheet and by target in every crib test.** f116v gives 3 tokens and an ambiguous glyph, so it is not a usable crib. Period ciphers (homophones and nulls) are covered by the harness fit, which failed. Nomenclators are untested.

**Net position.** The text is structured: it has a strong line-start rule, sheet-level writing units, section- and hand-specific vocabulary, and some dependence between neighbours. It is not plain language and not a simple cipher of Latin or Romance. Timm's published generator does not fully explain it either. A meaningful reading, if there is one, most likely sits below the word: verbose or homophonic units plus a line convention. Meaningless human gibberish is untested and is the key control. See `plan/DECIPHERMENT_PLAN.md`.


### 13b. Plan steps 1–4 (21 Nov, 08:55–09:19 UTC; `plan/DECIPHERMENT_PLAN.md`)
- **Step 1, human gibberish** (`gibberish/`; Gaskell & Bowern 2022 data). At 300 words, gibberish matches the Voynich's weak word order and weak ending dependence, which meaningful texts fail (59% vs 32% "Voynich-like", p = 0.007). E1 has no power at that size. A powered pooled test (10k words) shows the gibberish line-start first-glyph shift is +0.004, against +0.18 to +0.24 in the Voynich: **gibberish lacks the line-start rule**. Weak word order is therefore *not* evidence of a cipher.
- **Step 2, line-start rule** (`line_start/`). 45% of lines start with p, t, y, s or f words (p 17×, t 6×, y 3.9× their mid-line rates). Stripping that glyph removes 84% of E1, but the stripped forms are ordinary words at the same rate as for mid-line words, so an "added marker" can't be told from a word-class choice (pre-registered test fails). Line-initial words are also longer (+0.57 glyphs), which gibberish shows too.
- **Step 3, word-level codes** (`word_codes/`). All fail:
  - Latin/German abbreviation: word order unchanged, and h2 goes *up*.
  - Lingua Ignota-style invented words, and one-to-one nomenclators or relexified constructed languages: word order exactly unchanged (0.19–0.61).
  - Homophonic word codes: match word order but break Zipf and burstiness.
  - None of them yields near-copies or immediate repeats.
- **Step 3b, ingredient-list notation** (`ingredient_list/`). Fails. There are no closed quantity slots, and paragraph-initial words are *more* unique than other line-initial words (ratio 0.23–0.68). Leads: line-final words are rare types in S, P and B (0.45–0.64× shuffle; Timm 0.9+), and every paragraph opens with a fresh gallows word.
- **Step 4, Naibbe cipher** (`naibbe_test/`; Greshko's published Latin ciphertext). It matches 5/14 held-out statistics. It has no burstiness, near-copies or repeats, and too little word order. **Fitted Timm plus the step-2 line rule matches 11–12/14, the best fit so far.** It still misses word order (~30% weak), line-final glyphs (overshoot) and the full size of E1 (under half). Per the decision gates, the decoder (step 5) was not run.

- **Step 6, Currier A vs B as one system respelled** (`ab_alignment/`). No evidence. Rewrite rules close 22% of the herbal A→B vocabulary gap on TEST, about the same as rules learned against glyph-shuffled B (19%) and below Latin→Italian (27%). The method failed its own calibration (medieval-spelled Latin 1%, Latin→English 39%), so this null carries little weight.
- **Own copy-and-vary generator** (`own_generator/`; pair copying, line-start class, no trimming; fitted on FIT). Fails: 5–6/14 TEST statistics, against 11–12 for Timm + line rule. Pair copying did not raise word order (0.028 vs 0.070). The Voynich's word order remains unexplained by every model.

- **Word order lives at word boundaries** (`word_order/`, exploratory). The last glyph of a word predicts the next word's first glyph by 0.19 bits above shuffle (0.16 with 3+ glyph words). That is natural-language strength (Latin 0.03 … German herbarium 0.18), but **about 20× above fitted Timm (0.007–0.010), Naibbe (0.002) and gibberish (0.015)**. The boundary/within-word coupling ratio is 0.16 (languages 0.05–0.20; randomly respaced text 1.1), so spaces are real boundaries. Ending agreement is near zero (0.0075 vs 0.05–0.09). Re-ordering Timm's words to add the rule after the fact fails (11–12/14). This agrees with Rozanova & Temerev 2026. It is the strongest remaining evidence for language-like structure. Across 55 real and constructed languages (Gaskell & Bowern set), sandhi languages match the boundary strength (Sanskrit 0.20–0.25, Tagalog 0.19–0.23), but every text also has much stronger ending agreement and word order. **No language, cipher or generator tested combines strong boundary coupling with near-zero agreement.** Real abbreviated-Latin manuscripts also fail (boundary 0.05, word order 0.32). Adding a boundary rule to Timm text, as respelling of word openings while writing, raises boundary coupling to 0.17 but collapses word order (0.012) and fits worse (8–11/14). The mechanism remains open.

- **Generators v2–v4** (`own_generator/`). Choosing which earlier word to copy by how it joins the previous word **matches the Voynich word order for the first time (0.069–0.072 vs 0.070)**, at 9/14 overall. Adding a line-end rule (v3) reaches 12/14, the same ceiling as Timm + line rule. A larger search (v4, 180 settings) did not beat it: word order and local repeats trade off.
- **Not sandhi** (`sandhi/`). With the root held fixed, a word's final glyph does not depend on the next word (excess 0.005 vs Sanskrit 0.23–0.34, other languages 0.04–0.12). The boundary coupling comes from which word follows, i.e. word choice, which a generator rule can supply.

- **Line-start rule has two parts** (`line_start/` addendum). Paragraph starts take a gallows "capital" (84%: p 46%, t 23%, k 11%). Lines inside a paragraph prefer y-, s- and d- words (46% vs 12% mid-line) and avoid ch- (4% vs 19%). The second part carries most of E1 and is not a capital habit.
- **Copy-and-vary generator plateau** (`own_generator/` v5). With less noisy selection, the best FIT setting scores only 6–8/14 on TEST, so v3's 12/14 was partly luck. Fitted Timm + line rule (11–12/14 on every seed) stays the most stable model. No model reproduces word order, repeats and line-end behaviour together.
- **Cribs thread** (`cribs/REPORT.md`): zodiac labels as numbers, the f57v ring alphabet, plant names, and the f116v marginalia all fail; the plant-name pass was leakage from same-sheet vocabulary.

- **Robustness** (`word_order/` addendum 4, `transcriptions/`). At certain spaces only, the boundary coupling is still 0.159. In three independent transliterations (ZL3b-n, IT2a-n Takahashi-based, RF1b-e), boundary coupling is 0.16–0.18, E1 0.20–0.21, gallows start 80–86% of paragraphs, and y/s/d start 42–48% of other lines (12–13% mid-line). None of the main structural findings depends on one transcriber.
- **Capitals by image** (`capitals/`). With per-word boxes (voynichese.com via the Rozanova archive, 95 pages), paragraph-initial p-words are the same height and width as p-words inside lines (1.50 vs 1.50, p = 0.69); t is +12% (p = 0.001). The paragraph gallows are a *choice* of glyph, not an enlarged capital.

- **Full self-citation generator with the three scribal rules** (`sc_generator/`). Fails (5–9/14). The rules fix line ends (E2 matched for the first time) and raise E1, but our home-made copying is far too repetitive. The fair test is Timm's jar with these rules added, which needs his code installed and run.

- **Glyph variants (allographs)** (`allographs/`; v101 aligned with EVA). The variant of p (Claston's g vs j) is decided by line and paragraph position: g is 92% at line start vs 50% elsewhere. Variants of d and f follow neighbouring glyphs and position in the word. No variant depends on word identity beyond the page, so there is **no sign of a hidden variant layer**. The paragraph-initial p is a positional capital *form*, not a larger glyph.

- **Timm's own generator + the four rules** (`timm_rules/`, run by the Timm thread; patched Java source, rules from FIT). **Best model yet: 10–12/14 on TEST** (5 seeds; plain Timm 7–11). It matches E1, E3 and vocabulary on every seed and word order on 3/5. It misses line-end glyphs (E2 0.15–0.17 vs 0.087; trimming over-marks, no trimming under-marks) and word-length spread (S3 1.56–1.63 vs 1.78). It falls short of the 13/14 bar. A follow-up (no trimming, separate line-end weight γ_end 4, combine_split 60) fixes E2 and S3 on 4/5 seeds, but vocabulary, local repeats and burstiness break: 9–13/14 (1 of 5 seeds at 13). v1 remains the more stable model (`timm_rules/REPORT2.md`).

- **Joint fit and line-end rule** (`timm_rules/REPORT3.md`, `REPORT_ENDRULE.md`). Across about 170 settings, Timm + rules tops out at about 12/14. Adding a line-end ending rule (q fitted on FIT) gives 13–14/14 on TEST for one setting (exploratory). It then **fails a pre-registered confirmation on 5 statistics never used for fitting** (0/5 seeds). Boundary coupling is half the Voynich value or right, depending on setting. **Ending agreement is 3–6× too high in every setting (0.023–0.043 vs 0.007).** Copy-and-vary explains most of the surface, not the whole text.

- **Where the ending misfit comes from** (`ending_agreement/`, exploratory, plus one pre-registered test). Copy-and-vary text has twice the Voynich rate of adjacent near-copies (7.5–8% vs 4.5%), and 75% of them add or drop a first glyph (Voynich 23–25%). Their endings are almost always kept (93–95% vs 71–77%). Unrelated neighbours also share endings above chance (Voynich: exactly at chance). Pre-registered check, is each line a unit for endings? **No.** A line break at the same word distance changes nothing (LB ≈ 0, `ending_agreement/lb.out`).
- **The boundary link is glyph-driven, not word-driven** (`boundary_source/`, **pre-registered, PASS**). Beyond the two touching glyphs, the words add little across the space. R = (A+B)/edge is 0.32–0.35 in the Voynich. Every language is 0.68 or more: sandhi Sanskrit 0.68–0.96, Tagalog 2.0, Latin/Italian/German/Arabic 2.8–5.6, Esperanto/Toki Pona/Lojban 3.7–9.2. Timm + rules is 0.42. **This counts against a language with word grammar, natural or constructed, and for a glyph-level writing procedure.** Follow-ups:
  - A pure one-glyph chain model gets edge and ending agreement right (the first model to fit agreement), but only a quarter of word order. FAIL (pre-registered).
  - A same-page resample that keeps first and last glyphs keeps two-thirds of word order. The rest (0.03–0.04 bits) is not split words.

- **Window-chain generators** (`window_chain/`, pre-registered, 3 versions, **all FAIL**). The next word's opening is chosen by the previous word's ending, then the word is copied from recent text. This gets 4/5 held-out statistics on every seed (boundary, endings, line start, page gallows), but only 7–10/14 surface statistics, and word order is 0.01–0.06 vs 0.111. **Chain models and Timm-style copying fail in opposite directions.** No mechanism tested gives strong boundary + rich near-copying + moderate word order + no ending agreement together. Family closed.

- **Timm + rules with copied endings re-drawn** (`timm_rules/REPORT_REDRAW.md`). It passes its own pre-registered test with setting #1: 12–13/14, 3–4/4 held-out, ending agreement 0.008–0.013. It then **fails a second pre-registered confirmation on 5 new statistics** (2/5 on every seed). Copying leaves an ending alternation (d1−d2 +0.07 vs −0.01), too many first-glyph edits in near-copies (0.76 vs 0.58), and too-weak first-glyph runs between neighbours (0.02–0.04 vs **0.052**). Not an identification.

- **Glyph n-gram calibration** (`glyph_ngram/`, pre-registered, diagnostic). A model with 3–5 glyphs of memory, trained on FIT, matches 15–17/24 statistics on TEST. That includes the boundary link, ending agreement and line-start rules. It always misses burstiness, near-copies, local repeats and line end, which need page-level copying. Below the pre-set 20/24, so no claim that the structure is purely short-range. At order 6 it memorises word pairs and R jumps to 1.0 (language-like), unlike the Voynich.

- **Glyph model plus word cache** (`cache_ngram/`, pre-registered, **FAIL**). 15–18/24 and 6–8/10 never-fitted statistics. It misses burstiness (0.21–0.27 vs 0.47), near-copies, Zipf and line end, and R turns word-driven (0.57–0.70). Even-rate copying does not give the Voynich's clumped repetition.

- **Small neural model of the text** (`neural_lm/`, pre-registered, LSTM, two-fold).
  - 1.97 bits/glyph on held-out pages. About 0.08 bits come from context beyond a word or two (Timm text 0.06, Latin 0.005), which fits page-level repetition.
  - A model trained on Timm + rules text scores the real text at 2.90 bits/glyph, so the generator is about 0.9 bits/glyph away in detail.
  - Surprising lines rediscover known anomalies (the f57v ring sequence, "roseer", ring texts, f116r) and are concentrated in Currier A herbal pages.
  - **Page vectors predict illustration type across sheets beyond hand and dialect (0.715 vs null 0.62, p < 0.002; PASS).** But bag-of-words does the same (0.710), so the link is section vocabulary, not anything deeper.

- **Target profile** (`target_profile/TARGET_PROFILE.md`, `score.py`). 24 statistics with Voynich bands and a scorer for any generated text. The best models reach 15–18/24; none reaches 20. The hard part is clumped near-copying without ending alternation, together with first-glyph runs and a glyph-driven boundary.

- **Cache models v2 and v3** (`cache_ngram/`, pre-registered, FAIL). Bursty copying is worse (14–16/24). Copying from the current page only is the **best on the full profile so far: 16–18/24**, but still misses Zipf, word order, near-copies, line end, R (0.54–0.70) and first-glyph runs (0.035–0.039 vs 0.052). Page-local vocabulary is necessary but not enough.

- **Opening-class transitions and an onset-conditioned cache** (`first_runs/`, exploratory; `onset_cache/`, pre-registered **FAIL**). Neighbours' first glyphs are linked by specific class transitions, not runs: sh-→q- ×2.0 vs ch-→q- ×1.0, ch-↔sh- avoided (×0.63), a-/s-→a- ×2.7–3.2. A page cache that draws the next opening from the previous opening and ending overshoots that link (0.07–0.08 vs 0.052) and scores 15–17/24. **Generator work pauses at a plateau of 15–18/24 across all families.**

- **Step 5, regional languages in real manuscript lines** (`regional/`, pre-registered). Sources: 14th-c. Middle High German (Tauler, Freising law book, etc., ReM), Old Occitan, medieval Italian and abbreviated Latin (HTRomance), all diplomatic with real lines. **No text has the Voynich boundary profile:** R is 1.9–6.4, vs 0.32, and MHG is furthest. **Real scribal lines show weak line effects** (E1 0.003–0.055, E2 0.010–0.061, vs Voynich 0.19–0.21 and 0.08–0.09). So the Voynich line conventions are part of text production, not layout habit. Addendum: the Old Occitan *Breviari d'Amor*, Megenberg's MHG *Buch der Natur* and the Venetian *Herbolario volgare* (1540) give R 3.1–6.8. None matches.
  - **Comparison corpus, 25 Nov** (`regional/comparison/`, README there). It has 14 more public-domain texts, about 960k tokens, from archive.org: the Venetian *Libro di cucina* (ms. late 15th c.), two Tuscan 14th-c. cookbooks, the *Ricettario galante*, the Neapolitan *Bagni di Pozzuoli* (bath verse), a Bolognese health regimen, Benzi 1481, the *Fasciculo de medicina* 1522 and Manfredi's *Perché* 1512; and in German, Pfeiffer's Bavarian *Arzneibücher*, the Silesian *Breslauer Arzneibuch* (includes bathing), Vintler 1411 (Tyrolean), the *Gart der Gesundheit* (Ulm 1487) and Brunschwig's *Distillierbuch* 1532. They have print lines, not manuscript lines. **Boundary screen: none matches** (R 3.2–7.4 vs 0.32). Vernacular recipe books reach Voynich edge (0.10–0.21) only through repeated formulae: lastlast is 12–22× and word200 6–12× the Voynich values, so the coupling is word-driven, as in S7.

- **Decoding the copying choices** (`choice_decode/`, pre-registered with one documented fix). The 26 choice symbols (which earlier word was copied, what changed), mapped to letters on FIT and scored on TEST, decode **no better than shuffled** in Latin, MHG, Italian or Occitan, and no better than Timm's random choices. The method's positive calibration (homophonic Latin) passes clearly. **No letter-level message in the copying choices.**

- **Boundary rule, A vs B** (`ab_boundary/`, exploratory). The last→first lift table correlates 0.79 between Currier A and B, against 0.95–0.97 split-half within each. So it is the same kind of rule with different settings (e.g. l→k 0.58 vs 2.82). Hands 2 and 3 (B) share one table (0.945), and hand 1 (A) is furthest from the rest. Vocabulary differences are not separated out.

- **Step 7 / Hypothesis C, syllable-sized units** (`syllables/`, pre-registered). With spaces removed, a BPE inventory of about 100 units predicts held-out Voynich text best, and no language peaks in 50–150 (languages peak at 600–1200). So the rule passes, **but Timm's syllable-free text also peaks at 100**, so this is not evidence of syllables. The units almost never cross real spaces (4.8% of spaces inside a unit, vs 20% in Latin, Italian and Occitan, and 13% in Timm). **Not supported:** the Voynich is built from about 100 word-internal chunks, and its spaces are real.

- **Abbreviation, Lingua Ignota swap and homophonic/verbose ciphers on the boundary test** (`codes_boundary/`, pre-registered; 7 models × 4 plaintexts including 14th-c. MHG, plus Naibbe). **All fail**, at 4–10/24 each. Every substitution, homophonic and verbose cipher (Naibbe included) has a boundary link of about 0 against the Voynich's 0.19. Abbreviation keeps the host's ending agreement (0.04–0.12) and word order. **With this, every hypothesis in the plan has been tested; none fits.**

- **Slot generator** (`slot_gen/`, pre-registered, **FAIL**, 14–16/24). Each word is built as onset (chosen by the previous ending) + body (copied from the page) + ending (chosen independently). It overshoots the other way: R ≈ 0 (no word-level part, vs 0.32), word order 0.04–0.05, first-glyph link too strong (0.07), and near-copies differ at the ending rather than the first glyph. The Voynich sits between pure mechanisms.

- **Historical and contextual items H1–H8** (`historical/REPORT.md`; H1a, H3 and H6 pre-registered). **No historical anchor works.** (1) The C1 zodiac positional lead **does not replicate**: p 0.10–0.12 in RF1b-e (0.02–0.05 in ZL3b-n and IT2a-n). The pre-set rule needed both, so it fails. Al-Biruni says no two books agree on the degree tables, and clean tables weren't reachable. (2) **Genre-matched Latin fails**: Macer Floridus, *Circa instans*, Trotula 1544, *De balneis* 1553 and *Herbarius* 1485 have R 2.4–5.5 (Voynich 0.32). (3) **Period ciphers fail** (Fontana-type substitution, Mantua-type vowel homophones, nulls, chancery nomenclator, applied to Macer). Only the nomenclator lifts edge to about 0.19, and it pushes lastlast about 20× too high (0.15–0.19 vs 0.008). (4) **Stolfi Note 052 checked against the original**: the bifolio order EDABC is confirmed. The CSV leaf order had f83 and f84 swapped, and this is now fixed. (5) H7 and H8 are context only (see report). Access: archive.org text is reachable from the cloud via `/stream/` (`historical/code/iafetch.sh`).

- **Cheap meaning tests S7, S8, S9, S10, S11, S15, S18 and charms** (`meaning_tests/REPORT.md`, pre-registered with addenda A–C, 21 Nov 23:00–23:40 UTC).
  - **Formulaic Latin (psalter, litanies, hymns, rosary, Apicius, Cato, Forme of Cury) and charm texts (Marcellus; Ars notoria voces) FAIL.** R is 1.0–12 against 0.32. Repetition makes the boundary link more word-level (lastlast 25–120× the Voynich value).
  - **S7-G, PGM voces magicae (22 Nov, `meaning_tests/s7g/`): FAIL.** No Unicode Greek PGM is reachable, so the voces were extracted from Betz's *Greek Magical Papyri in Translation*, which prints every vox in capital Latin transliteration: 7,977 tokens, 1,498 formula runs (17× the *Ars notoria* set). Score 2/24, edge 0.015 (Voynich 0.19), lastlast 0.049 (7×), R 6.7 (vs 0.32); orderMI 0.21 (vs 0.07) because voces come in fixed formulae. Shuffled control fails the trio as required. Heim's charms not run (OCR garbles the Greek; Latin charms inseparable from commentary). Every charm corpus tried now fails in the same direction: whole-word repetition, not a glyph-level boundary link.
  - **Anagrammed Latin and Hebrew FAIL** (R 6–12, ≤ 7/24).
  - **Layout counts (S9) and dittography (S10) FAIL.** S10 has no line-start restarts.
  - **S11 drift is uninformative.** Timm passes the same rule. The Voynich glyph drift (d, q, t fall and l rises down a paragraph) is real but not yet calibrated.
  - **Numerals S18a FAIL** (position NMI 0.30 vs numerals 0.004). S18b label prefix runs give a weak pass that copying explains.
  - **New positive (S8): a vertical line-start rule.** The first glyph of a line depends on the first glyph of the line above, and on nothing at the second-word or line-final positions. It avoids repeating that glyph (7% vs 14% by chance) and follows specific transitions (q→ch ×3.4, o→q ×2.0, ch→ch ×0). The effect is lag-1 only. It holds in ZL3b-n, IT2a-n and RF1b-e and in Currier A and B. Timm shows a third of it, with no repeat avoidance. An acrostic would produce this, but so would a procedural line-start rule. It has not been decoded.
  - **S8 follow-ups (22 Nov).** **S8-D decode FAIL**: a FIT-fitted key on TEST beats shuffled lines in Latin, Italian and MHG but not an avoid-repeat-only rule, and loses to a first-order line-start chain (z −2.6 to −4.7). So the rule is pairwise and procedural, not an acrostic. **S8-G**: Timm + rules and the hybrid lack the rule (same-initial 0.11–0.20 vs 0.10, excess ≈ 0). A one-table post-process reproduces it at no cost to the profile (17–22/24) but overshoots the excess (0.10–0.18 vs 0.06); 1 of 6 generators passes, so FAIL as pre-registered. Proposed new profile statistic: line-to-line initial same-rate and differing-pair excess.

- **H5: Parisel's per-folio cho/che switch and Timm's single-hand continuum** (`historical/REPORT.md`, pre-registered). The switch **replicates** in ZL3b-n, IT2a-n and RF1b-e (ΔAIC 2,518–2,609, shuffled ≤ 10, held-out 99–100%, σ agreement 98–99%). It matches Currier language on 172/184 folios, and 10 pharma or late A folios sit on the B side. But a pure two-state switch is 540–580 AIC worse than **two broad overlapping clusters** (beta-binomial mixture), and the histogram dips without a gap. So it is bimodal drift, neither a boolean switch nor a smooth continuum. Timm's paper argues that Davis's five scribes are Currier A/B plus label pages relabelled. That is literature only; no image test was run here.

- **Section topic words** (`word_identity/REPORT_TOPIC.md`, pre-registered, **FAIL** in all 3 contrasts). Section words replicate on held-out sheets (ρ 0.56–0.58), but their section preference is predicted by the *other* words' spelling (leave-word-out glyph model ρ_glyph 0.53–0.65). In size-matched Pliny and Megenberg sections it is 0.03–0.46, and in a section glyph 4-gram + cache generator 0.55–0.66. What is left over beyond spelling (r_p 0.18 / 0.31 / 0.27) is below the languages (0.24–0.63) and no higher than a one-glyph-memory generator (0.10–0.27, exploratory). The most frequent words are the most section-specific (core C 2.6 in balneo vs herbal B; languages ≤ 1.1), so there is no shared function-word core. **Section vocabularies behave like section spelling regimes, not topic words.** Candidate lists (e.g. balneo qokain, qokal, qol, ol; herbal A cthy, chy, shol) are recorded there as candidates only. Timm + rules has almost no section vocabulary at all.
- **Systematic nomenclator** (`word_identity/REPORT_NOMEN.md`, pre-registered, **FAIL**, 10–12/24 on held-out plaintext). The first glyph codes a fitted left-context class, the last glyph a right-context class, and the code words are real Voynich words plus homophones. **New positive:** on held-out Italian and MHG it reproduces the boundary signature together: edge 0.16–0.17, lastlast 0.007–0.011, R 0.16–0.30 (Voynich 0.19 / 0.007 / 0.32). No earlier model managed all three. Latin fails held-out (edge 0.01) because its held-out books have a different vocabulary. It still misses burstiness, near-copies, repeats, h2 and the line rules, and homophones push word order to 0.02. **So the glyph-driven boundary no longer rules out a word code:** it rules out natural designs, but a codebook built around what may follow each word would fit.

- **H1b, zodiac labels vs Lilly's degree qualities** (`historical/`, pre-registered; table from Lilly 1647 p. 116 via skyscript). **FAIL.** Same-gender labels are a little more alike in ZL3b-n only (p 0.011; IT2a-n 0.077, RF1b-e 0.047). Luminosity and special degrees show nothing. The best exploratory alignment does not survive an adjacency-preserving null in two of three transcriptions. **H2 substitute:** the Italian *Tesoro de poveri* (1494/1500) has R 3.5–3.7 and lastlast 15× the Voynich, no match. The Paduan *Serapiom* is not available online.

- **Codebook + page copying (D3c) and codebook recovery** (`word_identity/REPORT_D3C.md`, pre-registered, **FAIL**). Adding decodable copying to the systematic codebook gives 8–13/24 on held-out text (Timm + rules 16–19; shuffled Voynich 11). With unique, decodable code words the vocabulary is wrong: 2,700 types vs 1,732 per 5k tokens, h2 2.9 vs 2.07, Zipf −0.2, word order ≈ 0.01. The pre-registered decoder failed its calibration (it collapses words onto "other"). An exploratory one-to-one decoder **recovers a 1:1 whole-word code from ciphertext alone** (Italian 62%, MHG 34% of frequent-word tokens; gain over shuffled 0.47–0.60), but not a homophonic one (≈ 0). **On the Voynich it finds nothing** (gain −0.04/−0.05, below Timm's −0.02…+0.02), so the Voynich is not a 1:1 word code of Italian or MHG.

- **Structure tests S12, S13, S14, S11-C** (`structure2/REPORT.md`, pre-registered, 22 Nov 06:50–08:30 UTC, cloud).
  - **S12 recipes ↔ astro link: FAIL.** With sheet-grouped nulls, recipe words are no more common in astro text than in random background sheets (p 0.67 against Currier-B sheets, 0.20 against all), and astro words are not enriched in recipes either (p 0.18 / 0.13). The method has power: Montemurro & Zanette's top link, pharma → herbal, replicates (p 0.002). Astro pages sit between A and B.
  - **S13 hand groupings: nothing needs five scribes.** The boundary rule follows Currier A/B (p 0.006) and does not differ between hands 2, 3 and 5 within a section (p 0.12–0.51), or by Parisel σ within Currier A (p 0.22–0.59). Hands do differ in vocabulary beyond Timm's A / B / label groups and section (p 0.010), which is the pre-registered "scribes carry vocabulary" outcome. But the effect is gone once the quire is fixed (exploratory, p 0.50 for sheets, 0.29 for pages), so hand cannot be told from position in the book. σ carries extra vocabulary within hands mainly through its own cho/che words. **S13-Q (pre-registered):** with leaf distance and quire as covariates, sharing a Davis hand adds nothing (B herbal p 0.15, whole book p 0.51), while closeness in the book does. Hand is not separable from position.
  - **S14 A/B alignment: untestable at this size.** Fused Gromov–Wasserstein and an anchor-graph addendum both fail calibration. They can't find a known Latin respelling between different stretches of text (only on identical plaintext). Voynich A ↔ B shows nothing either way (p 0.17–0.35).
  - **S11-C drift: FAIL by the strict rule, but the drift is real and copying doesn't explain it.** Against within-page copying generators (40 seeds, two designs), only l passes on both halves (z +4.1 / +3.7). d (z −5.8 / −2.3), q and t (−1.9 to −5.1) move the same way on both halves. Generators centre on ρ ≈ 0, and the calibration passed. So the glyph drift down a paragraph (d, q, t fall, l and a rise) is beyond copying as modelled. Whether it is content order or a writing habit is open (S11-D).
  - **S11-D drift reset vs page habit: unresolved.** The test was calibrated (planted reset drift and planted page drift were each classified correctly). On the 35 Voynich pages with ≥ 2 paragraphs, FIT leans towards a reset within each paragraph (composite b_para p 0.027, b_page p 0.28). TEST shows neither (p 0.55 / 0.94). No drift carries across paragraphs on either half. Follow-up S11-E uses the short star paragraphs.
  - **S11-E (real paragraph markers): the drift mostly runs on down the page.** The parsed `pages2.json` misses most paragraph breaks (ZL3b-n's `<%>`/`<$>`; quire 20 has 293 paragraphs), so earlier "paragraph-level" drift tests were close to page level. With the real breaks (137 pages, calibration passed), the page component replicates on both halves (b_page p 0.001 / 0.003). The within-paragraph reset replicates on FIT only (0.010 / 0.31). The pre-registered verdict is unresolved, but the replicated part favours a writing habit drifting down each page over ordered content inside entries. **Caution for all paragraph-level work: use `transcriptions/paragraphs_ZL3b-n.json` (or `structure2/code/paras_fix.py`), not the `pages2` `mark` field.**
  - **P7-W, Dulov's wormholes (quire 20): one track through f113–f116 only, unresolved for order.** The track sits at the same spot on four consecutive leaves and is absent on f111–f112, which fits the current stack and Dulov's alternative equally. The automated order test failed its own validation (holes show the next leaf, not the background), so it is not used. **Superseded by §5d (by-eye trace, 22 Nov):** strict size gradient f113 < f114 < f115 < f116 = the current stack.
  - **S11-R(a): the S8 line-start rule survives the paragraph correction.** With real paragraph interiors, the line-initial excess is +0.154 / +0.106 (p < 0.001), the comparison positions are n.s., and repeats are still avoided (0.07–0.10 vs 0.14–0.16).
  - **⚠ Paragraph-break audit (22 Nov, `structure2/audit/AUDIT.md`).** pages2's `@` marks only flag the first locus of each text unit (464), while ZL3b-n has 738 real paragraphs (`<%>`/`<$>`). Every script using those marks was rerun with the corrected file `transcriptions/paragraphs_ZL3b-n.json`. **Changed:** the S8 side result "paragraph-initial glyphs depend on the previous paragraph's" (excess +0.25/+0.41) was a ring-start artefact. Corrected: +0.066 (p 0.001) / −0.003 (p 0.55), so it does not replicate. **Weaker:** S11 drift inside true paragraphs is about half the size (d ρ −0.07 instead of −0.14), and most of it is page-level drift (S11-E). The S11-C strict verdict is unchanged. **Unchanged:** S8/S8b/S8c/S8e line-start rule (all p < 0.001 in three transliterations), S8d pattern, S9, the 24-statistic profile and E1–E5 (page/line based), ingredient-list Q2 (already used raw marks), capitals, allographs, scribe tests. Paragraph-start gallows: 0.63 vs 0.44 gallows per word (was 0.58 vs 0.46).

- **S16, Greshko's own Naibbe code** (`naibbe_greshko/REPORT.md`, pre-registered, 22 Nov, PC). **FAIL.** His generators were run from a reviewed copy of his repository: 52- and 78-card decks, consonant–vowel and vowel–consonant respacing with his token reuse, his alternative "Voynichesque" cipher, and his 20 published reference ciphertexts, on Latin (*Nat. Hist.* XVI) and Italian (Dante). They match 6–8 of 24 TEST statistics plain and 6–11 with our line rule (best single run 11). Controls: fitted Timm 12–14, word-shuffled Voynich 11, glyph-shuffled 6, FIT half 23, hybrid 21–22. Every variant misses burstiness, near-copies, local repeats, line effects and word order; the reuse option is far too rare to help. The earlier Naibbe FAIL was not an artefact of one Latin ciphertext. Open: D1 recalibrated on his real tables (S16b).
- **S16b (26 Nov, PC `naibbe_greshko/s16b/`, pre-registered): D1 decoder on Greshko's real N52 tables. FAIL.** His N52 encryption re-implemented line for line (6 tables, card weights 20/8/8/8/4/4, 17/36 respacing, ambiguity-safe bigrams, 3% space removal), Voynich FIT/TEST shapes, frozen D1 settings (16 x 20M moves, 3-gram LM). TEST letters recovered (bar 0.80): Macer Latin (primary) **0.206**; tokens-shuffled control 0.058; Pliny 0.103; Dante 0.115; no space removal 0.174. Segmentation 93-96% right; 846-878 cipher symbols vs 278 for D1's own key. Diagnostic (post-FAIL): the majority-true key under the decoder's segmentation reads 0.887 of TEST and scores better on the objective than the SA best (-240.9k vs -244.7k); annealing started at the truth stays at 0.88. The model is right; the annealer fails to converge on ~3x as many symbols. Consequence: D1's Voynich FAIL rules out our 3-table Naibbe-style key, not a Greshko-style 6-table key. Naibbe is not reopened as a model (S16 profile FAIL), but the decoding test is incomplete for his tables. Next: S16d.
- **S16d (26 Nov, PC `naibbe_greshko/s16d/`, pre-registered): more search for the D1 annealer on Greshko's N52 key. FAIL.** Attempt 1 (16 x 200M moves): 0.207 TEST letters; attempt 2 (32 x 400M, 28 min): 0.207 (restarts 0.20-0.23, agreement 0.58). Bar 0.80. Every restart falls into the same wrong basin, although the true key scores better on the same objective and reads 0.887. Verdict: the D1 decoder cannot recover a Greshko N52 key at Voynich size; the obstacle is the search landscape (~880 symbols, rare gamma tables), not the move budget. D1's Voynich FAIL still does not cover Greshko-style 6-table keys. Voynich not rerun (stop rule).
- **S16e (26 Nov, cloud `s16e/`, pre-registered + amendment): new search (heat-bath sweeps over every letter per symbol, 4-gram LM, 64 restarts; D1 objective and segmentation unchanged). Strict FAIL (Italian), but Latin, MHG and Occitan are now calibrated for Greshko-size keys.** TEST letters on Greshko N52: Macer 0.884 (dev), Pliny 0.887, Megenberg MHG 0.876, Breviari Occitan 0.886 (last three held out); D1 own key Latin 0.936, MHG 0.890; shuffled control 0.063; Dante 0.194. The found keys score better than the true key, so the search now reaches real optima; Dante fails because the Italian LM corpus is noisy herbal OCR with library boilerplate (true key scores 11k worse), so D1's Italian runs were never calibrated either. Attempt 1 (staged, 3-gram, 16 restarts) failed (Macer 0.88 by 1 lucky restart, rest ≤ 0.12). Voynich run: S16f.
- **S16f (26 Nov, cloud `s16e/REPORT_S16f.md`, pre-registered): S16e decoder on the Voynich (FIT→TEST) in Latin, MHG, Occitan. FAIL in all three.** M1 4.58 / 4.44 / 4.31 (bars 3.78 / 3.38 / 3.68); M2 0.073 / 0.198 / 0.202 (bar 0.30); controls (Timm, word/glyph-shuffled, gibberish) match or beat the Voynich; top-8 restart agreement 0.11–0.19 (calibration 0.54–0.92). A Naibbe-style verbose homophonic cipher with Greshko-size tables is now ruled out for Latin, MHG and Occitan. Italian is still uncalibrated (S16g).
- **H10, Timm's Archetype palaeography data** (`h10/REPORT.md`, pre-registered, 22 Nov, PC). **Inconclusive.** The database (1,684 boxed glyphs, section hands mapped to Davis's scribes) has no variant coding, so features were measured automatically from Timm's full-resolution images (1,666 glyphs). No n-flourish or k feature meets the pre-registered Timm rule (tracks spacing within a scribe, scribe adds nothing) or Davis rule (scribe adds beyond layout and A/B). The automatic k-crossbar measure failed the by-eye check, so Davis's main criterion is not properly tested (H10b). What holds: 45–69% of n and sh variation is within pages; the n final stroke and sh-plume separation differ strongly by Currier A/B (plume separated 0.89 vs 0.71, p 0.0004; Pharma 0.95, as Timm says), and the five scribe labels add ΔR² ≤ 0.017 once A/B is known. Exploratory: B pages have tighter lines (116 vs 144 px) *and* smaller glyphs (58 vs 72 px), so relative spacing is the same (~2.0); "less room in B" is not supported as the cause. Agrees with S13: nothing in the hand data needs five scribes beyond A/B.

- **Section keys: a separate cipher key per section or Currier language** (`section_keys/REPORT.md`, pre-registered, 22 Nov, cloud). **FAIL in all 32 runs** (8 units: herbal A, herbal B, balneological, pharma, stars/recipes, astro+cosmo+zodiac, all Currier A, all Currier B; × Latin, MHG, Occitan, Italian). This uses the D1 decoder, re-implemented in the cloud. Calibrated at each unit's own size, it recovers 83–95% of a known Naibbe-style key in 7 of 8 units; pharma is underpowered (MHG 0.60). A mixed-key check shows the test can see per-section keys: five section keys are recovered at 92–93% per section, against 61% for one pooled key. On the Voynich, held-out M1 is 0.6–2.8 bits above the language bar and M2 is 0.02–0.12 against the 0.30 bar. Restart agreement is 0.09–0.21, the same as Timm and shuffled text, against 0.67–0.91 on known keys. Voynich decodes beat all five controls on both metrics in 11/32 runs, by small margins (e.g. 0.14 bits), which fits its known order and spelling structure, not a key. Closes D1's "keys that change by section" escape for this cipher family. Also found: the Pfeiffer Megenberg OCR ends in modern-German notes and glossary; it is now cut from the corpus (`section_keys/code/prep.py`).

- **Meaning inside the writing procedure: D6, D2, D3b** (`meaning_procedure/REPORT.md`, pre-registered, 22 Nov ~07:05–09:00 UTC, cloud).
  - **D6, real text hidden in the procedure's word choices: PASS (possibility).** The frozen hybrid writes TEST pages while redrawing each word until it falls in the bin named by the next message bits (held-out Pliny herbal Latin, Dante, Megenberg herbs, Huffman-coded). At 1–2 bits per word the text keeps 20–23/24 with R and d1d2 in band (key G, a scribe-feasible grid on first/last glyph: 14 of 15 runs at b 1, 13 of 15 at b 2) and decodes letter-perfect (accuracy 1.000). Capacity ≈ 2 bits per word (G) or 2–3 (whole-word hash); at 3–4 bits S3, S4, S6 and edge break. 2 bits per word over the manuscript ≈ 18k letters ≈ 3,000 plaintext words. Word order (S6) is the one statistic that notices the hiding. **So the profile cannot rule out a hidden message carried by word choice.** It gives no sign that one is present, and the procedure used leans on the real FIT word-pair table.
  - **D6-V, reading the Voynich through the grid channel: decoder calibration FAIL.** Annealing over cell → bit and code → letter tables recovers 1–10% of a planted message (bar 80%; the true key scores −2.2 vs −4.75 bits per letter found, so the search fails). Voynich and all controls collapse to one-letter output. Not interpreted.
  - **D3b, first/last glyphs as context classes beyond the boundary link: FAIL.** Knowing the whole neighbouring word instead of its touching glyph gains nothing on held-out sheets (Voynich −0.067 / −0.047 bits at k 5, +0.014 / −0.002 at k 20), below Timm (G_right +0.013 / +0.06), gibberish and the hybrid. Italian and MHG gain +0.10 to +0.17. The D3c-u code also gains nothing (its syntax sits in the touching glyphs), so the pre-registered "D3 prediction" was misframed.
- **D3d (26 Nov, PC `d3d/`, pre-registered): homophone merging, then the D3c one-to-one decoder. Calibration FAIL, Voynich not run.** Variants merged only within a (first glyph, last glyph) cell by PPMI context clustering (3 rounds), tau tuned on Italian D3c-u, frozen on MHG. Accuracy: Italian 0.002-0.018 over tau 0.2-0.7, MHG 0.000 (bar 0.30); gains over shuffled negative, inside the Timm control range. Oracle merge (true groups) gives 0.508 / 0.618, so the decoder works if groups are right; merging fails because most variants occur once or twice in 20k tokens (6.1-6.6k groups vs 5.4k true, merges 45-59% pure). Verdict: a homophonic whole-word code of the D3c-u kind is not recoverable by merge-then-decode at Voynich size.
- **D3e (26 Nov, cloud `d3e/`, development only): joint word-level decoder (code type → word heat-bath, cell rule as a Dirichlet-multinomial term in the likelihood). FAIL at development.** With maximum-likelihood emissions the truth is not the optimum (model failure); with a Bayesian (CRP) emission the truth's neighbourhood wins (-167.0k vs -169.1k), but 7 searches from scratch reach only 0.01–0.06 (bar 0.30). Mostly-singleton code types give the search nothing to grip. Closes the D3 decoding line; Voynich not run.
- **D10a (26 Nov, PC `d10/`, pre-registered): pharma (PH, 1,176 FIT / 1,126 TEST tokens), original D1 decoder, 8x stronger search (32 restarts x 80M). FAIL.** Calibration (Naibbe-style key at PH size, TEST letters): Latin 0.08/0.89/0.90 (mean 0.62; more moves not reliably better), MHG 0.93/0.85/0.90, Occitan 0.86, Italian 0.22, so PH is powered in MHG and Occitan only. Voynich PH: MHG M1 4.72 (bar 3.38), M2 0.152 (bar 0.30), controls Timm 5.03/0.146, word-shuffled 5.11/0.155, glyph-shuffled 5.11/0.117; Occitan M1 4.35 (bar 3.68), M2 0.153, controls 4.44/0.215, 4.33/0.195, 4.41/0.156. Restart agreement 0.13-0.20; decodes are letter salad. Bars missed and controls not beaten. A per-section Naibbe key for pharma is ruled out in MHG and Occitan; Latin and Italian pharma stay underpowered.
- **D10b (26 Nov, PC `d10/`, pre-registered amendment): shared cipher alphabet with one letter shift per sheet (Alberti-style). Calibration FAIL, Voynich not run.** D1 segmentation, then SA over a base key plus 26 FIT-sheet shifts (16 x 40M); TEST sheet shifts chosen by LM score. TEST letters: Latin unrotated sanity 0.919; Latin random shift per sheet 0.066; MHG 0.079; restart agreement 0.09-0.12. Seed 2 skipped (two-seed mean cannot reach 0.80). The search cannot find key and shifts together, so per-sheet keys stay untested, not ruled out.
- **D10c (26 Nov, cloud `d10c/`, development only): three new searches for per-sheet shifted keys (joint heat-bath over key + shifts; key from a shift-invariant letter-difference LM first; Poisson sheet-profile model). FAIL at development: 0.08 TEST letters (Latin seed 1), 4–6/26 sheet shifts right.** In every design the true key scores clearly better on the decoder's own objective and is stable when started there, so this is a search failure. Per-sheet keys stay untested, not ruled out; Voynich not run.
  - **D2a, order-specific slot grammar: PASS on 1 of 4 links.** A4 (onset of word i → onset of word i+2) is +0.0108 bits, p < 0.0005 (2,000 shuffles; deviation: the pre-registered 200 could not reach the Bonferroni level), above every procedure (Timm ≤ 0.0051, pure procedure ≤ 0.0016, hybrid ≤ −0.0002, gibberish −0.002) and ≥ Latin. A1 ending agreement, A3 and A5 fail. Exploratory: A4 replicates in ZL3b-n, IT2a-n, RF1b-e, survives dropping line-initial/final words, is **Currier B only** (A ≈ −0.003 to −0.015), and is an onset *alternation*: same onset on a different word two places on is 16.1% vs 14.5% shuffled (Timm +0.3–0.4 points), carried by q-, o-, ch- ("qokedy chedy qokedy"). A new unexplained structure, not a reading.
  - **D2b, constructed language (category prefixes, agreeing role endings, category grammar) through the procedure: FAIL.** Chosen on FIT (ρ 0.5, γ 0.3): 16–19/24 on TEST, 0/5. Strong grammar 12–14/24 (agreement and boundary break). At profile-compatible strength its grammar is nearly invisible (A4 0.001).

- **Follow-ups A4-G and D6-V2** (`meaning_procedure/REPORT.md`, `PREREG2.md`, 22 Nov ~07:55–11:45 UTC, cloud).
  - **A4-G: PASS, the onset alternation is a writing habit.** Adding one rule to the hybrid on Currier B pages ("5% of the time, start a word with the glyph that began the word two back"), chosen on FIT, gives TEST A4 +0.007 to +0.013 (Voynich +0.0115) with 20–21/24, 3/5 seeds passing. Without it A4 is −0.005 to +0.001. Pair copying (x y x′) overshoots or breaks the profile. It puts slightly too much of the effect into B and costs S6 on some seeds. **So the D2a link is not evidence of grammar;** it is a Currier B convention like the line-start rules.
  - **D6-V2: FAIL, no decoder passed calibration.** Three pre-registered annealing decoders and one post-hoc one recover 0.4–19% of a planted 1-bit-per-word grid-channel message (bar 80%); the Voynich was not decoded. A choice channel of this kind is out of reach of ciphertext-only search at this size, so the text can neither confirm nor exclude one.

- **Overnight cloud run M5, D4, D5** (pre-registered, 22 Nov ~08:40–12:10 UTC).
  - **D4, Bax-style names in Arabic, Persian or Greek: FAIL in all 13 runs** (`d4_names/REPORT.md`). Fitted glyph keys with sheet- and name-grouped CV (as C3): held-out rank 0.47–0.53 against shuffled-name nulls of 0.51–0.53, best p 0.10 (bar 0.0083). Bax's own reconstructed key, no fitting, on 81 herbal pages off his source leaves: best p 0.06, and the same key on glyph-shuffled words does as well. Star labels f67r–f68r through Bax's key are no closer to 73 Arabic star and mansion names than shuffled labels (p 0.61) or running-text words (p 0.49). Caveat: name lists written from standard names, not fetched (D4-V).
  - **D5, Tironian-style notes: FAIL** (`d5_tironian/REPORT.md`). Radical + ending signs with own signs for frequent words, rank-mapped onto Voynich chunks (Latin, Italian, MHG): 5–10/24, edge 0.004–0.015 (Voynich 0.19), word order 0.20–0.29 (0.07). Any one-sign-per-word system keeps the host's word order. The within-word onset–ending dependence (U 0.34–0.40 for 3-letter radicals, Voynich 0.38) fits, but Timm's generator (0.45) fits too, so it is not specific. No Tironian lexicon was reachable as data; sign shapes are untested (D5-S).
  - **M5, embedding alignment A vs B: untestable** (`m5_embed/REPORT.md`). VecMap-style unsupervised and identical-word-seeded alignment both fail calibration (Latin respelling P@1 0.00–0.02, bar 0.30). Supervised Procrustes given half the true dictionary reaches only 0.03 on Latin at 11k/23k tokens (0.31 on Spanish at 100k), so the size limit is fundamental. Voynich A↔B (S 0.504) equals B shuffled within page (0.506), Timm (0.503) and Latin (0.501). With S14, alignment methods are closed for the A/B question.

- **Follow-ups A4-P and D6-C** (`meaning_procedure/REPORT.md`, `PREREG3.md`, 22 Nov ~11:40–12:30 UTC, cloud).
  - **A4-P: PASS.** A4 (onset two words on) as a 25th statistic, band from a TEST-sheet bootstrap (+0.0066 to +0.0193; Voynich FIT +0.0083 inside). The hybrid + Currier B onset habit (a 0.05, not refitted) scores 21–22/25 with A4, R and d1d2 in band on 5/5 seeds. Without the habit A4 is missed on 5/5; pure procedure, Timm + rules and shuffled text all miss it. The habit costs 1.2 of the other 24 on average (mostly S6). **A4 belongs in the target profile; the best model now is hybrid + B onset habit.**
  - **D6-C, plant-name crib for the word-choice channel: calibration PASS, Voynich FAIL.** With genus names really hidden at the start of each herbal page (1 bit per word, grid key, 5-bit code), the crib decoder recovers 93% of held-out name letters (shuffled names ≤ 0.11). On the Voynich it gets 0.079, inside the shuffled-name range (99th pct 0.105) and level with Timm (0.068) and the pure procedure (0.070). Herbal pages do not open with their pre-1960 plant names through this channel.

- **PC overnight bundle T1–T5 + drawings v2** (pre-registered in `bundle/PREREG.md` and `vlm_drawings_v2/PASS_RULE_DRAWINGS_V2.md`, 22 Nov ~03:00–11:50 UTC, RTX 5060; summary `bundle/RESULTS_SUMMARY.md`). All on the FIT/TEST split, TEST scored once with seeds 900–904 unless stated.
  - **T1/S4, held-out statistics for the hybrid: split A PASS, split B FAIL.** Fitting only the 14 profile statistics, the hybrid matches 8–9 of the 10 never-fitted boundary/line statistics (per seed 9, 9, 8, 8, 9; R in band on 3/5), against 4.4 (Timm + rules) and 4.0 (within-page shuffle); FIT-half ceiling 10/10. The reverse (fit the 10, hold out the 14) gives 7–9/14 against controls of 10.0–10.8: FAIL. **So the line and boundary behaviour follows from a generator fitted to the profile, which is real held-out evidence for the procedural model; the converse does not hold.** Split A misses S3_sdlen, S4_zipf, S6_orderMI and editfirst (seed 900).
  - **T2, extended family (S2 + S3 + S8-P, 26 statistics): S2 PASS, S3 PASS, S8-P FAIL, overall FAIL.** A line-final word/ending table fixes E2 on 5/5 seeds (0.059–0.073 vs Voynich 0.087), the first model to do so stably; a length template fixes S3_sdlen on 5/5 (1.68–1.73 vs 1.78). With the vertical line-start statistics added, vrep stays too low (0.074–0.087 vs 0.102) and vdexc too high (0.067–0.096 vs 0.060): S8-P passes on 1/5 seeds, overall 23/26 on 2/5 (per seed 25, 21, 20, 23, 22). Controls 14–19/26. Ablations (exploratory, seeds 900–902): dropping the length template costs about 2 statistics (19–21); dropping the line-final or vertical rule costs nothing (22–23).
  - **T3/S6, the hybrid result under more seeds and stricter bands: FAIL.** The original rule (≥ 20/24 with R and d1d2) holds on 19/20 new seeds with the project's chunk bands, but on **0/20** with bands from a page bootstrap of the whole TEST half (which matches the sample size actually scored). No control reaches the rule under either. Fragile under project bands: S3_sdlen, E2. **The hybrid's 20–22/24 depends on band width**; it is a close fit at the project's tolerance, not an exact one.
  - **T4/S5, LSTM + page cache: FAIL.** The best setting uses no cache (pc 0, T 0.9): 18–19/24, 0/5 seeds pass. It misses burstiness, immediate repeats, E2, pagegal, R and ff. A generic short-memory model, with or without copying, does not reach the profile; the hand-built rules matter.
  - **T5/M3, contrastive page image ↔ text within section (mask v3 images): FAIL, borderline.** Drawings MRR 0.346 against a within-section null p99 of 0.350 (p 0.015) and a shuffled-train model at 0.239. The full-page positive control passes (0.394 vs p99 0.360). A weak hint, below the pre-set bar; replication listed (M3-R).
  - **Drawings v2, full drawings with ink outlines, text removed → text (VLM): FAIL, valid** (`vlm_drawings_v2/REPORT.md`). New text-line mask (mask v3; leak gate on train pages: own vs other X − D −0.0003 [−0.004, 0.004] vs 0.370 on full pages). A Qwen2.5-VL-3B adapter trained on 139 pages' text-free images: held-out X − D −0.00003 [−0.0010, 0.0009] bits/char, B − D 0.0044 [0.003, 0.006] (generic "a picture is present"); both leak probes clean. Outlines add nothing over paint alone (v1 X − D −0.0003). **Correction:** v1's INVALID flag was a probe bug (other-page text not capped to equal length); re-scored it is 0.011 [−0.003, 0.024], so v1 is a valid FAIL too.

- **D6-C2, plant-name crib over 5 channels × 2 positions** (`meaning_procedure/REPORT.md`, `PREREG4.md`, 22 Nov ~13:00–14:00 UTC, cloud). **All 9 new decoders calibrate (92–99% of planted names recovered on held-out pages); the Voynich hits none.** Channels: (first, last) glyph cell, first glyph, last glyph, glyph-count parity, gallows presence; name at page start or page end. Voynich held-out rates 0.035–0.117 are inside the shuffled-name 99th percentiles (0.049–0.134) in every configuration and never above both Timm and the pure procedure. Herbal pages do not carry their pre-1960 plant names through any of these word-choice channels.

- **D6-C3, zodiac labels and a 2-bit plant crib** (`meaning_procedure/REPORT.md`, `PREREG5.md`, 22 Nov 13:25–17:30 UTC with a pause, cloud). **FAIL.** Zodiac ring labels carrying the page's month name or Latin sign name, 1 bit per label (onset, ending, parity, gallows; the cell channel fails calibration): planted versions recover 67–84%; the Voynich gives 0.000–0.122, and the one value above the 20-run shuffled 99th percentile (onset/month, 6/49 letters) has permutation p 0.095 with 200 shuffles, ≈ 0.76 after correcting for 8 configurations, and vanishes in reversed reading order. Plant names at 2 bits per word: planted 0.93, Voynich 0.061 (shuffled 99th pct 0.090, Timm 0.071). Pharma jars have no known contents, so no crib is possible. **No crib of any kind tested so far gives a reading.**

**Updated net position.** The text's surface is best described by a *copy-and-modify generation process with a line-start convention*. No tested cipher, code, notation or constructed-language model comes close. Human gibberish reproduces the low-level oddities but not the line rule. This does not prove the text is meaningless. It does mean any decipherment must explain the local copying structure, which none of the tested schemes does. And any generator must explain the language-strength coupling across word boundaries, which none of the tested generators does. (22 Nov: a systematic word code with context-class first and last glyphs reproduces that coupling on held-out text, but not the copying structure; see `word_identity/`. Also 22 Nov: a real text *can* be hidden in the procedure's word choices at about 2 bits per word without the 24-statistic profile noticing, and Currier B has an onset alternation two words apart that no procedure makes; see `meaning_procedure/`.)

## 14. File index

- `cribs/` — crib and key tests (C1–C5), `REPORT.md`, `plant_ids.json`.
- `section_keys/` — per-section key test (PREREG, CALIB_LOG, REPORT, code, results).
- `plan/DECIPHERMENT_PLAN.md` — assessment and prioritised testing plan (21 Nov).
- `plan/SYNTHESIS.md` — how the text was most likely produced, and what would move it forward.
- Meaning tests: `meaning_tests/` (PREREG.md, REPORT.md, code/, texts/).
- Plan step outputs: `gibberish/`, `line_start/`, `word_codes/`, `ingredient_list/`, `naibbe_test/` (each has PREREG.md, REPORT.md, code/).
- Language and decipherment reports: `language_test/`, `word_families/`, `timm_generator/`, `grammar_labels/`, `decipherment_harness/`, `labels/`, `sheets_as_units/`, `plant_drawings/`, `calibration/`, `sources/`.

- `VOYNICH_HANDOFF_v2.md` — findings 8–14, mis-binding thread.
- `uploads/hearth/19f96944-783f-4aae-a432-420dffb662eb` (in ``) — v1 handoff, findings 1–7, 2006-scan folio map. `uploads/hearth/8e1c58e4-…` = v1 scripts zip.
- `voynich_scripts_v2.zip` — `parse.py`, `analyze.py`, `sheet_pairs.py`, `inner_outer.py`, `reorder2.py`, `lsa_reorder.py`, `skin.py`, `follicles.py`, `texture.py`, `wear*.py`, `stain_q20*.py`, `stain_ctrl.py`, `stain_all.py`, `visual*.py`; data `sheets_skin.json`, `tex_all.json`, `wear*.json`, `fol_all.json`, `canvas.tsv`.
- `skin_side_results.txt` — skin side and wear tests output.
- `figures/` — quire 20 stain maps and top-stain panel.
- `manuscript_wide/code/` — `t1_pairs.py` (pair types), `t3_order.py` (within-sheet + sheet order + positive control), `t6_quires.py`, `t7_timm3.py`, `t8_proposals.py`, `t9_groupings.py`, `p1_stains.py`, `p1b.py`, `p2_gutter.py`, `p3_offset.py`, `p4_feat.py`, `p4_test.py`, `vlib.py`, `seg.py`, `parse2.py`, `phys_feat.py`. Outputs `*.out`; `pages2.json`, `p4_feat.json`, `canvases.tsv`.
- `continuity/` — `CONTINUITY_REPORT.md`, panels, `fold.py`, `spread.py`, `panel.py`, `score.py`, `rank.py`, `gutter_baseline.txt`.
- `physical_offsets/` — `code/` (`prep.py`, `score.py`, `analyze.py`, `spreads.py`, `pp.py`, `overlay.py`; fix the scratchpad path), `.npy` score matrices, `names.json`, `figures/`.
- `page-order-review/` (in ``) — `proposed_orders.csv`, `proposed_orders_pages.csv`.
- `yale_images/` — 183 full-size pages + `manifest.json`.
- `forme_of_cury_pg8102.txt` — calibration text.
- Docs: manuscript-wide report ; literature review


## PC bundle 2 (22 Nov 2026, partial; U1 stopped, U2/U3 not yet run)
- **M3-R image-to-text replication: FAIL.** Mean drawings MRR over 5 seeds: 0.270 vs within-section null p99 0.313 (p 0.21) on split 1, and 0.253 vs 0.307 (p 0.39) on split 2. The full-page control passes on both. T5's p 0.015 was noise, so drawings do not predict text.
- **M2 glyph clustering (P1 step 1): PASS.** 58,869 train and 25,966 test components, K 32. Stability ARI 0.541; row-initial vs medial JS excess +0.129 over within-row shuffles (p<0.005).
- **U1 (not final):** the old T2 setting and hybrid 1594 fail under H bands (16–20/24). The H-band refit scores 19–20/24 and holds on 3 of 5 seeds, which meets the S6-C bar pending the JSON. It keeps missing S8_nearcopy, E2, nearadj and S3_sdlen.


## PC bundle 2 final results (finished 22 Nov 21:51 local)
Full summary: `bundle2/RESULTS_SUMMARY.md`.
- **M3-R (drawings↔text), FAIL.** MRR 0.270 vs null p99 0.313 (p 0.21); split 2 0.253 vs 0.307 (p 0.39). Full-page control passes. T5 hint did not replicate.
- **M2/P1 step 1, PASS.** Glyph-shape clusters ARI 0.541; row-initial JS excess +0.129 (p < 0.005).
- **S6-C, PASS.** U1b H-loss hybrid refit: 20,20,19,20,19 of 24, rule met 3/5 seeds (FIT 24/24, best control 14/24). Still misses S8_nearcopy, E2, nearadj, S3_sdlen. U1a FAIL; U1c FAIL 1/5.
- **S2S3-H, FAIL.** Held-out 4–5/10 under H (controls 2–3), R missed 5/5; fitting profile stats breaks boundary stats (R, ff, d1d2, edge).
- **S8-P2, FAIL.** Vertical pair 0/5: vrep 0.05–0.06 vs 0.102, vdexc 0.10–0.12 vs 0.060. Table-plus-avoidance cannot produce the line-start convention.
- Notes: U1 resumed twice; a resume bug ran 8,000 trials but selection was capped at the first 4,000 as preregistered and reproduced 3/5. U1c ended at 4,007 trials; U2 resumed once.

## PC bundle 3 results (23 Nov 2026)
Full summary: `bundle3/RESULTS_SUMMARY.md`; prereg includes Amendment 1 (W3 baseline row-finding fix, made before any W3 statistic).
- **S6-D (W1), PASS.** H scores 20, 21, 21, 19, 20 of 24; rule on 4/5, E2 and sdlen on 5/5, all three on 4/5. Chosen pLF 0.06, pLE 0.22, pT 0.83, tol 0, q 0.99. Still misses S8_nearcopy, nearadj, ff, editfirst. Best mechanical generator so far under H.
- **S8-P3 (W2), FAIL.** Vertical pair 0/5: vrep fine (0.08–0.10 vs 0.102) but vdexc 0.08–0.11 vs 0.060. Third failed version of the line-start rule.
- **P1 step 2 (W3), FAIL.** All pages aligned (3,523 test words); cluster→EVA first-glyph accuracy 0.194 vs baseline 0.186, null p99 0.193. P3 not scored (gate failed).
- **M1 (W4)** not run (opt-in).

## PC bundle 4 results (23 Nov 2026, 12:00 local)
- **S6-E (X1), FAIL by prereg.** Adds a one-glyph-edit-of-previous-word mechanism to S6-D (chosen pA 0.017, wFa 0.92, sA 0.49). H scores 23, 22, 22, 21, 23 of 24 (S6-D: 20, 21, 21, 19, 20); 3 of the 4 target gaps close on every seed; E2 and sdlen hold 5/5. But the generator rule holds on only 2/5 seeds, so all conditions are met on 2/5 (needed 3/5). Best control 14/24. Seed 900 misses only S8_nearcopy. Highest generator match to date, but not a pass.

## PC bundle 5 results (23 Nov 2026, 12:23 local)
- **S6-F (Y1), FAIL.** Redrawn copy endings, long-range one-glyph copies, R/d1d2 double-weighted (chosen pA 0.018, wFa 0.70, sA 0.77, aE 0.04, pW 0.009). H scores 21, 22, 21, 21, 22 of 24; rule 3/5; d1d2 3/5; E2 and sdlen 5/5; **S8_nearcopy matched 0/5**; all conditions 0/5. Best control 14/24. Long-range one-glyph copying does not reproduce the Voynich near-copy rate; the near-copy statistic resists every mechanism tried (S6-D, E, F).

## PC bundle 6 results (24 Nov 2026, 19:04 local)
Prereg: `bundle6/PREREG.md` (H bands). Full JSON stays on the PC in `bundle6/results/`.
- **S6-G (Z1), INFORMATIVE.** Diagnosis only, nothing fitted. Voynich TEST local near-copy rate (a one-edit neighbour in the previous 20 words) is 0.372 against a random-other-page base of 0.220. S6-E makes 0.277 local against a base of 0.218. The base rates are equal, so the gap is a real shortage of local copies, not a vocabulary or denominator effect.
- **Missing sources** (Voynich/S6-E ratio, page-bootstrap CI low > 1.5): target word is line-initial 2.11x, first-glyph deletion 1.85x, first-glyph substitution 1.82x, source 2–5 words back 1.65x. Last-glyph edits are already matched (sub L 0.90, ins L 1.02, del L 1.25). S6-D shows the same pattern (del F, ins F, sub F, line-initial).
- Other S6-E ratios: dist 1 1.15, dist 6–20 1.27, ins F 1.46, del M 1.30, ins M 1.22, sub M 1.28, same line 1.37, previous line same slot 1.51, previous line other 1.38, further back 1.17, target not initial 1.30.
- **Reading:** the generators lack a route where a line-initial word is a first-glyph variant of a word a few positions back. This names the next mechanism (S6-H). No meaning is claimed.

## Hidden message inside the procedure (25 Nov 2026, cloud, `hidden_message/PREREG.md`, `REPORT.md`)
ZL3b-n via pages2.json; FIT/TEST by sheet; controls = Timm + rules (5), pure procedure (5), full hybrid (5).
- **N2, line-indicator cipher: FAIL.** The first glyph of a line does predict the glyph mix of words 3+ of that line on held-out pages: 0.014 bits/glyph above a within-page key shuffle (p 0.005, 200 perms), in Currier A (0.013) and B (0.016). But Timm + rules makes 0.037–0.049 from line-level copying, so the Voynich is far below the copying control; the hybrid and pure procedure make none (≤ 0.001). A planted 4-key line cipher adds ~0.035–0.045 and is found at p 0.005. Reading: a weak line-level coherence, the size of copying, not a line key. New direction N2-b.
- **N1, autokey on the previous last glyph: FAIL.** Rank-matched per-context onset permutations (FIT) de-key TEST: boundary MI falls 0.222 → 0.072 and word order rises +0.099 bits/token (controls −0.060 to +0.093). But 20 random keys raise word order by +0.098 to +0.127 (99th pct 0.127), so the rise is an artefact of re-keying, and h2 rises +0.256 against Timm's +0.24 to +0.28 (max control 0.279). Calibration: a true autokey on Latin is 44% undone (7% raw) and recovers +0.038 of the 0.089 lost word order. No sign of an autokey.

## Published physical evidence (25 Nov 2026, cloud, `physical/README.md`)
Literature and data search for step 5 (P4, P5, S11-F, H10b/c). Files: `physical/data/*.csv`, `physical/sources/`.
- **Little underlying data exists.** Published: radiocarbon on 4 leaves, McCrone's 20-sample ink and pigment table (no spectra), 2014 multispectral images of 10 folios (released by Davis Sep 2024, public Google Drive, PC fetch needed), Davis's scribe assignments (already in ZL3b-n `$H`, 2022 revision), Zandbergen's collation. Not published anywhere: a list of scribal corrections or erasures, an ink-session map, XRF of text ink, a hair/flesh collation. Davis's singulion code was promised for GitHub; not found.
- **Radiocarbon check (new, negative):** f8, f26, f47, f68 (Scribes 1, 2, 1, 4; A, B, A, foldout) give 489–550 BP and agree with one date (χ² 1.53, df 3, p 0.67; combined 516 ± 18 BP, 1404–1438). It cannot order scribes or sections, and it dates the skins, not the writing.
- **Inks (McCrone 2009):** text and drawing inks on Scribes 1, 2 and 4 pages are all iron-gall with gum. Iron content (and opacity) varies: f47r and f78r text are "low iron". Quire mark and f1r alphabet are very low iron and high carbon; foliation is high iron. That gives three phases: text and drawings → quire marks → foliation.
- **MSI (2014):** no underwriting; Davis reports no scribal corrections on the ten folios. f93r text is written over a pigment stain, so painting came before writing there.
- **Hands:** the herbal hand changes by bifolium; 57/66 is split (57v Scribe 1); the Rose foldout is split (Scribes 2 and 4); **f115r lines 1–12 are Scribe 2, then Scribe 3**. That is a known within-page change for calibrating H10c (new H10d). `voynich-letters` (Ward 2026) finds the three main scribes' letter shapes identical except d.
- **Writing process:** **f88v's line-initial glyphs look written first as a column** (Zandbergen). That is a possible physical basis for the line-start rule (new P4-L, high priority). f105r has an ink change mid-page and an inserted partial line (P4-S). Stolfi documents later **retracing** of faded text (f2r, f1r, zodiac), so isolated dark glyphs can't be read as new pen dips without checking stroke ends and whitegrain.

## Line endings, LE series (25 Nov 2026, cloud, `line_end/PREREG.md`, `REPORT.md`)
ZL3b-n paragraph text, FIT and TEST separately; replicated in IT2a-n and RF1b-e. Nulls: within-line shuffle, within-page re-pairing of consecutive lines, label permutation.
- **ESTABLISHED: line-final words are their own class.** Final glyph E2 0.094 / 0.081 (null 0.003), with ‑m ×16.5 and ‑g ×26 (‑d ×1.7; ‑o, ‑r, ‑l depleted). Their *first* glyph is shifted too (JS 0.051 / 0.045). Only 65–68% of line-final tokens occur mid-line elsewhere, against 83–85% for mid-line tokens (LE4, p 0.003 everywhere). Unattested line-final words are usually an ordinary word with a different last glyph (25% attested after dropping it, vs 15%), not truncations. ‑m words have stems whose mid-line endings are mostly ‑iin, ‑r and ‑l (exploratory).
- **NULL: nothing crosses the line break.** The last glyph of line n does not predict the first glyph of line n+1 (MI excess +0.002 / −0.006), also with the S8 vertical rule held fixed. It does not predict whether line n+1 opens with a first-glyph near-copy (the S6-G pattern, p 0.31–0.56). Words are not split across lines (concatenation attested 0.7–1.1%, below re-paired 1.0–1.2%). Near-copies across the break run at 2.2–2.4%, against 1.6–1.7% re-paired and 4.7% for adjacent mid-line words: not established. **Line ends and line starts are separate rules.**
- **Margin lines vs paragraph-final lines (exploratory, robust).** Last word minus mid-line length: −0.18 glyphs at the margin, +0.49 at paragraph ends (difference p 0.002 on both halves and in all three transliterations; not due to ‑m/‑g). The pooled effect cancels, which is why earlier work saw no line-final shortening. The ‑m/‑d/‑n ending shift is present in both groups and larger at the margin (pre-registered H_margin: TEST p 0.007, FIT p 0.016, so the 0.01 bar is not met on FIT).
- **Wrap control: E3 is mostly layout.** Shuffling each paragraph's words and refilling its original line widths gives line-initial lengthening +0.37 (real +0.55; IT +0.34/+0.51, RF +0.47/+0.56), but no margin shortening, no paragraph-final lengthening and no E2. A long word that doesn't fit opens the next line. So most of E3 comes from wrapping. The line-start *glyph* rules (E1, S8) are untouched.
- **Generators (LE7): none reproduces the line-end features.** Timm + rules (`timm_rules_pages.json`): ‑m 0.28 and ‑g 0.155 at line end against 0.153 / 0.016; final words 0.46 glyphs too short; attestation deficit −0.09 against −0.16. Its later runs make no ‑m/‑g at all. The hybrid 1594 has no line-end effect (E2 0.002). S6-Dc / S6-H (with the T2 line-final table) are pending from the `s6h` thread.

- **N3, signal plus filler: finder FAILED calibration, Voynich not read.** Type-level mixture (signal types form a skip-filler bigram chain, filler unigram; prequential FIT objective; greedy flips). Planted Latin/Italian codebook words at 20–40% inside pure-procedure pages are recovered at 0.3–1% token recall (bar 0.6), although their true held-out order gain is 0.24–0.96 bits. On the Voynich the finder picks 52 types (6.8% of TEST tokens, chedy, shedy, qokeedy, qokedy …) with order gain 0.057 bits, below Timm (max 0.142) and the procedures (max 0.287) and inside the word-shuffled range (−0.049 to 0.047). Not interpretable as a negative because the finder cannot find a planted signal; replaced by N3b.
- **LE8 / LE11 (pre-registered follow-up): the margin vs paragraph-end split is CONFIRMED.** Paragraph-final minus margin last-word excess length D = +0.67 glyphs (null +0.02, p 0.001). It holds in Currier A (+0.61) and B (+0.78), in hands 1, 2 and 3 (+0.60, +0.63, +0.87; all p 0.001), and after matching on line word count (+0.48, FIT +0.47 / TEST +0.48). It is not due to the 39 right-justified or title lines (+0.67 without them). Short words close a line at the margin and long words close a paragraph, for every scribe.
- **LE9 (pre-registered): line-final ‑m is not a stand-in for one ending.** Its stems (a, da, ota, qoka, oka…) match the stems of the whole ‑iin / ‑r / ‑in / ‑l group. ‑iin is nearest on FIT, but on TEST ‑r is, and ‑iin wins only 12% of bootstraps (bar 95%). The ‑y sanity control passes (100%). So ‑m is one more choice in the a + {iin, in, r, l, m} ending slot, preferred at line end, not an abbreviation of one specific ending.

- **N3b, spectral finder: calibration FAILED again, Voynich not read.** PPMI of skip-4 co-occurrence, leading eigenvector, size by the FIT objective. The objective picks the top 10 types in every text. Planted signal recall 0–19% (bar 60%). Reported only: the Voynich top-10 subsequence (ol, chedy, or, shedy, chey, qokeedy, qokedy, qokeey …, 10% of TEST tokens) has held-out order gain 0.053 bits and ending agreement 0.042, just above every generator (≤ 0.045 / ≤ 0.040) and above word-shuffled Voynich (≤ 0.005). Planted Latin/Italian carry 0.24–0.96 bits, so this is at most a fifth of language strength. It fits the known A4 alternation (D2a) better than a hidden signal. **No subset with language-strength word order was found, but the finder cannot yet find a planted one, so N3 stays open (N3c).**
- **LE12 (pre-registered): the whole ending slot shifts at line end.** With ‑m removed, a-stem endings still differ final vs mid-line (JS 0.037 / 0.021, null 0.005, p 0.001 on both halves): ‑r ×0.5, ‑ir ×0.2, ‑iin/‑in ×0.7, ‑l ×0.85. o- and e-stems likewise. A generator needs an ending slot that depends on line position, not only a line-final word table.
- **LE13 (pre-registered): a line-final word table with separate margin and paragraph-final halves reproduces the line end (4/5 features on 4/5 TEST seeds); an ending-only redraw fails (1–2/5).** The pooled T2-style table misses the margin vs paragraph-end length split. But table words break the hybrid's local copying (profile 20 → 18/24: order, near-copies, word200, ff). The ending-only version keeps the profile (21/24, fixes E2) but stays short on E2 and the split. No version makes line-final words as rare as the real ones (LE4).

- **D6-P, hiding without the Voynich word-pair table.** Pure procedure (hybrid, pw 0, alpha 0), key G, 5 seeds: b 0 scores 14–16/24 (it fails the profile anyway, R missed). Hiding keeps that level at 1 bit (14–16) and 2 bits (13–15, ≥ 3/5 seeds within 1 of b 0 for all three texts), and at 3 bits for Latin and Italian (MHG 2/5); decoding exact (1.000), no fallbacks. **Capacity ≥ 2 bits per word: it does not need the FIT word-pair table.** Timm + rules (Java R1–R4, stego filter on the K-candidate pick, Latin): b 0 scores 17–19/24 (R ok, d1d2 missed); at 1 bit it drops to 12–13 on every seed and loses R, S8, S9, E3; 2–3 bits 14–15. Letters decode 99.2–100% at 1 bit (aligned), 95–99% at 2 bits. **Timm + rules cannot hide even 1 bit per word without visibly changing its text.** So hiding capacity depends on the generator's mechanism (slot procedure yes, Timm's line copying no), not on the word-pair table. As with D6, this shows possibility only; nothing suggests a message is present.
- **LE13b/c (pre-registered): copying line-final words from the page, short at the margin and long at paragraph ends, FAILS** (best 3/5 features on one seed). The length split can be matched, but E2 stays low and line-final words are far too ordinary (LE4 −0.07 vs −0.16). Line-final words are more often new forms than either page copies or a FIT table give.
- **LE13d (pre-registered): freshly built line-final words FAIL** (best 3/5). They come closest on LE4 rarity (−0.12 to −0.15 vs −0.16), but ‑m is far too rare (0.04 vs 0.15) and the profile drops to 19/24. **Summary of LE13–13d:** only separate margin/paragraph-final FIT word tables reproduce the line end, and they cost 2 profile statistics. No mechanism yet gets the line end while keeping the local copying.


## PC bundle 8: blocked diplomatic sources fetched and screened (25 Nov 2026, `bundle8/`, `regional/comparison/README.md`)
Fetched on the PC (242 files, all non-empty and md5-checked where a checksum exists), reduced to a 3.4 MB text extract and converted by `regional/comparison/code/prep_b8.py` into `regional/comparison/comparison_pages_b8.json` (13 texts, about 194k tokens). Screen: `code/screen_b8.py` → `screen_b8.out`, same `gen_stats` and Q1 rule as the first comparison screen (R < 0.5, edge > 0.1, lastlast < 0.02); every statistic is an excess over within-line word shuffles.

| key | lines | words | edge | lastlast | word200 | R | E1 | E2 | E3 |
|---|---|---|---|---|---|---|---|---|---|
| **Voynich TEST** | manuscript | 20396 | 0.192 | 0.008 | 0.11 | 0.32 | 0.206 | 0.077 | 0.54 |
| de_bav_megenberg_buch_natur_1482_ridges | print lines | 9798 | 0.097 | 0.089 | 0.55 | 4.08 | 0.016 | 0.016 | 0.04 |
| de_swabian_gart_gesundheit_1487_ridges | print lines | 12486 | 0.056 | 0.056 | 0.45 | 5.81 | 0.031 | 0.037 | 0.25 |
| de_tallat_artzneybuechlein_1532_ridges | print lines | 7958 | 0.072 | 0.056 | 0.54 | 5.71 | 0.061 | 0.013 | 0.19 |
| de_alsatian_brunfels_kreuterbuch_1532_ridges | print lines | 14210 | 0.056 | 0.045 | 0.43 | 5.21 | 0.033 | 0.015 | 0.13 |
| de_bock_kreuterbuch_1539_ridges | print lines | 8846 | 0.055 | 0.052 | 0.29 | 3.49 | 0.023 | 0.042 | -0.31 |
| de_fuchs_kreuterbuch_1543_ridges | print lines | 8627 | 0.064 | 0.057 | 0.44 | 4.38 | 0.047 | 0.052 | -0.27 |
| de_schellenberg_experimenta_1550_ridges | print lines | 5111 | 0.044 | 0.040 | 0.20 | 3.08 | 0.040 | 0.041 | -0.11 |
| de_bodenstein_wie_sich_meniglich_1557_ridges | print lines | 5458 | 0.035 | 0.023 | 0.13 | 1.53 | 0.042 | 0.037 | -0.04 |
| de_austrian_klosterneuburg_cod48_ms_15c | MANUSCRIPT lines | 26438 | 0.057 | 0.060 | 0.48 | 5.24 | 0.008 | 0.014 | 0.31 |
| de_swabian_inzigkofen_oct842_ms_15c | MANUSCRIPT lines | 45668 | 0.051 | 0.062 | 0.38 | 4.69 | 0.010 | 0.013 | 0.22 |
| de_swabian_inzigkofen_fol1045_ms_15c | MANUSCRIPT lines | 22670 | 0.051 | 0.068 | 0.41 | 5.07 | 0.008 | 0.013 | 0.24 |
| de_bav_enhg_charters_1480_85_ms | MANUSCRIPT lines | 18516 | 0.069 | 0.066 | 0.51 | 5.50 | 0.009 | 0.011 | 0.21 |
| de_wuerzburg_buoch_guoter_spise_c1350 | NONE | 7536 | 0.161 | 0.157 | 0.75 | 3.43 | 0.007 | 0.003 | 0.01 |

- **NEGATIVE: no new text has the Voynich boundary profile** (Q1 none; R 1.5–5.8 vs 0.32). Diplomatic RIDGES herbals (1482–1557) sit with the OCR prints; the OCR *Gart* (R 5.6) and RIDGES *Gart* (5.8) agree, so OCR noise did not drive the earlier screen.
- ***Buoch von guoter spise* repeats the recipe-book pattern:** edge 0.16 near the Voynich, but through whole formulae (lastlast 0.157, 20× Voynich; word200 0.75).
- **NEW: real 15th-c. Upper German manuscript lines have no line-position word classes.** Four sets, three scriptoria, 113k words: E1 0.008–0.010 (Voynich 0.206), E2 0.011–0.014 (Voynich 0.077). Print lines show slightly more (E1 0.02–0.06, from headings and initials). The Voynich line-start and line-end rules are not a habit of German scribes of the period writing ordinary text. Caveat: genre is sermons, devotional and charters, not herbals, and letters are compared with EVA glyphs.

- **D11, copying generator through the section-key decoder: mostly explained, not fully by the rule.** Same decoder and settings (16 restarts × 20M moves), hybrid and pure procedure laid out at all 202 slots and cut to each unit's sizes. The full hybrid beats Timm, word- and glyph-shuffled text on both M1 and M2 in 9/32 runs (Voynich 11/32; pure procedure 5/32). The median Voynich advantage over the hybrid is 0.008 bits per letter on M1 and 0.000 on M2. But the Voynich beats the hybrid on both metrics in 13/32 runs (pre-registered bar ≤ 8), mostly herbal B, pharma and Italian, so by the rule the margin is **not fully explained**. The pure procedure is clearly worse (median 0.16 bits), so the word-pair copying in the hybrid carries most of the margin. Every decode is still 0.6–2.8 bits from the language bar; there is no key. One hybrid seed only (D11b).

- **S16c, Naibbe with heavy copying: FAIL.** Greshko's own N52 and CV-respacing ciphers (fresh clone, Latin and Italian, 5 seeds) plus a copy layer (pc 0.1–0.75 of tokens copied from the last 20–80 words, optional one-glyph edit) and the line-start rule; settings chosen on FIT. TEST scores: N52 Latin 11–14, N52 Italian 12–13, CV Latin 11–13, CV Italian 10–13 of 24 (bar 20). FIT selection kept copying low (pc 0.1–0.2), because heavier copying lowered the score. Near-copies match in CV Latin 3/5 and CV Italian 5/5 seeds, never in N52, but those variants lose word length, burstiness and repeats. All variants still miss word order, line effects (E2, E3, edge, R), ff and pagegal. **Adding copying to a Naibbe cipher fits worse than the pure procedure (14–16) and far worse than the hybrid (21–22).** Copying alone does not rescue a verbose homophonic cipher.

## S6-H (cloud, 25 Nov 2026): line-start copying generator, **PASS**
Prereg and report: `s6h/PREREG.md`, `s6h/REPORT.md`. H bands, ZL3b-n, TEST seeds 900–904.
- **Mechanism:** with probability pL (fitted 0.043), a line-initial word is a first-glyph substitution/deletion (FIT line-initial edit table) of a word 2–5 back; with pG (0.063), other words are first-glyph variants of a word 2–5 back. Built on a cloud reconstruction of S6-D/S6-E (the PC code isn't in the cloud).
- **Result:** generator rule 5/5 and S8_nearcopy 5/5 (both on 5/5; needed 3/5). H scores 22, 20, 20, 20, 22. E2 and sdlen 5/5.
- **Controls:** the cloud base S6-Dc already matched nearcopy 2/5 (S6-Ec 3/5), so the real gain is 2/5 → 5/5 (ratio ~1.30 → ~1.46 vs Voynich 1.49). Taking the source from another page drops nearcopy to 1/5, so the gain comes from locality. Timm + rules and the within-page shuffle match nearcopy but fail the rule (10–14/24).
- **Costs:** `edge` is now missed on 5/5 seeds; `editfirst` is missed by every cloud model. The vertical line-start pair is matched 0/5 (vdexc ≈ 0 vs 0.060), so this route does not explain the S8 line-start convention.
- **Exploratory breakdown:** S6-H closes first-glyph sub/del and the 2–5-back gap. First-glyph **insertion** is still short 1.79x [1.54, 2.04].
- Stage B (adjacent near-copy) chose pA ≈ 0 in the cloud. Line-endings thread: no line-end → next-line-start dependency, so nothing was added for it.
- **LE7 on the S6 family (S6-Dc/Ec/H, cloud): surface right, structure wrong.** S6-H matches E2 (0.071), the ‑m share at line end (0.146) and margin shortening (5/5 seeds). It misses line-final rarity (LE4 −0.42 vs −0.16: its final words are *too* rare), the ending-slot shift (LE12a 0.37–0.45 vs 0.022), paragraph-end lengthening (D ≈ 0 vs +0.75), the mid-line ‑m share (2×) and ‑g (2×). Line-final features 2/5 on every seed. Its line-start copy route does not import ‑m/‑g into line starts (0.0063 vs Voynich 0.0048; S6-Ec 0.0074).

## LE14 (cloud, 25 Nov 2026): line-type line-final words on S6-H, **FAIL** (`le14/PREREG.md`, `REPORT.md`)
- **Mechanism:** 80% of last words (pX 0.80) come from a new route: 71% whole words from a FIT table for that line type (margin or paragraph-final), 29% a stem from the page plus a line-type ending, with short stems preferred at the margin and long ones at paragraph ends. Words from this route skip S6-H's last-glyph rule (Amendment 1, made before fitting).
- **Result:** both parts of the rule held on 1/5 TEST seeds (3 needed). Profile kept (generator rule 5/5, S8_nearcopy 5/5). LE features 3, 2, 3, 4, 3 of 5 (S6-H 2 on every seed).
- **Fixed relative to S6-H:** line-final rarity (LE4 −0.15 to −0.19, Voynich −0.16; S6-H −0.42) and most of the paragraph-end lengthening (D +0.39 to +0.60, Voynich +0.75; S6-H ≈ 0).
- **Controls:** one pooled table drops D back to ≈ 0, so the margin/paragraph-end split needs separate line types. Stems taken from another page work as well as the current page, so the line-final word is not a local copy. Timm + rules and the shuffle fail everything.
- **Still wrong:** the ending shift LE12a is 0.05–0.09 against 0.022 (0/5 seeds). E2 is slightly low (0.061–0.069, band ≥ 0.063). ‑m mid-line and ‑g at line end are both about 2× too common, carried over from the base. Next: LE14b (all last words through the route, base rule off, ending table by stem class and line type).

## H10d (cloud, 25 Nov 2026): can image measures see a known hand change? **BLIND** (`h10d/PREREG.md`, `REPORT.md`)
- Seven line-level measures from the Yale photos (ink tone, stroke width, core height, ink density, slant, spacing, line pitch), with break scores against placebo breaks on single-scribe quire-20 pages. 8 of 22 placebo pages passed the line-finding gate. f115r passed (45/45 lines, checked by eye).
- **Davis's Scribe 2 → 3 change after f115r line 12 scores at the 28th percentile of paragraph-start placebos (rule for "see": above the 95th).** No single measure stands out. These coarse measures can't tell scribes apart, so they can't decide H10c either.
- Exploratory: the strongest break on any measured page is on f115r after line 17, an ink-tone step (d = −7.9, 100th percentile) in the middle of a paragraph, visible by eye. It is either a new ink session inside Scribe 3's stint, or the scribe change is really at 17/18. Only a letter-form check can tell (H10e). The line tone detector can be reused to map ink sessions (P4-S-a).

## P4-S-a (cloud, 25 Nov 2026): ink-tone steps across pages — **not testable** (`p4s/PREREG.md`, `REPORT.md`)
- The H10d line finder passed its gate on only 13 of 117 text pages (it fails on illustrated pages), and the detector found one step: f103r after line 14, mid-paragraph. The pre-registered T1 ("are steps at paragraph starts?") read 0/1, which says nothing. Needs real line segmentation (Kraken on the PC, P4-S-b).

## D11b (cloud, 25 Nov 2026): decoding margin over 5 hybrid seeds (`d11b/PREREG.md`, `REPORT.md`)
- Same section-key decoder as D11, 4 new hybrid layouts. The Voynich beats the hybrid on both M1 and M2 in 13, 14, 14, 14, 14 of 32 runs: median 14 > 8, so **not explained** by D11's bar. That bar was too strict, though. Two seeds of the same hybrid beat each other in 6–15 runs, and 14 is at the top edge of that range.
- **The per-run pattern is real:** 10 runs are robust (Voynich beats ≥ 4 of 5 seeds), 9 of them among D11's 13. Exploratory: the Voynich beats all 5 seeds in 5 runs. Any single hybrid seed beats all 4 others in at most 4, which is an easier bar. Most robust runs are Currier B units (herbal B, pharma, recipes, all-B) decoded with the MHG and Italian letter models, with gaps of +0.05 to +0.34 bits per letter. In astronomy the hybrid decodes better.
- Reading: the hybrid misses a little of the glyph-level regularity in Currier B that a substitution decoder can use. Every decode is still 0.6–2.8 bits from the language bar, so there is no key. Next: D11c (newer generators, skeleton-preserving shuffles).

## S6-I (cloud, 25 Nov 2026): first-glyph insertion in the copy route, **PASS** (`s6i/PREREG.md`, `REPORT.md`)
- Built on S6-H. When the line-initial or 2–5-back copy route fires, it inserts a first glyph with probability pI, using FIT insertion tables. Fitted values: pL 0.24 (5× S6-H), pI 0.44, and pG ≈ 0.
- **Generator rule + S8_nearcopy on 5/5 TEST seeds (H scores 20–22)**, and the first-glyph insertion ratio fell from 1.79 to 1.26 [1.08, 1.44], so it is no longer flagged. **`edge`, missed by S6-H on every seed, is now matched on 5/5.** `editfirst` is still missed.
- Costs: first-glyph deletion reopened to 1.56 (the fit dropped the general mid-line route), and line-initial targets are now slightly over-produced (0.87). With the insertion source taken from a random page, the control still passes 4/5 and recovers edge, so the edge gain comes from insertions at line starts, not from locality. Line end unchanged (2/5). Next: S6-J (separate edit weights for line-initial and mid-line copies, plus the LE14b line end).

## LE14b (cloud, 25 Nov 2026): every last word through the line-type route, **FAIL 2/5** (`le14b/PREREG.md`, `REPORT.md`)
- Same as LE14, but every line-final word comes from the line-type route, so the base's last-glyph rule never touches one, and stems and endings are split the way LE12 measures them. The fit put almost all weight on whole words from a flattened line-type table (σ 0.05, tX 1.5).
- **Both parts of the rule on 2/5 seeds (3 needed).** Line-end features 4, 3, 3, 2, 5 of 5. The ending shift LE12a is down to 0.030–0.052, in the CI on 2 seeds (LE14: 0/5). LE4 is in the CI on 5/5. Paragraph-end lengthening weakens (1/5), ‑g at line end rises to 0.03–0.04 (Voynich 0.016), and the generator rule holds on 4/5. The pooled-table control again removes D.
- Reading: a separate vocabulary for margin lines and for paragraph-final lines accounts for nearly all of the line end. What is left is a trade-off from flattening that vocabulary. Next: LE14c (separate temperatures per line type) and S6-J (queued: this line end plus S6-I's copy edits).

## N3c (cloud, 25 Nov 2026): cross-validated signal finder, **calibration FAIL** (`n3c/PREREG.md`, `REPORT.md`)
- Forward selection of word types by held-out bigram gain recovered 0.2–11% of the planted Latin/Italian signal tokens (bar 60%). As registered, the Voynich result is not read. The problem is the search, not the objective: one type on its own carries no order, so adding types one at a time never assembles the signal group, and the procedure's own locally repeated types get picked instead. N3, N3b and N3c all fail calibration. Next: N3d (an HMM fitted by EM, or adding types in pairs).

## C5 (cloud, 25 Nov 2026): Voynich line end vs 13 real manuscripts (`c5/PREREG.md`, `REPORT.md`)
- Six line-end features, each measured as an excess over within-line shuffles, on 13 manuscript-line sets (German, Occitan, Italian, Latin) and 8 printed herbals.
- **Voynich-specific:** the glyph shift at the line end. E2 is +0.083 against at most +0.056 in the manuscripts (German 0.005–0.015), and E2first is +0.043 against at most +0.028. Both are far beyond 2 sd.
- **Within scribal range:** line-final words being rare elsewhere (LE4 −0.15; manuscripts −0.07 to −0.31, from split words and abbreviations) and long words on short (paragraph-end) lines (+0.61; range −0.72 to +1.52).
- **At the edge:** short last words on full lines (−0.16; only the Latin set shortens, the rest lengthen), and the top glyph lift (‑m 24; manuscripts up to 15, one printed herbal 52).
- Reading: only the glyph-level ending system (‑m/‑g) needs a Voynich-specific explanation. The other line-end facts are ordinary layout.

## LE10 (cloud, 25 Nov 2026): line-initial lengthening beyond wrapping (`le10/PREREG.md`, `REPORT.md`)
- E3x = E3 minus the E3 of re-wrapped text. **Voynich TEST +0.18 [+0.10, +0.26]:** a real line-start lengthening of about 0.18 glyphs remains once wrapping (+0.40) is taken out.
- **No generator produces it.** The hybrid and S6-H match raw E3 by layout alone (E3x 0.02–0.05). LE14, LE14b and Timm + rules miss both. From now on the target profile should use E3x, not E3. Earlier verdicts stand as they were scored. New target: LE10b (a line-initial lengthening mechanism).

## C5b/C5c (cloud, 25 Nov 2026): line ends and rhyme (`c5/REPORT.md`, `PREREG_C5c.md`)
- The one manuscript set that comes near the Voynich's line-end glyph shift (Occitan, E2 0.056) is troubadour verse, and its shift comes from rhyme. Prose manuscripts reach at most 0.020; the Voynich is at 0.083.
- **Pre-registered rhyme test: absent.** Line-final words of adjacent or alternate Voynich lines share their last two glyphs no more often than words from random lines on the same page (ratios 1.02–1.07, p > 0.1, in Currier A and B alike). The verse calibration passes (Occitan 1.28, Italian alternate lines 5.2), and prose manuscripts show mild neighbour similarity (1.1–1.4). So the Voynich line end is a shared line-final vocabulary, not rhyme, and nearby line ends are less alike than in prose.

## D11c (cloud, 25 Nov 2026): the Currier B decoding residual with newer generators (`d11c/PREREG.md`, `REPORT.md`)
- The same section-key decoder on S6-H and LE14 layouts. By the pre-registered rule the residual shrinks only partly: of the 10 robust D11b runs, the Voynich still beats each generator on both metrics in 6 (shrink would be ≤ 5, persist ≥ 8).
- In substance the residual persists. The M1 gap in those runs is still positive and the same size (+0.02 to +0.35 bits per letter) in 19–20 of 20 cells. The newer generators decode slightly worse than the hybrid overall. The residual comes from structure inside lines, not from line layout. Next: D11d (skeleton-preserving glyph shuffles).

## S6-J (cloud, 25 Nov 2026): copy edits + line end combined, **FAIL 1/5** (`s6j/PREREG.md`, `REPORT.md`)
- S6-I's copy routes, with separate insertion shares for line-initial and mid-line copies, on top of the LE14b line end. Fitted values: pL 0.065, pIL 0.93, pG 0.02, pIG 0.39.
- All parts held on only 1/5 seeds. The generator rule held on 2/5 (scores 19–20), line-end features 2–4/5, nearcopy 5/5. No first-glyph edit type is flagged missing, but overall local near-copies fell to 0.289 (Voynich 0.372) and `edge` is missed again.
- Reading: the stages compete through the shared word stream. Taking every last word from a table thins the copy pool, and the fit then cuts line-start copying. No generator yet holds the profile, near-copies by edit type and the line end together. Next: S6-L, a joint fit with table words fed back into the copy pool.

## D11d (cloud, 25 Nov 2026): what the decoder uses in the Currier B residual, **mixed** (`d11d/PREREG.md`, `REPORT.md`)
- Voynich text with glyphs randomised within their class (gallows, benches, e, i, a/o, y, q, d/s, l/r, n/m/g) went through the same section-key decoder in the 10 robust runs. The class-shuffled text still beats the hybrid in 6/10 runs, so the result is mixed.
- In the large units (all-B, BIO, REC, all-A) the edge survives, so there the decoder is using the glyph-class skeleton and word order. In herbal B and pharma it disappears, but those units are small and noisy (shuffle seeds differ by up to 0.3 bits). Next target: WS1, word-skeleton statistics in generator scoring.

## WS1 (cloud, 25 Nov 2026): word skeletons (glyph-class strings), Voynich vs generators (`ws1/PREREG.md`, `REPORT.md`)
- **No generator matches.** All copy-and-vary generators (hybrid, S6-H, LE14, LE14b, S6-J) make skeletons that are too varied. Held-out skeleton entropy is 9.4–9.7 bits against the Voynich's 8.87 [8.74, 8.99]. Words are also built too loosely inside: within-word class entropy is 2.03–2.08 against 1.92 [1.89, 1.95]. The gap is bigger in Currier B. Timm + rules errs the other way (too predictable).
- This points to the structure the decoder exploits in D11d: a tighter word-internal class grammar than the slot tables and single-glyph mutations give. One deviation: the bootstrap CI for skeleton type counts is biased, so K is read raw. Next: WS2, a skeleton-constrained word route.

## N3-A4 (cloud, 25 Nov 2026): the top-10 types' extra order is not the A4 onset habit (`n3a4/PREREG.md`, `REPORT.md`)
- The N3b top-10 Voynich types carry 0.053 bits/token of held-out skip-filler order (generators ≤ 0.045). Reduced to onset classes they keep only 0.016. With the onset stripped they keep 0.050. The order is also stronger in Currier A (0.079) than in B (0.034). So it is not the B onset alternation A4. It sits in the endings and bodies of the commonest words. It is small but above every generator. Next: N3-A4b (which pairs carry it).

## S6-K (cloud, 25 Nov 2026): vertical line-start chain + line-initial lengthening — FAIL 1/5 (`s6k/PREREG.md`, `REPORT.md`)
- Line-start lengthening (E3x) is now reproduced: inside the Voynich TEST CI on 4/5 seeds (S6-J was about 0). With E3x counted, the generator rule passes 5/5 for the first time.
- A copy chain from the word above at line starts reproduces the vertical excess vdexc (+0.06 to +0.10 vs Voynich +0.060). The same chain not tied to line starts does not, and nor does any control.
- It fails because the vertical excess overshoots on TEST (vdexc 0.076–0.098, window 0.048–0.072; FIT sheets have 0.090, so this is mostly a FIT/TEST sheet difference) and on the line-end set (1–4/5). [Corrected: an earlier line here blamed exact repeats vrep; vrep 0.08 is inside its window.] edge, editfirst and nearadj are still missed by every S6 model.
- N3-A4b (exploratory): the extra filler-word order is mostly local repeats; the generator makes the same amount on other pairs. Not evidence of a grammar.

## WS2 (cloud, 25 Nov 2026): word-skeleton filter on S6-I — FAIL 0/5 (`ws2/PREREG.md`, `REPORT.md`)
- Filtering mutated and fresh words by a FIT skeleton trigram model brings word-shape entropy part way to the Voynich value (H1 9.5 → 9.1–9.2, Voynich 8.87; Hin 2.03 → 1.94–1.97, Voynich 1.92) and keeps the profile. It never lands inside the CI for both on one seed.
- A filter built from shuffled skeletons gets about half of the same gain. So the generator's main excess is too many distinct word shapes in general; the specific skeleton grammar adds only a little on top.

## N3d (cloud, 25 Nov 2026): two-chain hidden-word finder — calibration FAIL (`n3d/PREREG.md`, `REPORT.md`)
- Scoring signal and filler chains together finds more planted words than N3c (recall 0.08–0.40), but it also takes the commonest filler words, so precision is low. The Voynich result is not read (it would also not beat the best procedural control: 0.250 vs 0.277).
- The N3 family's 0.6 recall bar cannot be met by any finder: only 23–58% of planted tokens belong to types common enough to be candidates. N3e needs a fair calibration.

## S6-L (cloud, 25 Nov 2026): joint refit of all generator stages — FAIL 0/5 (`s6l/PREREG.md`, `REPORT.md`)
- Fitting the stages together, not one at a time, gives 21–22/24 statistics and the near-copy match on every TEST seed. The added exact vertical-copy term is not needed (it answered a misreading of S6-K, now corrected).
- The line-start column effect is reproduced in sign and existence, but its size differs between FIT and TEST sheets (0.090 vs 0.060) by more than the pass window, so the fitted model overshoots on TEST. The line-end set still holds on only 1–2 seeds of 5.
- Net state of the generator line: one mechanical generator matches most of the text's statistics together; line-end detail, the edit-type mix (edge, editfirst) and word-shape variety (WS2) remain open.

## N3e (cloud, 25 Nov 2026): pruned finder with fair calibration — calibration FAIL (`n3e/PREREG.md`, `REPORT.md`)
- Adding a step that keeps only word types with order among themselves makes the finder precise when the planted signal is strong (Italian 40%: 94%), but it throws away most planted words (reachable recall 0–0.46). At 20% it finds nothing planted.
- Five finders have now failed calibration. Hidden ordered words at ~20% among procedural filler cannot be found by order alone with this much text. The N3 line is parked.

## WS3 (cloud, 25 Nov 2026): word-shape filter on all routes inside S6-L — FAIL (`ws3/PREREG.md`, `REPORT.md`)
- The closest generator so far on word shape (H1 8.95–9.10 vs Voynich 8.87; Hin in CI on 3/5 seeds), with the profile kept and the best line-end match yet. Still only 1/5 seeds hold word shape and near-copies together.
- Most of the gain comes from a lower mutation rate and from filtering at all; the Voynich skeleton grammar itself adds about 0.05–0.1 bits. Word-shape variety trades off against the other statistics.
- State of the generator line after tonight: one mechanical copy-and-vary generator matches most measured structure together. What remains looks like trade-offs within the family, not a missing mechanism. Nothing here says anything about meaning.

## N2-b (cloud, 25 Nov 2026): the line-start glyph → rest-of-line link is missing from every S6 generator (`n2b/`)
- Voynich: a line's first glyph predicts the glyph mix of the rest of the line (+0.014 bits/glyph over permutations, p 0.005). S6-H, S6-K, S6-L and WS3 all give zero on every seed; their line-start mechanisms touch only the first word.
- This is one of the clearest gaps left between the Voynich and the best mechanical generator. A "line mode" set at the line start would make it, whether in a cipher (line indicator) or a procedure. Next: S6-M tests a mechanical line mode.

## S6-M (cloud, 25 Nov 2026): a word-table line mode cannot add the line-start link — FAIL 0/5 (`s6m/`)
- Drawing words for the rest of a line from a table keyed to the line's first glyph makes the N2 link only at a rate that breaks the copy-and-vary profile (13/24). The fit chose to switch it off. The link and the profile do not fit together this way; Timm + rules has the link but not the profile.
- This line-start → rest-of-line link is now the clearest Voynich property no tested model reproduces along with everything else. A glyph-level line mode (S6-N) is the remaining mechanical candidate.

## S6-N (cloud, 25 Nov 2026): a glyph-level line mode reproduces the line-start link — PASS 5/5 (`s6n/`)
- Keeping template words whose glyphs suit the line's first glyph (and redrawing others by the same route) gives the Voynich line-start → rest-of-line link (0.019–0.022 vs 0.014) with the 24-statistic profile and near-copies on all 5 TEST seeds.
- A control keyed to the wrong glyph mixes also makes the link (too strongly), so the link needs only some line state set at the line start, not the Voynich's particular pairing. This fits a mechanical line mode. It does not separate a cipher's line indicator from a scribe's habit. No meaning is claimed.

## S6-O (cloud, 25 Nov 2026): line mode + word-shape filters together — FAIL 0/5 (`s6o/`)
- Together they bring one word-shape measure (Hin) into the Voynich range on every seed, but the other (H1) stays high. The fit's higher mutation rate lengthens mid-line words and so removes the line-start lengthening, so the profile rule fails on 3/5 seeds. A shuffled-skeleton control does not have this conflict.
- The fixes found tonight work one at a time but interfere when combined. No single generator yet holds everything at once.

## S6-O2 (cloud, 25 Nov 2026): the closest generator yet — FAIL 0/5 (`s6o2/`)
- With the mutation rate held fixed, one generator holds the 24-statistic rule, near-copies and the line-end set on every seed, and one word-shape measure (Hin). The other word-shape measure (H1) is 0.02–0.07 bits too high, and the line-start link sits at the lower edge of its window (3/5).
- Only the real Voynich skeleton scorer brings Hin into range; a shuffled one does not. Word-internal glyph order is a real ingredient of the text's regularity.
- Still FAIL by the pre-registered bar. The gaps left are small and specific: the edit-type mix (edge, editfirst), the size of the vertical column effect, and the last few hundredths of a bit of word variety. None of this reads any text; it describes how regular the writing is.

## S6-P (cloud, 25 Nov 2026): onset-swap copies — FAIL 0/5 (`s6p/`)
- A rare habit of repeating the previous word with a new first glyph fixes the share of one-edit neighbours and moves editfirst part way. The word-boundary glyph dependency (edge: Voynich 0.19, all S6 models about 0.13) does not move, so it is not made by copying. It is now the main statistic left unmatched. Next: S6-Q, a junction preference.

## S6-Q (cloud, 25 Nov 2026): a word-junction preference closes the boundary gap — PASS 5/5 (`s6q/`)
- Preferring word pairs whose junction glyphs go together brings the word-boundary dependency into range on every seed. A table built from shuffled lines does not. The generator now matches 22–24 of the 24 statistics on held-out pages (all 24 on one seed), with the edit-type mix in range too.
- Left off: line-start lengthening (lost on 4/5 seeds), word variety H1 (0.01–0.1 bits high), the line-start link (3/5).
- Overall after tonight: one mechanical copy-and-vary procedure with a few local preferences reproduces nearly everything measured about the text's structure. That is strong evidence the structure needs no language. It does not prove the text is meaningless: a cipher or constructed language with the same local habits would score the same.

## S6-R (cloud, 25 Nov 2026): joint refit — strict all-targets FAIL 0/5 (`s6r/`)
- Fitting all preferences together trades targets instead of meeting all of them: line-start lengthening comes back on 3/5 seeds, while the boundary and line-start links fall to 3/5 and 2/5. One seed matches all 24 profile statistics. Word variety H1 misses by 0.002–0.16 bits on every seed.
- The family now sits at the edge of every window. The next informative test is generalisation to a different page split (S6-S), not more tuning.

## S6-S (cloud, 25 Nov 2026): the best generator does not carry over to the other half — FAIL 0/5 (`s6s/`)
- With FIT and TEST sheets swapped (private copies of all split-dependent references; the Voynich halves score 24/24 against each other both ways), the S6-Q generator with 15 stage parameters refit scores only 16–20/24 and fails the rule on every seed. It makes too few word types and loses the boundary-source ratio R (0.06–0.10 vs 0.35).
- The failures are in the base copy-and-vary layer, whose parameters were tuned on the original FIT half. The later mechanisms (line mode, junction preference, line-start lengthening) carry over.
- **Correction to how S6-Q should be read:** its 22–24/24 is split-dependent. "One mechanical procedure reproduces the measured structure" holds only for the half it was tuned on until a full refit on the other half (S6-S2) passes.

## M1b / PC bundle 7 (PC, 25 Nov 2026): Kraken line reader on held-out pages, **PASS** (`bundle7/PREREG.md`, `bundle7/RESULTS_SUMMARY.md`, `bundle7/results_full/`)
- **Setup:** Kraken 7.1.1 CTC line recognizer (about 4 M parameters) trained from scratch under WSL2 on the RTX 5060. Rows come from daniilvaino's centre-line traces (commit 28a4a7d) on the archive.org scans, paired with ZL3b-n P lines by width only. 2,306 training lines and 176 validation lines from the 139 train pages. The same 139/36 split as the VLM; 35 of the 36 test pages have traces. Pre-registered; no test-page text reached training (asserted in code).
- **Primary (page CER vs ZL, all rows read, greedy, no LM):** main model **0.111 [0.082, 0.143]**, against 0.607 for the Qwen2.5-VL-3B page reader. Three seeds: 0.111, 0.110, 0.110.
- **Controls:** reading scored against a different same-section test page is worse by **0.667 [0.602, 0.733]**. A model trained on shuffled labels scores 0.723, worse by **0.612 [0.575, 0.648]**. All three pass conditions are met.
- **Line CER** on 649 ZL-paired test lines: 0.073. This matches Lemur-Labs' unreleased 7.0%, and is optimistic in the same way theirs is, because ZL helped choose the lines. Against IT2a-n: page CER 0.113, line CER 0.074. Caveat: IT2a-n and ZL differ by only 0.020 page CER on these pages, so the IT check is only weakly independent of ZL.
- **Ablations (paired, vs main):** no augmentation is worse (+0.004 [0.002, 0.006]). Synthetic Eva-2-font pretraining (−0.003 [−0.006, −0.001]), ZL+IT labels (−0.003 [−0.006, −0.001]) and a 3-seed ensemble (−0.003 [−0.005, −0.002]) are each slightly better. All gains are under half a point. A 6-gram character LM in beam search (side test only) is **worse** (+0.009 [0.007, 0.012]). Best single number: ensemble 0.107.
- **Weakest pages:** f1v (0.39), f48v (0.33), f46v, f33v and f99v (about 0.26). Best: f19v, f32r and f115r (0.02–0.03). Much of the residual error is probably row grouping (extra or merged rows), not glyph reading. Untested.
- **Meaning:** we now have a reliable glyph reader trained on ZL conventions. It says nothing about what the text means. It makes possible a model-made transliteration of every page and per-glyph confidence, as a check on the human transliterations.


## S6-S2 (cloud, 25 Nov 2026): fully refit on the other half, the generator still fails — FAIL 0/5 (`s6s2/`)
- Refitting everything on the swapped fitting pages (S6-H base 3,900 trials, then 17 later parameters) gives 16–19/24 on the swapped test pages and fails the rule on every seed. The refit base fits its own pages (23/24) but not the other half (19/24); the boundary-source ratio R fails every time.
- **Revised overall reading:** the copy-and-vary generator family reproduces the measured structure when fitted on the original FIT half, but not when fitted on the other half. "A mechanical procedure explains the structure" is not established. This is not evidence for meaning; the best mechanical model is just not general enough. Next: S6-T (why one direction only; cross-validated tables).

## M1c / PC bundle 9 (PC, 25 Nov 2026): machine transliteration of every page (`bundle9/`, `bundle9/RESULTS_SUMMARY.md`, `bundle9/results_full/`)
- **What:** the bundle-7 3-seed Kraken ensemble (mean posteriors, greedy, no LM) read all traced images (226 of 227; f101v page image lost to a duplicate folio id). 4,590 rows. Combined IVTFF-like file `voynich_kraken_b9.txt` with `$K=train|val|test|unseen` per page and per-line confidence and 3-seed agreement; `voynich_kraken_b9_heldout.txt` has only pages never trained on.
- **New row grouping (v2, geometry only):** left-to-right mutual-best joins along the line slope. It was chosen by the pre-registered rule on validation pages (v2 − v1 −0.062 [−0.097, −0.030]). **Test-page CER 0.061 [0.048, 0.079]** (v1 0.107, which reproduces bundle 7 exactly). f1v 0.387 → 0.052, f48v 0.324 → 0.031. Row grouping, not glyph reading, was most of bundle 7's residual error.
- **Controls:** another page's reading scored against this page is worse by 0.697 [0.601, 0.802] on held-out pages. Confidence tracks error: Spearman −0.42 (3-seed agreement −0.60); line CER by confidence quartile 0.132 / 0.057 / 0.045 / 0.025.
- **Weak spot:** the 35 unseen pages score 0.386, driven by circular-text foldouts (f86v4 1.84, f67r1 1.69, f68r1 1.10 …), where top-to-bottom rows do not follow ZL's ring order. Ordinary held-out pages are fine.

## B9 recheck (cloud, 25 Nov 2026): key findings hold on the machine transliteration (`b9_recheck/`, pre-registered)
- **The line-start rule, the line-end rule and the 24-statistic profile are not artefacts of the scholarly transcriptions.** On 63 reader-held-out slots, E1, p/t/y/s/f starts, ysd, pagegal, E2, the ‑m lift and LE4 all come out at 0.8–1.2× ZL and far above the within-line shuffle null (p ≤ 0.005).
- **Profile:** 24/24 on TEST slots for machine text (paired rows and all rows). On reader-held-out slots, machine vs ZL agree on 24/24 (paired) and 23/24 (all rows; local repeats inflated by unfiltered short rows).
- **One pre-registered miss:** the ‑g line-end lift is 3.2× ZL, because mid-line ‑g is very rare in both (0.04% vs 0.08%). The line-final ‑g share is close (1.7% vs 2.1%).
- Caveat: the reader learned ZL's glyph conventions, so this rules out line-level transcription errors and choices, not EVA's segmentation itself.

## Bundle 10 (PC, 25 Nov 2026): ring-aware re-read of the circular pages; f101v both halves
Reader unchanged (bundle-7 Kraken ensemble). Only the geometry is new: circle fits find the diagram centres, ring pieces are read clockwise from ZL's start clock, and radials and labels are cut along their own lines. Scored against every ZL locus on the page. Primary metric is acer, an order-free CER using a one-to-one unit-locus matching. Baseline is bundle 9 v2, scored the same way.
- f67–f70, f86 (20 pages): acer 0.643 → 0.345 (−0.298 [−0.427, −0.168]); cer_all 0.535 → 0.336; ring loci 0.748 → 0.419. Shuffled control margin 0.821 [0.618, 1.083]. ADOPTED. Best pages: f67r1 0.093, f68v1 0.081, f69v 0.078, f70r2 0.079, f86v4 0.084.
- Extension f57v, f71–f73, f85r2 (12 pages): acer 0.867 → 0.550 (−0.317 [−0.451, −0.189]); shuffled margin 0.247 [0.102, 0.388]. ADOPTED. f71r 0.076.
- Ring counts match ZL on 18 of 26 ring pages. Caveat: the geometry constants were tuned with ZL ring counts in view, but not with the text.
- f101v: in bundle 9 the right-half photo overwrote the left half. Both halves are now joined into 10 lines (ZL has 10). Page CER 0.635 → 0.163; acer 0.875 → 0.182. Post-run fix, stated openly: the first run counted three joined labels as a paragraph row (CER 0.566). The paragraph block now starts after the largest vertical gap (geometry only).
- Worse or unsolved: f67r2 0.79 → 1.05 (curved paragraphs grouped as rings); f70r1 0.82 → 0.93; f57v has no usable traces; f72v1 and f72r3 have rings under-detected. Adoption was decided per set, so these pages are replaced too.
- Output: voynich_kraken_b10.txt (on the PC, bundle10\results_full\) is bundle 9 with 33 pages replaced, plus a held-out-only version.

## X1 (cloud, 25 Nov 2026): key findings hold on our own machine transliteration (`x1/`)
- On 33 held-out pages read by our Kraken model (bundle 9), the line-start → rest-of-line link, the word-boundary dependency, line-start lengthening and the vertical line-start effect all reproduce at 65–100% of their ZL size (all p ≤ 0.01). They are properties of the writing, not of ZL's page-level transcription choices (the reader still uses ZL's glyph alphabet).

## X2 (cloud, 25 Nov 2026): the full 24-statistic profile holds on the machine transliteration (`x2/`)
- On 33 held-out test pages all 24 statistics of the machine reading agree with ZL within 2 band sd. The scoring profile is robust to page-level transcription choices. (Unseen pages: profile not computable for either text.)

## X3 (cloud, 25 Nov 2026): the line-end glyph shift holds on the machine transliteration (`x3/`)
- On held-out test pages the machine reading gives E2 +0.082 and E2first +0.038 (ZL +0.083, +0.040), both above all 13 real manuscript sets. The Voynich-specific line-end marking is in the writing, not in ZL's transcription choices.

### Bundle 11 (B10a): ring geometry fixes on the weak circular pages: ADOPTED (25 Nov 2026, PC)
Same reader, geometry only, pre-registered (bundle11/PREREG.md on the PC). Mark-filter bug fixed: a ring's mean point is its centre, so every f57v ring had been dropped. The trace dataset's (daniilvaino's) two "key-like sequence" boxes still drop f57v R2/R4. Also new: per-ring models, merged nearby centres, wider outer rings, and sector stacks split into curved lines (P1). Ring counts match ZL on 19 of 26 pages (b10: 18).
Order-free CER on 32 diagram pages: 0.422 → 0.368, diff −0.054 [−0.113, −0.009]. Shuffled control 0.823 [0.563, 1.146]. Non-target pages unchanged (0.000 [−0.003, 0.003]). Targets: f70r1 0.93→0.29, f67r2 1.05→0.63, f57v 1.00→0.60, f72v1 0.80→0.57, f72r3 0.77→0.73. Worst change elsewhere: f72v3 0.61→0.64 (spurious 4th ring). Caveats: targets were picked from b10 scores, and constants were set with ZL ring counts in view. Output: voynich_kraken_b11.txt (PC).

### B10b: edge rules and profile rechecked on b10 (held-out, 63 slots): reproduced
The b9 recheck code was run unchanged. All units and P0-only both reproduce every rule except the ‑g lift (3.5/2.7, unstable). E1 1.08/1.13×, ptysf 1.05/1.07×, ysd 1.01×, pagegal 1.02/1.04×, E2 0.80/0.86×, ‑m lift 0.98/1.02×, LE4 1.09/1.24× ZL, all p = 0.005 vs within-line shuffle. Profile 24/24. Ring + radial text alone (835 words, descriptive): the start rules hold (E1 0.208 vs ZL 0.158), but no end rules (E2 p 0.22, ‑m lift 0.49× ZL, LE4 p 0.50). ZL's own ring loci do show end marking.

### B10c: does ring text behave like paragraph text? Mostly no (machine and ZL agree)
- R1, ring start marked: yes (E1 machine 0.219 vs 0.065 rotation null, ZL 0.174 vs 0.058, p 0.001). The machine start uses ZL's start clock, so it is not independent.
- R2, ring→ring word repeats: none (lift 1.05 [0.75, 1.36] machine, 1.02 ZL), vs 2.1 for paragraph line→line.
- R3, local repeats: not significant (1.25 p 0.15; 1.17 p 0.17).
- R4, composition: unlike paragraphs (JS 5–20× above the null) in both sources. Confounded with section, scribe and language.

## X4 (cloud, 25 Nov 2026): the A4 onset alternation holds on the machine transliteration (`x4/`)
- Currier B held-out test pages (17): machine A4 order-specific +0.0144 bits, p 0.0005; ZL +0.0158, p 0.0005. Same onset two words on: 16.6% vs 14.9% shuffled (ZL 16.4 vs 14.8). The alternation is in the writing, not a transcription habit.
- Not judged: Currier A test/unseen pages show A4 +0.013 to +0.029 in ZL (machine +0.016 to +0.028), against D2a's A ≈ −0.01. Small sets; "B only" is now "clear in B, uncertain in A" until X4b.
- **X4b (`x4/REPORT_b.md`):** on 10 random page splits Currier A does show A4 (median +0.015, 9/10 p < 0.05), so D2a's negative A value was a property of its one split. But with line-initial and line-final words dropped, A falls to +0.001 (0/10) while B stays at +0.009 (10/10). The mid-line onset alternation is Currier B only; A's signal is the line-edge rules (exploratory step, not pre-registered).

## M1k (cloud, 25 Nov 2026): the B9 line rules do not hang on the noisy machine lines (`m1k/`)
- Dropping the least-confident quarter of machine lines (by mean confidence or by 3-seed agreement) keeps every surviving line rule on reader-held-out slots; E1, ‑m lift and LE4 get slightly stronger. TEST-slot profile stays 24/24.
- Held-out profile machine vs ZL falls 24/23 → 22/21, almost all from R, which line deletion breaks by construction (fails the pre-registered "within 1").
- The ‑g lift "failure" is single-digit counts: mid-line ‑g 8 in 9.6k words (ZL) vs 1 in 6.7k (machine); line-final ‑g 1.9% vs 1.4%. No sign the reader over-reads final ‑g.

## S6-T (cloud, 25 Nov 2026): the generator's held-out pass does not transfer reliably to other splits (`s6t/`)
- S6-T-a: the original FIT/TEST split is typical of 200 random sheet splits on all 24 statistics.
- S6-T-b: the full S6-Q stack refitted on two new splits, both directions, scores 16–22/24 on TEST: FAIL by the old bands, but the real halves themselves score only 18–21 there.
- S6-T-c (split-independent bands, real halves 22–24): generalises on 3/6 directions (original, r0ab, r1ba; 20–23/24), fails on swapped, r0ba, r1ab (16–19/24). Rule needed 5/6: **FAIL**. Exactly one direction passes per split; not explained by half size or Currier B share. Misses rotate across many statistics. Always 5–12 statistics ahead of Timm + rules and shuffles, N2 everywhere.
- S6-T-d (exploratory): on its own FIT half the generator scores only 19–23 under the same bands, held-out 1–2 lower. **A fit ceiling (~20–21/24), not overfitting.** R (whole-word share of the junction link) is missed in 29/30 in-sample texts (real 0.30–0.35, generator 0.02–0.25) and M2 in 19/30.
- **Reading:** S6-Q's 5/5 PASS is real on its split but lucky. Describe the generator as "about 20 of 24 on any split". Its junction rule works on glyphs only; whole-word junction structure is missing.
- **S6-T-r (`s6t/rings/`, user question):** scoring on paragraph text only (scholarly ZL, labels already excluded; ring + radial ≈ 6% of running text) changes the generator by +0.6 statistics vs +1.3 for controls; passing directions stay 3/6. Non-paragraph share per half (2.4–10.9%) does not track pass/fail. R stays missed. Ring text is not what holds the generator back (pre-registered verdict MIXED, leaning no).

### Bundle 12: f57v's "key-like" rings read: ADOPTED (25 Nov 2026, PC)
The trace dataset (daniilvaino/VoynichManuscriptOCR, data/marks/114_0_f57v.json) boxes f57v rings R2 and R4 as "alphabet_column / key-like sequence"; bundles 9–11 dropped them. Bundle 12 ignores alphabet_column boxes centred on a ring (pre-registered, bundle12/PREREG.md on PC). f57v now 13 units (4 rings, 4 radials, 5 labels; matches ZL). f57v acer 0.596 → 0.386; best other page vs f57v ZL 0.790 (rank p 1/32); other 31 pages unchanged. voynich_kraken_b12.txt is now the current machine transliteration. Reader cannot output R2's rare glyphs (@169–@172, I), so machine R2 is garbled.

### B11g: is f57v R2 (or R4) a key? No support beyond list-like form
Key = ZL f57v.3 (R2): 72 symbols, 18 distinct, a 17-symbol sequence written 4 times. Test text: ZL P lines on held-out pages (1,268) and machine text (1,393).
- K1 list-like: yes for R2 (one-glyph words 0.94, 1st of 72 rings; periodicity 0.96, next 0.62, shuffle 0.13, p 0.001). R4 not (0.15, rank 66).
- K2 coverage: no. 0.560 vs random 12-letter sets 0.479 (q99 0.709, p 0.21); omits e,a,i,n,s,h. Machine p 0.41.
- K3 order structure: no. Mean key distance 5.07 vs random 4.67 (p 0.68); machine p 0.67.
- K4 periodic substitution key vs 1,000 random keys: no. Bigram cond. entropy 2.147 raw, 2.395 R2, best shift 2.362, random 2.445 (q01 2.211), p 0.32; machine p 0.34.
Answer: R2 is the most list-like ring, but not a script inventory, order is irrelevant, and as a substitution key it is no better than random. Non-alphabetic keys (numeral, calendar, nomenclator) untested.

## P4-S-b (PC, 25 Nov 2026): ink-tone steps with Kraken-bundle lines — CUT ACROSS ENTRIES (weak; detector misses f115r) (files on PC: Voynich\p4sb\)
- Line source swapped to bundle 9 v2 rows (Kraken rows paired to ZL loci), cut from archive.org scans; detector and tests unchanged from P4-S-a, plus a lighting control (paper-grey steps) and a circular-shift control. 225 images, 3,809 paired rows; 115 pages pass the gate (P4-S-a: 13).
- 8 pages have a step (7%; ~1.2 expected by chance): f107v/33, f14r/6, f24r/15, f37v/5, f42r/5, f88r/26, f88v/20, f99v/22. T1: 1/8 at a paragraph start (f88v), expected 0.17, p = 1.0 → CUT ACROSS ENTRIES (exactly the pre-set 8-step minimum); circular-shift control agrees (0.12 vs 99th pct 0.50). One step (f24r) coincides with a paper-brightness step. T2: 7/61 Currier A pages vs 1/53 B (7 of 8 in Scribe 1). T3 (exploratory): text doesn't change across a step (JS 0.878 vs 0.873, p 0.84).
- Calibration fails: f115r's maximum is at the right boundary (after line 17, tone ≈115 → ≈72) but |d| 5.6 vs page threshold 17.1; the within-page permutation null is too wide for long blocks, so the detector under-counts long-block session changes. f103r outside the gate.
- Meaning: the steps fall mid-paragraph, consistent with continuous copying with breaks anywhere, not one entry per session. Weak. No claim about meaning.

## P4-S-c (PC, 25 Nov 2026): long-block changepoint on P4-S-b tones — CUT ACROSS ENTRIES, calibration passes (PC: Voynich\p4sb\PREREG_c.md, REPORT.md)
- Best whole-page split (Welch t), 3-line block-permutation null; same 115 pages. Calibration passes: f115r after line 17 (|t| 24.8 vs threshold 11.0).
- 11 pages change: f104v/14 (para start), f105v/18, f115r/17, f49r/7, f58v/15, f76r/52, f76v/26, f78r/34, f78v/19 (para start; also paper-brightness change), f81v/10, f86v5/10. T1: 2/11 at paragraph starts, expected 0.14, p = 0.96 → CUT ACROSS ENTRIES; circular-shift control agrees.
- Gradient control: 8/11 fit a page-long drift nearly as well as a step; only 3 clean steps (f104v/14 para start, f115r/17, f76v/26). T2: 9/53 B vs 2/61 A, opposite of P4-S-b (7/8 A); the two detectors pick almost disjoint pages, so page lists are not stable. T3: no text change across a change (p 0.58).
- With P4-S-b: ink-tone changes are rare, mostly gradual, mid-paragraph about as often as chance; no sign of sessions starting at entries. Favours continuous copying with occasional breaks; thin evidence. No claim about meaning.

## S6-V (cloud, 25 Nov 2026): a word-level junction rule fixes R but the generator still fails the any-split rule (`s6v/`)
- New terms in the junction step: whole previous word → next onset (bW) and junction glyphs → rest of next word (bR). Refitted on all 6 split directions, scored with split-independent bands.
- **FAIL, 4/6 directions** (rule 5/6; S6-T-c was 3/6). Mean TEST 20.3/24 (was 19.4), in-sample 21.5 (was 20.6). R missed in 10/30 TEST texts (was 22/30), mostly overshoots on the original split.
- Remaining gaps over 30 texts: S4_zipf 20, M2 14, S10_immrep 13, S3_sdlen 13. Whole-word junction structure is a real missing piece of the generator, not the only one.

## S11-D pace (cloud, 25 Nov 2026): the down-page drift is not a line-length effect (`s11d_pace/`)
- Pre-registered. With line length (glyphs per line) added to the S11-E regression, the page drift of the composite (l + a − d − q − t) stays at p 0.002 / 0.003 on FIT / TEST (b_page +0.160 / +0.111, vs +0.164 / +0.129 without length).
- The length verdict is **void**, because calibration failed: unplanted hybrid text has the same length link. Voynich b_len (−0.21 / −0.15) is inside the range of 10 hybrid seeds (−0.24..−0.09). Short lines shift the glyph mix mechanically, so this is not evidence of pace.
- Spacing and ink speed are still untested, because the image measures are blind (H10d).

## N7 (cloud, 25 Nov 2026): words are not a few independent choices (dice, geomancy, cards) — **FAIL** (`n7_divination/`)
- Pre-registered. Held-out bits per TEST token: a glyph trigram beats the best independent-slot model (k = 2–4 contiguous pieces, latent split, EM) by **0.89 bits** on the Voynich. The Timm generator gives the same gap (0.88), while the positive controls (4-throw dice text; text sampled from a Voynich-fitted 3-slot model) favour the slot model (+0.11 / +0.27). Latin, Italian and German favour the slot model by +0.8 to +1.4 bits (stem + ending).
- So Voynich words do not factor into independent pieces. Their inner structure behaves like a glyph-to-glyph procedure (as with Timm). Outcomes spelled out through a glyph chain cannot be told apart from any other glyph procedure.

## N4 (cloud, 25 Nov 2026): a medieval synonym glossary (*Alphita*, *Sinonoma Bartholomei*) — **FAIL** (`n4_alphita/`)
- Pre-registered. Mowat's editions (archive.org OCR, glossary body only). *Alphita*: 4/24 profile matches, boundary triplet fails (edge 0.051, lastlast 0.090, R 5.85 vs 0.19 / 0.007 / 0.32). *Alphita* + *Sinonoma* at Voynich TEST size: 4/24, R 5.51. Word-shuffled *Alphita*: 4/24. Latin Pliny: 3/24. A glossary is ordinary Latin on these statistics. Its formulae ("i.", "idem", "respice in") raise edge and word order slightly, but the boundary link stays word-driven, as with the recipe books.

## C4 (cloud, 25 Nov 2026): recipe formulae vs the boundary contrasts — **separation holds** (`c4_recipes/`)
- Pre-registered, ~5k-token chunks. Six recipe books (four Italian, Bavarian *Arzneibücher*, *Buoch von guoter spise*) give 13 chunks. On edge, 4 of 13 fall inside the Voynich chunk range (0.154–0.253). On R (Voynich −0.10–0.21, recipes 2.9–6.8), lastlast (0.003–0.016 vs 0.091–0.178) and word200, none do (0/13). Even the recipe chunks with the highest edge have R ≥ 2.9. Edge alone cannot rule out a formulaic recipe text, but R and lastlast can, even on short passages.

## M1d (cloud, 25 Nov 2026): ZL vs IT disagreements on held-out pages — **mixed, the reader backs neither** (`m1d_zl_it/`)
- Pre-registered. Bundle 9 v2 readings, 666 test-page lines. In glyph disagreements the reader backs ZL 55% [49, 61], the same as an image-free ZL text prior (55%). The shuffled-row control gives 46%. On train pages it backs ZL 86% (memorised labels). Word-space disagreements: 49%.
- Exploratory by type: *r*/*s* and *ch*/*ee* go to ZL, but the text prior does the same (convention). **Extra *i* in ZL (aiiin vs aiin): the reader backs IT 12/3 against a neutral prior** (p ≈ 0.035 uncorrected). *a*/*o* is split, a genuine ambiguity in the ink. Overall, the reader cannot arbitrate between the transcriptions at CER 0.06. A posterior-level check needs M1g.

## S11-G (cloud, 25 Nov 2026): drift by page height vs writing order — **not testable** (`s11g/`)
- Pre-registered. Using bundle 9 row heights (162 pages, 3,259 lines), line order and height correlate at ρ 0.987, and still at 0.95–0.98 on pages with large gaps around drawings. Calibration failed: a planted height drift was not recovered (p 0.15). The Voynich result is unresolved (p 0.09–0.74). Paragraph text cannot separate the two readings.

## N7b (cloud, 25 Nov 2026): the S6 generators miss the slot-vs-glyph gap — **FAIL** (`n7b/`)
- Pre-registered. N7's Δ = H(glyph trigram) − H(best k-slot model): Voynich TEST −0.889, band ±0.072. The swapped halves give −0.857, inside the band. S6-Q gives −0.48 to −0.62 over 5 seeds, and S6-J/L/N/O2/P give −0.42 to −0.68: all outside, too slot-like. The Timm generator gives −0.88, inside (**corrected by N7d:** that Timm text used a different split; on the project split Timm is also out). Their copy-and-edit word building splices word parts more freely than Voynich glyphs combine. **Proposed statistic 25** for the target profile, and a new target for the generator thread.

## f57v R2 follow-up (cloud, 25 Nov 2026): rare glyphs and the cycle's placement (`f57v_r2/`)
- **@169–@172 occur only on f57v** (4× each in R2; @170/@171 once in R4, @172 once in R3) **and in the f66r single-glyph column** (@169, @172). They never appear in paragraph text. EVA v is also nearly f57v-only (14/15; once on f3r). The end of the f66r column shares R2's order weakly (pairs f→@169 and c→@172; LCS p 0.036, pair count p 0.084 vs shuffles).
- **Placement (image unwrap):** R2 = 4 repeats of 18 symbols, starting at about 308°, 48°, 137° and 220°, one per quadrant. The first starts at the ring's start mark (vertical stroke, outer word *dairal*). The four figures sit near 11°, 95°, 180° and 275°, so the repeats start **between** the figures, not at them (one phase, not significant). The f→p variant splits the repeats 2 + 2. So the quartering sets the number of repeats, but the cycle is not keyed to the figures. Numeral and calendar readings remain untested.

## S6-W (cloud, 25 Nov 2026): boosting the commonest words does not help (`s6w/`)
- A pre-registered frequency-boost term (pZ, gZ) on top of S6-V, with the same 6-direction check: **FAIL, 3/6** (S6-V 4/6). Mean TEST 20.2, against 20.3 for S6-V. The fit chose pZ of 0 to 0.03 and S4_zipf misses fell only from 20 to 17 of 30. S6-V stays the best generator. The shallow slope likely comes from word formation (too many rare new types), which fits N7b's finding that S6-Q's words split too freely (slot-vs-glyph Δ −0.48 to −0.62 against Voynich −0.89).

## F57-a (cloud, 25 Nov 2026): f66r/f49v letter columns vs the f57v rings — **no shared order** (`f57a/`)
- Pre-registered. 7 pairs × 2 statistics (LCS and shared adjacent pairs) against order shuffles: none passes p < 0.0036, and the smallest p is 0.093 (f49v–R2 LCS). The lists share symbols but not sequences. f49v carries its own small repeat ("p o @192 y e @140" twice). There is no evidence of one key list copied across pages. The f66r–R2 hint (p 0.036) is not confirmed.

## B11a (cloud, 25 Nov 2026): ring vs paragraph text with the page held fixed — **real but small** (`b11a/`)
- Pre-registered. On 7 pages with both, ring and paragraph glyph distributions differ beyond a within-page line-permutation null: JS 0.043 vs 0.021, p 0.0005. Word-final glyph gives 1.6×, p 0.001. Currier B pages alone give 2.3×. The effect is about 2× the null, against 5–20× in B10c R4, so most of that difference was section, scribe and language. It is carried by f70r2 and f86v4; the other pages are not significant on their own.
- **B11h (pre-registered): not a line-position effect.** Dropping the first and last word of every locus leaves glyph JS at 1.8× the null (p 0.0005). Rings have less *l*, *sh* and *q* and more *d*, *t* and *r* than their own page's paragraphs.

## S11-F page part (cloud, 25 Nov 2026): the drift starts afresh on each page, no carry-over (`s11f/`)
- Pre-registered. Bottom-of-page composite does not predict the next page's top beyond page means (r −0.04, p 0.49 vs random same-section successors; r→v and v→r both n.s.). Exploratory: the composite drops 0.043 from page bottom to the next page top, equal to the average within-page rise (69% of 182 pairs drop, t −4.7). The pre-registered reset test was mis-specified, because its null also resets. So the drift is a per-page phenomenon: it runs on across paragraphs inside a page (S11-E) and restarts at each page.

## N7c (cloud, 25 Nov 2026): slot-vs-glyph gap by Currier language — **B is more slot-like than A** (`n7c/`)
- Pre-registered. Δ is strongly size-dependent (−0.89 on the full text, −1.4 to −1.9 on 2–6k-token subsets), so subsets are compared with size-matched random page sets. Currier B −1.00 ± 0.10 vs size-matched −1.13 (range −1.18..−1.08): more slot-like. Bio −1.40 vs −1.90: more slot-like. Currier A −1.61 ± 0.20, at the glyph-dependent end of its size range (−1.61..−1.33). Herbal and stars are typical. A and B intervals do not overlap. B words recombine parts more freely (the *qo-*/*-edy* system), and A words are tighter glyph chains. A per-language Δ target would be fairer for the generators.

## S11-I (cloud, 25 Nov 2026): the per-page drift is uniform across pages, hands and languages (`s11i/`)
- Pre-registered, 183 pages, mean within-page ρ +0.165. The drift does not depend on lines per page (ρ 0.00; total rise ρ +0.06), paragraph count (p 0.12–0.18), Currier language (p 0.64), Davis hand (p 0.88) or section (p 0.58). With S11-E and S11-F: a page-relative effect, the same for every scribe, spanning the page whatever its length. A tiring hand or a scribe habit would grow with page length and differ by scribe, and it does neither.

## S11-J (cloud, 25 Nov 2026): no generator shows the page-relative drift — **FAIL** (`s11j/`)
- Pre-registered. Voynich within-page drift ρ +0.165 [0.121, 0.211]. S6-Q (5 seeds) −0.013..+0.016, S6-L +0.017, S6-O2 +0.041, Timm + rules +0.020..+0.047: all outside. The page drift is an ingredient missing from every generator: it needs settings that shift down each page and reset at the next.

## D4-V (cloud, 25 Nov 2026): Bax-style plant names with verified Arabic names — **FAIL** (`d4v/`)
- Pre-registered. Leclerc's Ibn al-Baytar (tome 1, archive.org) verifies 14 of D4's Arabic plant names (headword + French gloss match), on 13 herbal pages off Bax's leaves. Bax's key: true-name rank 0.523 vs null 0.512 ± 0.050, p 0.60, no better than Timm (0.504) or glyph-shuffled (0.500). Leclerc's spelling alone: p 0.63. So D4's failure is not down to the memory-written name lists. Limits: only tome 1 is online, so 14/76 genera; the Wellmann Greek OCR is unusable; 13 pages give low power.

## P5 text proxy (cloud, 25 Nov 2026): ZL-flagged corrections (`p5/`) — **inconclusive**
- Pre-registered. The 19 words ZL flags as corrected are rarer than random same-page, same-length words (log frequency 1.69 vs 3.09, p 0.0004; attested 58% vs 78%) and lean line-final (32% vs 13%, p 0.03). This is the opposite of correcting toward ordinary words. But an overwritten spot is naturally transcribed as an odd word, so the proxy cannot tell the scribe's intent from reading damage. The image-based erasure search was not done (too large; multispectral images are better).

## C6 (cloud, 25 Nov 2026): RIDGES diplomatic vs normalised vs lemma — spelling variation does not make near-copies (`c6/`)
- Pre-registered. The same 72k tokens of 1482–1588 German herbals in three versions. Diplomatic spelling raises near-copies only from 1.00 (normalised) to 1.05 (Voynich 1.49), and nearadj stays at 0.004 in all versions (Voynich 0.047, 10×). Variant spellings scatter across the text and differ mid-word (editfirst 0.37 vs Voynich 0.58). Voynich near-copies sit next to each other and differ at the first glyph. Inconsistent spelling does not explain the Voynich's near-copy structure. The boundary statistics are unchanged (R 5–6).

**B11c (PC, 25 Nov, Voynich\b11c_m1di\, PASS: ring starts are marked without ZL's clock).** Bundle-12 ring geometry, each ring started at the midpoint of its largest gap, no ZL clock (grouping reproduced bundle 12 on all 32 pages, 75 rings). Held-out 63 rings: E1 0.215 vs rotation null 0.060, p 0.001; p/t/y/s/f first word 0.41 vs 0.11 (ZL-clock start: E1 0.219, 0.43). Placebo (random other gap ≥ 1 x-height, 20 draws): E1 median 0.117, p < 0.01 in 55% of draws, so gaps are text breaks in general and the largest is strongest. Largest-gap start within 45° of ZL's on 50% of rings (random angle 25%, random gap 20%). Gallows not used (circular). B10c "ring start is special" does not depend on ZL's start.

**M1d-i (PC, 25 Nov, Voynich\b11c_m1di\, negative: no i-specific over-count).** 1,844 rows (993 held-out). Whole-line CTC likelihood with each run one stroke shorter/longer. Held-out runs n ≥ 2: i prefers-fewer 0.044, prefers-more 0.005, D 0.039 [0.026, 0.052]; control e D 0.078 [0.060, 0.097]; D_i − D_e −0.039 [−0.061, −0.017], so the over-count rule fails. Placebo (another row's posteriors): 77% prefer fewer, so the real 4% follows the ink. Lean is in long runs: iii 26% (57), eee 33% (99); ii 3%, ee 6%. Where IT has one i fewer than ZL, reader prefers fewer on 68% [55, 79] of 53 runs, but e behaves the same (50% [34, 66], n 36). Image stroke counter failed its calibration gate, so stroke check inconclusive. Net: some ZL aiiin may be aiin, but it's a general long-run effect, not an i problem.

## S-long-runs (cloud, 25 Nov 2026): profile robust to ZL's i/e stroke counts (`longruns/`)
- Pre-registered. Merging *iii*+→*ii* and *eee*+→*ee* (1.5% of TEST tokens) moves no statistic by more than 1 band-sd (max S6 +0.51), and all 24 stay in band. Collapsing every *i*-run (*ii*→*i*, 12.6% of tokens) moves only word order (+2.3 sd) and Zipf (−1.1). A possible ZL over-count of long runs (M1d) does not affect the profile-based conclusions.

## N5 (cloud, 25 Nov 2026): duplicated passages across sheets (garbled exemplar copy) — **FAIL** (`n5/`)
- Pre-registered. No exact cross-sheet duplicate of ≥ 4 words (0; generators 2–3). Near runs ≥ 4 words (each word within 1 edit): Voynich 71, page-shuffled max 27, Timm 29–84, S6-Q 39. Above the shuffle, but within generator range. The differences are mostly insertions/deletions and family alternations (*ch/sh*, *l/r*, *k/t*), not visual-confusion copyist slips. There is no sign of a copied exemplar, which agrees with S10.

**B11h-gaps (PC, 25 Nov, Voynich\b11c_m1di\, negative).** Inner ring gaps (≥ 1 x-height, not the largest): 300 located. First glyph vs the ring's no-gap words, within-ring position-permutation null. Held-out (51 rings, 255 words): E1-gap 0.028 vs null 0.021, p 0.12; p/t/y/s/f 0.08 after gap vs 0.09 elsewhere; by width 1–2 x-h p 0.08, >2 p 0.12. All pages p 0.013. Words after inner gaps are not start-marked.
**Strip-start reading artefact (PC, exploratory).** The same ring word is read differently at a strip start vs mid-strip (132/300 differ); at strip start it opens with p/t/y/s/f 25% vs 9% mid-strip (okeodal→keodal, am→pam, kakar→teekar). The reader has learned a line-start prior.
**B11c CORRECTED:** with each ring's first word read mid-strip, held-out start marking on the same 48 rings drops from E1 0.215 (p 0.001) to 0.121 (null 0.071, p 0.016), p/t/y/s/f 0.42 → 0.21 (null 0.10, p 0.022). About half the machine ring-start marking in B11c and B10c's machine R1 is reader artefact; the rest is weak. Reader-independent results stand: largest gap near ZL's start (50% within 45° vs 25%), and ZL's own ring loci have a marked start (B10c). Machine B10b ring-start p/t/y/s/f (0.39 vs ZL 0.20) is largely this artefact.

## P5-b (cloud, 25 Nov 2026): the ZL "corr?" spots by eye (`p5b/`) — descriptive, originals unreadable
- 15 of 20 flagged spots cropped from the Yale images. 3 show a dense ink blob over one glyph (f1v.7, f19r.2, f39r.12), 3 a glyph retraced in heavier ink (f50v.8, f87r.7, probably f107v.44), 2 stains, and 7 show nothing at this resolution. No original glyph is readable under any correction, so what was corrected cannot be coded. The blobs explain why ZL reads some corrected spots as rare glyphs or words (e.g. @242 on f19r), and so why the P5 text proxy is confounded. This needs multispectral images.

## D9b (cloud, 25 Nov 2026): one glyph rewrite between section vocabularies — **FAIL** (`d9b/`)
- Pre-registered. The best permutation of the top 20 glyphs mapping bio or stars vocabulary onto herbal-B is the identity (held-out gain 0.000; shuffled-label max +0.002; Timm 0.000). 74% / 63% of held-out tokens are already herbal-B words as written. Sections share words directly and differ in word frequency, not spelling. There is no per-section glyph cipher (one-to-one; many-to-one rewrites not tested).

## D9c (cloud, 26 Nov 2026): section glyph shifts are frequency changes, not swaps (`d9c/`)
- Pre-registered, sheet-grouped null. Bio vs herbal-B: *q* up (+0.90 log), *m* and *f* down (−1.33, −1.53). Stars vs herbal-B: *q* up (+0.47), *f* down (−1.06). Replacing the risen glyph by a fallen one inside words gives attested herbal-B words 0.000–0.001 of the time (random pairs 0.66–0.75). So these are independent frequency shifts (more *qo-* words, fewer *f*-gallows and *-m*), not section-specific spellings.

## N7d (cloud, 26 Nov 2026): generators too slot-like in both Currier A and B (`n7d/`)
- Pre-registered. Δ per language on matched slots: Voynich A −1.61 ± 0.20, B −1.00 ± 0.10. S6-Q (3 seeds): A −1.24..−1.31, B −0.79..−0.84, out in both. Timm + rules seed 21: A −1.10, B −0.69, out. **Correction to N7/N7b:** Timm's in-band pooled value came from a different text and split (`decipherment_harness/timm_pages.json`, first 19k tokens). On the project split Timm is also too slot-like. The direction (A more chained than B) is reproduced; the level is not.

**M1h (PC, 25 Nov, Voynich\b11c_m1di\, paragraph line-start claim stands; context method failed).** 1,033 held-out paragraph rows, each read normally (N), after 6 x-heights of the previous row's ink (C), and after 6 x-heights of blank paper (B). First-word error vs ZL: N 0.092, C 0.277, B 0.134. p/t/y/s/f first word: ZL 0.447, N 0.455, C 0.403, B 0.272. E1: ZL 0.206; N 0.206 (ratio 1.00); C 0.182; B 0.085. The pre-registered "weakens" rule is technically met (C < N), but the context reads are much less like ZL (ink leaks across the cut), so the drop measures damage done by the context. Reader-independent evidence: normal machine first words match ZL on held-out paragraph lines (0.455 vs 0.447, E1 ratio 1.00). The start prior misleads only on non-line-start text such as rings (B11h). Machine line-start rules (bundle-9 recheck / M1e, B10b B-all/B-para) stand.

**B11i (PC, 25 Nov, Voynich\b11c_m1di\, mixed: ring start marked; its p/t/y/s/f excess is a reader artefact).** Bundle-12 ring and radial units, ZL-clock start, read normally (N), after 6 x-heights of context (C), and after blank paper (B). Held-out: 143 units (63 rings). Ring R1 E1 vs rotation: N 0.217 (p 0.001), C 0.132 (null 0.059, p 0.002), B 0.104 (p 0.013). Ring + radial p/t/y/s/f start share: N 0.42 (2.33× ZL), C 0.25 (1.39×), B 0.17 (0.94×); ZL C+R loci on the same pages: E1 0.158, p/t/y/s/f 0.18. Ring-start marking survives the artefact; B10b's p/t/y/s/f excess over ZL is explained by it. Caveat (M1h): context can damage first words; ZL is the anchor. Net: ring starts marked at about E1 0.13–0.16, p/t/y/s/f about 0.2 (ZL level); machine 0.4 figures in B10b/B10c/uncorrected B11c overstated it.

**M1d-b (PC, 25 Nov, Voynich\b11c_m1di\, neither: ZL and IT fit the ink equally where they disagree).** 984 held-out lines, 966 ZL/IT disagreement windows, whole-line CTC likelihood ZL vs ZL-with-IT. Glyph windows (613) ZL share: twolab reader (ZL + IT) 0.542 [0.498, 0.583]; main reader (ZL only) 0.537 [0.493, 0.577]; placebo 0.475. Space windows (353): twolab 0.467 [0.412, 0.523]; main 0.550 [0.499, 0.603]; placebo 0.416. twolab − main: glyphs +0.005 [−0.020, +0.029]; spaces −0.082 [−0.132, −0.036]. The main reader has no ZL glyph bias but learned ZL's word spacing; M1d's space figure is partly that. Descriptive (twolab ZL/IT): ZL a vs IT o 36/52, ZL o vs IT a 25/11 (ink favours o both ways); ZL r vs IT s 25/9; ZL extra i 12/29 (favours IT, shared with e); ZL ee vs IT ch 13/5.

## S6-X (cloud, 26 Nov 2026): glyph-built new words don't close the slot-vs-glyph gap (`s6x/`)
- Pre-registered: S6-V + glyph-3-gram new words (pG3), copying free (pc, pw), Δ term in the objective, 6 directions. **FAIL**: 4/6 directions, as S6-V (mean TEST 20.1). Δ in range on 0/6 (generator −0.38 to −0.91 against real −1.03 to −1.26). The fit keeps pG3 at 0–0.10 and copying high. In the probe Δ reached the real value only with copying cut hard, at about −6 statistics. Δ and the page-level copy statistics pull against each other in S6; copies need to respect glyph-to-glyph structure.

## S6-Y (cloud, 26 Nov 2026): a page-position term reproduces the page drift on every split (`s6y/`)
- Pre-registered: S6-V + bD (word choice nudged towards l/a and away from d/q/t as the page fills; resets each page), drift term in the objective, 6 directions.
- **Secondary PASS:** TEST page drift is within ±0.06 of the real half on 6/6 directions. The generator gives +0.11 to +0.27 against real +0.14 to +0.19. S6-V gave about 0.00, and bD fitted at 1.7–3.3.
- **Main FAIL:** 3/6 directions on the 24 statistics (S6-V 4/6), mean TEST 20.0. Remaining gaps unchanged (S4_zipf, S3_sdlen, M2, S10_immrep).
- A simple page-position preference is enough to produce the S11 drift. S6-Y is the new reference generator, with the drift as statistic 26 and Δ as 25.

## S6-X3 (cloud, 26 Nov 2026): a never-recopied rare-word stream is rejected by the fit (`s6x3/`)
- Pre-registered: S6-Y + glyph-3-gram rare words not re-copied on the page. In the probe this matched Δ (−1.27 vs −1.26) and the hapax share (0.19 vs 0.18) at a cost of 4 statistics. With Δ and drift in the objective, 6 directions: **FAIL, 2/6**. Four searches kept pG3 = 0 (the S6-Y setting), and two used 4–8% and got worse.
- Three word-formation attempts (S6-X, X2, X3) now agree: in S6, raising Δ and the hapax share costs word-length and repetition statistics. Parked. Possible next step: rare words made by length-preserving glyph-probable edits of common words.

## B11a (cloud, 26 Nov 2026, ZL only): ring text matches paragraph text on the same page (`b11a/`)
- Pre-registered. On the 7 pages with both, ring vs paragraph JS for glyphs, onsets and endings is at the within-page line-shuffle null (ratios 0.92–1.21, p 0.17–0.59; 781 ring words). B10c's ring-vs-paragraph difference comes from the pages rings sit on (zodiac/cosmological), not from ring text itself. Ring text needs no separate generator component. Modest power; the A/B part was not possible (Currier unassigned on ring pages).

## Generator gap diagnosis (cloud, 26 Nov 2026, exploratory with controls): why S6-Y misses what it misses (`GENERATOR_GAPS.md`, `gapdiag/`)
- **One setting vs several scribes.** Across hands 1–3 (~11k words each), the real text's spread exceeds 40 random page regroupings (p95) on 11/24 statistics (S1, S2, S5, S6, S7, E1, E2, E3, edge, word200, nearadj; e.g. E1 0.87 band vs control median 0.15). S6-Y's spread sits at or below the control (E1 0.03–0.14, M2 0.06–0.09). Across 6 directions S6-Y follows 8% of real FIT–TEST differences (pooled slope 0.08) (`g2.out`, `g1.out`).
- **Systematic in-sample biases (same sign on 6/6 directions):** S4_zipf +0.98 band (too flat), M2 −1.00, S10_immrep +0.59, S5_types −0.55, E2 −0.52, S2 +0.60, lastlast −0.65, ff −0.39. S3_sdlen has no consistent bias. Its error is a fit instability (swapped direction −3.3 band in-sample).
- **M2 (ending → next ending) is not a line-edge or copying effect:** whole-text real 0.0043 → 0.0041 with line edges dropped, 0.0041 with adjacent near-copies removed (page-shuffle 0.0000). It triples from hand 1 (0.0034) to hand 3 (0.0107), while S6-Y stays at ~0.002 for every hand. The preferences are directional (hand 3: -in→-al 1.45×, -al→-in 0.80×).
- **One-off words are not local edits in the real text:** hapax share 0.138 vs S6-Y 0.077. One edit from a word in the previous 40: real 0.083 (random-page 0.029), S6-Y 0.23 (0.046). One edit from a frequent word: real 0.36, S6-Y 0.45. Lengths match (6.75 vs 6.8). A two-common-words join test is uninformative (0.38 vs 0.33). This counts against S6-X4 as stated.
- Reading: the misses come from (A) scribe/section mixture and (B) novelty made by recycling recent words instead of fresh word building, plus (C) a per-hand directional ending order. Realistic next fixes F1 (per-hand settings), F2 (new words from hand-level parts), F3 (per-hand ending-order table). Full 24/24 is judged not realistic.

## GG-3 (cloud, 26 Nov 2026): the ending-order preference follows the Currier language, not the scribe (`s6z/gg3/`)
- Pre-registered. Directional asymmetry of adjacent ending pairs (top 15), correlated between half-hands (200 halvings). Within hand: ρ 0.44 / 0.63 / 0.53 (hands 1/2/3). Between: 1–2 **0.08** (inside shuffle range), 1–3 0.19, 2–3 **0.49**. Ratio to within: 0.15, 0.39, **0.84**. Rule verdict: mixed. Hands 2 and 3 (both B) share the order; hand 1 (A) does not share it with either.
- The distance-2 (line-position) part is shared by all hands (ρ 0.36–0.42). S6-Y matches the whole-text asymmetries (ρ 0.63–0.71) but not per-hand ones (0.26–0.47).
- Reading: a per-language habit (A vs B), not one book-wide grammar and not per scribe. It does not separate B grammar from a B writing procedure. F3 will use one table per language with per-hand strength.

## D7 (cloud, 26 Nov 2026): the margin glyph columns are not a key (`d7/`)
- Pre-registered. f49v (26 glyphs, one per line), f76r (9, "sdqsolkrs"), f66r (34). Margin glyph = next line's first glyph: f49v 1 vs 0.97 expected (p 0.65), f76r 1 vs 0.88 (p 0.62); in the first word p 0.35 / 0.78. Shared bigrams with the f57v ring: 0 / 1 / 2 (p ≥ 0.22). Glyph variety equals random page-glyph draws (p 0.06–0.59), so not alphabet lists.
- **Only structure:** the f49v column repeats `p o @192 y e @140` twice and `y e @140` three times (p 0.0001 vs shuffles), not aligned with paragraph breaks. Looks like counting or ordinal marks; it gives no reading. In the Yale image the column is in text-like ink close to the line starts; the "1–5" beside paragraph 1 is a paler addition.
- f1r margin letters need the MSI images (PC fetch); star labels and month names have no pairing to test.

## P4-D (cloud, 26 Nov 2026): the per-page text drift has no ink or pen counterpart (`p4d/`)
- Pre-registered. Bundle 9 Kraken rows on Yale JPEGs, 139 pages / 2,895 rows. Measure check: f115r 17/18 tone step seen (t 36). McCrone "low iron" f78r has the highest photo contrast of the 3 sampled pages, so contrast is not ink chemistry.
- Down the page the composite rises (r 0.18) but ink contrast (r −0.06) and pen width (r 0.03) don't. Q1 within-page, position removed: contrast r 0.046 (p 0.014, passes); pen width p 0.78. **Exploratory split-row check:** ink from one half, text from the other: r 0.002 (p 0.87) vs 0.051 same half, closer to a glyph-mix artefact (some glyphs ink darker) than to a shared ink state, though low power. Q2 page sessions vs text: FAIL (p 0.60 / 0.10).
- Reading: S11's per-page drift is not an ink-load or pen-wear effect visible in the photos. A clean per-glyph version waits for the letter boxes (P4-D-b).

## D8 (cloud, 26 Nov 2026): zodiac labels are not degree names with planetary rulers (`d8/`)
- Pre-registered. Do labels of degrees with the same ruler look more alike? Egyptian terms, Chaldean decans (cross-sign pairs, segment rulers permuted within sign) and a scheme-free 7-planet degree cycle (distance 7/14/21 vs neighbours). Calibration: planted ruler onsets at q 0.3 give p 0.001–0.02; wrong-table control p > 0.05 in 20/20.
- **FAIL.** ZL3b-n p 0.31 / 0.30 / 0.81 (order-corrected 0.78 / 0.56 / 1.00); IT2a-n and RF1b-e p 0.21–0.43. Observed effects ≤ 0.003 Jaccard.
- With C1, H1a and H1b, no degree scheme links to the zodiac labels. Untested: a free start per sign; ruler-free 360-name lists (need a crib).

## P2-W (PC, 25-26 Nov 2026): voynich-letters per-letter boxes regenerated — DONE (PC `Voynich\p2w\`)
- Ward's voynich-letters pipeline (commit 4a27daa) rebuilt on the RTX 5060 in WSL: Kraken lines on 166 pages, dataset reproduced exactly (2,824 lines found, 2,173 used, 48 sheets), morphology4metrology patch compiled for sm_120, reference model trained (step 0 + step 1, 100 epochs), every ZL letter placed. **82,272 letters on 2,173 lines**, model letter = ZL at 97.6% (authors 97.7%); test-line CER vs ZL 5.39% [4.58, 7.47] (authors 5.1%). Deviations: 8 GB card, gradient accumulation kept the effective batch (16 / 8); step 1 paused after epoch 78 at the user's request and resumed (epoch 78 repeated, optimizer momentum restarted). Outputs on the PC: `p2w/out/letters.csv`, `extra.csv`, `lines.csv`, `results/`; crops in `~/p2w/voynich-letters/data/letters/`.

## P4-L (PC, 26 Nov 2026): was the line-initial glyph written apart? — gap PASS, tone NULL; box-free check holds in Currier B only (PC `p4l/PREREG.md`, `REPORT.md`)
- 17,736 words with >=2 glyphs; fixed effects for glyph 1, glyph 2 and line; 2,000 within-line permutations of the line-initial label.
- **Gap glyph 1->2: line-initial +0.044 line heights (+0.24 sd), p 0.0005**; A +0.13 sd, B +0.32 sd (both p 0.002); all three Davis scribes (+0.14/+0.38/+0.22 sd); second-word placebo -0.02 sd (p 0.33). **Tone (glyph 1 vs glyphs 2-3): NULL** (-0.002 sd, p 0.93). Pre-registered verdict: SEPARATE PASS SUPPORTED (by the gap).
- Secondary: line-initial gap far more variable (variance ratio 2.84); glyph-1 left edges slightly better aligned than glyph-2 (sd 22.4 vs 25.5 px, 63% of pages).
- Artefact checks (exploratory): line-initial glyph-1 boxes narrower (-0.20 sd), so part of the gap may be box placement at the line-image edge; no symmetric right-edge effect (line-final last gap -0.18 sd). **Box-free gap (blank ink columns between glyph centres): +0.17 sd overall (p 0.001), Currier B +0.26 sd (p 0.001), Currier A +0.02 sd (p 0.71).**
- By eye: f88v not among the 166 pages; f88r boxes sit correctly.
- Meaning: in Currier B the line's first glyph stands apart from the rest of its word, with more variable spacing and the same ink tone, consistent with a separate placement movement without a fresh dip; a possible physical basis for the S8/N2/S6-G line-start rule in B. In A it may be a box artefact. A spacing habit would look the same; this does not show the glyph was chosen separately. No claim about meaning.

## P4-D-b (PC, 26 Nov 2026): ink on o/e/y vs the S11 drift — PASS by rule, but a letter-mix artefact; each letter alone null (PC `p4d_b/`)
- P2-W letter boxes on the Archetype TIFFs; per line, ink contrast (P4-D L* rule, paper = local row band) on o, e and y boxes only; within-page partial correlation with the S11 composite after row position; 5,000 within-page permutations.
- **Primary: C_oey r +0.125, p 0.0002 (86 pages, 1,794 lines) -> PASS.** Control on all letter boxes r +0.050 (p 0.035), replicating P4-D's 0.046.
- **Exploratory decomposition:** o alone +0.007 (p 0.77), e alone -0.015 (p 0.57), y alone +0.021 (p 0.41); inner-60% boxes +0.118 (not neighbour intrusion); other glyphs +0.027 (p 0.27). The pooled link comes from the line's o:e:y mix (letters differ in typical contrast and the mix moves with the composite), not from ink state.
- Meaning: letter by letter, ink contrast does not track the S11 drift. With P4-D's split-row check this closes it: the drift has no ink or pen counterpart; both small correlations are glyph-mix artefacts. Lesson: pool ink only after standardising within letter type.

## H10e (PC, 26 Nov 2026): f115r 17/18 ink step vs hand change — NOT TESTABLE (calibration fails) (PC `h10e/`)
- Glyph-level Scribe 2 vs 3 classifier (HOG + box shape, 15 letter classes, leave-one-sheet-out, f115r excluded from training) on the P2-W crops. Gate passes: held-out-sheet line accuracy 0.747 (1,408 lines).
- **Calibration fails:** f115r lines 1-12 (Davis: Scribe 2) score +1.31 log-odds toward Scribe 3, lines 18+ +1.54 (p 0.43): the whole page reads as Scribe 3. Lines 13-17 +1.13; best split after line 36 (|t| 1.9) vs placebo 95th pct 4.9 on 18 Scribe 3 pages; score unrelated to ink tone (p 0.19).
- Meaning: letter shapes show no Scribe 2 stint on f115r and no change at 17/18; leans towards the 17/18 step being an ink session inside one hand, but with calibration failing it can't be claimed. Consistent with Ward and H10d.

## S6-Z1 (cloud, 26 Nov 2026): separate tables and settings for Currier A and B — **PASS 5/6, first pass of the any-split rule** (`s6z/z1/`)
- Pre-registered. Each language gets its own FIT-only tables and a re-search of 6 settings (copy, mutation, ending keep, line-end temperature, junction, drift). Held-out TEST over 6 directions × 5 seeds: mean **20.83/24** (S6-Y 20.00), 5/6 directions generalise (S6-Y 3/6), all texts above Timm and shuffle controls. Own tables with S6-Y's settings (Z1a) are worse: 18.90, 1/6.
- The fit makes Currier A much less copy-driven than B: copy rate 0.06–0.23 for A vs 0.40–0.64 for B (5/6 directions each), and A takes more mutation. A's settings vary a lot across directions (thin FIT data).
- Misses fall for R, editfirst, ff, E1, S4, S3, M2; S1_h2 and word200 rise slightly. The statistic-by-statistic A–B difference is still mostly not reproduced (slope 0.29 vs S6-Y 0.26). Z1b is the new base for S6-Z2.

## S6-Z2 (cloud, 26 Nov 2026): fresh word building from word parts — **not kept; the fit switches it off** (`s6z/z2/`)
- Pre-registered, on the Z1b base. A share pF of words built as onset + body + ending from the language's own FIT tables, kept away from the previous 40 words; plus redraw of exact repeats. The fit chose pF 0.00–0.04 in all 12 group fits. Mean TEST 20.47 (Z1b 20.83), 5/6 directions; keep rule fails.
- Mechanism check fails everywhere: one-off share 0.07–0.09 (real 0.138), edit-of-previous-40 0.18–0.30 (real 0.083). Same outcome as S6-X3: the 24-statistic objective prefers local recycling. Either the real one-off words come from something the profile can't see, or the profile under-weights them (it has no direct one-off statistic).

## S6-Z3 (cloud, 26 Nov 2026): per-language ending-order table — **not kept** (`s6z/z3/`)
- Pre-registered, on Z1b. Mean TEST 20.63 (Z1b 20.83), 4/6 directions (FAIL). M2 misses 10 → 6 and R 6 → 4, but word200 and ff misses rise and r1ba drops. The fit set the table strength to 0 in 7/12 group fits: on the Z1b base, the per-language junction tables already carry much of the ending order.

## S6-Z4 (cloud, 26 Nov 2026): ending-order table in Currier A only / B only — **not kept** (`s6z/z4/`)
- A only (Z3's A fit + Z1b's B): 20.93, 5/6, a narrow lead, but a pre-registered fresh-seed refit gave **20.57, 5/6** (Z1b 20.83). The gain is fit noise (spread between the two A fits 0.36 > effect 0.10). A table leaves M2 misses unchanged (10–11).
- B only: 20.70, 5/6; M2 misses 10 → 6 but word200, ff and S6_orderMI worse. **Z3's M2 gain came entirely from B's table**; B's ending order is real but entangled with line-position statistics.
- Fit-seed noise in the held-out mean is ≥ ±0.2–0.3, so earlier small rejections (Z2, Z3) mean "no detectable gain", not harm. Z1b stays frozen.

## S6-Z frozen reference (26 Nov 2026): **S6-Z1b**, mean TEST 20.83/24, 5/6 directions (`s6z/REFERENCE.md`, `s6z/REPORT.md`)
- Replaces S6-Y as the reference generator. It reproduces line-start rules (E1, E3), edge, ff and the copy/near-copy statistics almost always on held-out pages. It still misses S4_zipf 13/30, S3_sdlen 11, M2 10, S10_immrep 9, and the swapped direction stays at 17–20. One-off words are still made the wrong way: share 0.07–0.09 vs real 0.138, local-edit share 0.20–0.31 vs 0.083. Gains stalled after the per-language split, so the generator line stops here.

## P4-L-r (cloud, 26 Nov 2026): line-initial glyph gap REPLICATES on held-out sheets, but follows page layout (non-herbal), not Currier B (`p4l_r/`)
- Pre-registered, on P4-L's boxes. Box-free ink gap after the line-initial glyph, Currier B: **FIT sheets +0.25 sd, TEST sheets +0.27 sd (both p 0.0005, word-2 placebo ≈ 0) → REPLICATES.** Stays with paragraph-first lines removed (+0.25 sd).
- By section (B): balneological +0.37, stars +0.20 (both p 0.001), **herbal B −0.11 (ns)**. Exploratory: Scribe 2 shows it on balneological pages (+0.37) but not on herbal (−0.10); **Currier A non-herbal pages show it too (+0.42 sd, p 0.002)**; all herbal −0.06 (ns), all non-herbal +0.32 sd.
- P4-L-b (gap larger where the first glyph looks "added"): **not supported** (−0.01 sd, p 0.58).
- Meaning: **corrects P4-L's "Currier B only"**: the gap is a layout habit (pages with a straight left text edge; herbal text wraps round plants), not a language or scribe property, and it is not tied to the line-start glyph choice so far. No claim about meaning.

## D7-b (cloud, 26 Nov 2026): is the f49v margin column a counting sequence? — PATTERNED, not shown to count (`d7b/`)
- Pre-registered. Successor determinism 0.75 vs shuffle 99th 0.55 and natural line-initial columns 99th 0.63 (both p < 0.001); best periodic match 0.37 at lag 7, beating the shuffle (p 0.003) but not natural columns (99th 0.48, p 0.19).
- The column is one run `p o @192 y e @140` said twice, plus `y e @140` near the start; y→e 4/4. No tie to the f57v ring order (5 usable transitions). f76r and f66r columns are not like it.
- Meaning: a fixed-order recited list or formula, not a shown count. No claim about meaning.
- D7-d (same day): the run and its rare glyphs (@192, @140, @164) are almost unique to the f49v column (1–2 uses elsewhere each); not a formula used in the text.

## P3 + H10f (PC, 26 Nov 2026): line-edge glyph shapes and Davis's stroke criteria — **P3 PASS but NOT ROBUST; H10f NOT TESTABLE** (`p3h10f/`)
- Pre-registered. P3-L (line-initial vs mid-line first glyph): AUC 0.707, perm p 0.005 (floor), placebo word 2 0.545. P3-R (line-final): 0.607, p 0.005, placebo 0.535. But the box-render control (ellipses only, no ink) gives 0.674 (L) and 0.627 (R), so box size and placement explain almost all of it; ROBUST needed 2× the box-render excess.
- By eye (montage_LM): no consistent difference in glyph form; L masks more often carry extra ink from the line above or margin.
- H10f: validation gate failed on 1,266 Scribe 2/3 lines, 18 sheets: held-out-sheet balanced accuracy 0.557 (needed 0.70), perm p 0.119. By eye, the k crossbar measure picks up merged neighbouring ink, and the n tail measure mostly tracks whether the mask caught the whole glyph. f115r not scored.
- Meaning: no evidence that line-edge glyphs are drawn in a different form; the line-start effect stays one of choice, spacing and placement. Davis's criteria need stroke-level segmentation (H10g).

## P5-i (PC, 26 Nov 2026): image search for overwrites and erasures — **both detectors NOT TESTABLE** (`corrections/`)
- Pre-registered (`corrections/PREREG.md`). 82,155 P2-W boxes, 149 pages, 12 excluded for image problems (incl. f1v, f115r). 53 overwrite flags (733 before the redip guard), 426 erasure flags (420 from the ghost-gap rule).
- Gate failed. Recall 0/6: only f1v.7 of the six P5-b overwrites has P2-W boxes, and f1v was excluded (its spot scored D_z +2.8, just below the threshold). Precision by eye: overwrite 17/40 (43%; the true blobs are d/k/l/o/y loops filled solid, i.e. ink pooling, with no retracing); erasure ~5/40 (13%, mostly blank word gaps). Ghost rule fires on 1.35% of blank vellum windows vs 1.75% of real gaps, so erasure flags are near noise.
- Descriptive only (not scored): C5 rare words overwrite p 0.87, erasure p 0.89; overwrite line edges p 0.59. Erasure class and page effects follow gap width and page condition.
- Meaning: this says nothing either way about whether corrections cluster. It is a negative result for a visible-light darkness/brightness detector on this box set.

## P5-j (PC, 26 Nov 2026): retracing detector for overwrites — **NOT TESTABLE** (`Voynich\retrace\`)
- Pre-registered (`retrace/PREREG.md`). No letter boxes: every Kraken text line on 167 pages (166 TIFFs + f19r from the upscaled Yale JPG). Retrace score = signed two-tone asymmetry across widened strokes, corrected for stroke angle and nearby ink; blobs excluded by design. 292,582 windows, 469 flags (0.29 %). Six target boxes located by eye before the run.
- Gate failed on both parts. Recall 1/6 (chance mean 0.42, P(≥1) 0.37; the one hit is the t at the start of f39r.12, not the blob). Closest miss: f87r.7's retraced k (4 retrace pixels, flag needs 5). Blind precision (40 flags + 40 controls shuffled): strict 0/40 vs 0/40; lenient "two-tone/smudged" 5/40 flags vs 1/40 controls. Flags are mostly loop pooling, heavy strokes, blur.
- Descriptive only: line-edge proxy ratio 1.10 (p 0.25); line number rho +0.005; page dispersion 1.45. C2/C5 not computed.
- Meaning: at ~0.08 mm/px with 5–6 px strokes, neither darkness (P5-i) nor edge asymmetry (P5-j) separates corrections from normal ink variation in visible light. Says nothing either way about corrections. Next routes: MSI (P5-M) or a larger hand-confirmed overwrite set.

## P4-L-e (cloud, 26 Nov 2026): line-start glyph rule vs the line-initial gap — SEPARATE (`p4l_e/`)
- Pre-registered. JS divergence of line-initial vs later first glyphs above a within-line swap null: Currier B herbal 0.26 vs B other 0.24 (ratio 1.09, CI 0.85–1.46); Currier A herbal 0.14 vs A other 0.22 (ratio 0.62, CI 0.52–0.72).
- Meaning: the line-start rule is full strength on herbal B pages, where the physical gap is absent. The gap is a layout habit, not the mechanism of the line-start rule. No claim about meaning.

## S17-J (cloud, 26 Nov 2026): slow vocabulary drift in the frozen generator — FAIL (drift 2/6; profile guard met) (`s17j/`)
- Pre-registered. A recent-pages copy pool (previous 10 pages, decaying) added to S6-Z1b and fitted per language on FIT pages. At zero it reproduces S6-Z1b exactly. The fit chose 0–0.05 for every B group and 0–0.3 for A.
- Held-out TEST drift curve (mean overlap ratio at 2–5 pages): within 0.2 of real and closer than S6-Z1b on 2/6 directions (swap, r1ab). r0ba overshoots. Profile 20.73/24, 5/6 directions (guard met). **FAIL**; S6-Z1b stays the reference.
- **Key correction to S17-I:** within one language, with rare types counted inside it, there is almost no slow drift (A: d1 1.99, d2–5 1.14; B: d1 1.35, d2–5 1.02). The S17-I drift (d2–5 1.75) appears only when A and B are pooled. The real page structure is a one-page bonus within a language plus language and section mix.

## S17-L (cloud, 26 Nov 2026): is the S17-I slow drift section mix? — YES, no drift inside sections; one-page bonus survives (`s17l/`)
- Pre-registered. Pairs within (section, hand); each pair against its own section's ≥6-apart baseline; rare = count 2..10.
- Pooled d1 / d2–5: S17-I as published 2.37 / 1.75; per-group baseline with whole-manuscript rare 1.64 / 1.17; rare within language 1.46 / 1.06; **rare within section 1.36 (p 0.0005) / 1.00 (shuffle null 1.00, p 0.54)**. Rule: section mix explains the drift (100% of the d2–5 excess).
- Per section (within-section rare): d1 A-herbal 1.52, B-herbal 1.32, B-stars 1.14, A-pharma 1.11, B-bio 1.02.
- **Correction to S17-I:** its 1.75 "slow drift" was mostly a baseline-weighting artefact (one baseline dominated by the long, sparse A-herbal run) plus section mix. The real page structure is a one-page bonus, strongest in A-herbal, and no drift. Page-order tests must use adjacency within a section. No claim about meaning.

## S17-K-A (cloud, 26 Nov 2026): page order inside Currier A herbal — cross-leaf bonus weak PASS, nesting rank FAIL (`s17k_a/`)
- Pre-registered. A-herbal hand 1, rare types counted within A-herbal. Same-leaf r→v R 1.66 (n 46); **cross-leaf neighbours in a quire 1.38 (n 30), leaf-shuffle null 0.99, p 0.042**; across quire boundaries 0.88 (n 4). Heavy-tailed: 12/30 cross-leaf pairs share no rare type.
- Rank of the current nesting among 384 bifolio orders × flips per herbal quire: mean share of better orders 0.37 vs null 0.50, **p 0.11, FAIL**; only 1–7 A–A cross-leaf pairs per quire because A and B bifolios alternate. B-herbal untestable (2 pairs).
- Exploratory: Pelling's tear sequence (35 36 9 10 15 16 37 38) joins score 1.66 on 3 pairs, 74th percentile; not significant.
- Meaning: the A-herbal binding keeps a little of an original page sequence across leaves, but text alone cannot rank quire nestings. No claim about meaning.

## P4-L-f (cloud, 26 Nov 2026): why the Currier A line-start rule is weaker on herbal pages — SECTION, not length or drawing (`p4l_f/`)
- Pre-registered; statistic as P4-L-e. Herbal A Δ 0.136 vs other A 0.219 (0.62). Reweighting herbal lines to other-A lengths: ratio 0.64 (CI 0.51–0.80), so length does not explain it; within herbal, 3–5-word lines have the strongest rule (0.160).
- P2-W widths: herbal lines cut short beside the drawing Δ 0.171 vs full-width 0.119 (short/full 1.44, CI 1.10–1.91); full-width herbal is 0.54 of other A. The drawing does not explain it either; it goes the other way.
- Meaning: the weaker rule is a property of the herbal A text itself (likely its vocabulary), not of layout. No claim about meaning.

## GG-3b (cloud, 26 Nov 2026): Currier B ending order across sections within hand 2 — SECTION-SPECIFIC (`gg3b/`)
- Pre-registered; GG-3 measure, all groups size-matched to herbal B hand 2 (2,337 words). Balneological vs balneological ρ +0.52; **herbal B vs balneological (same hand) +0.00** (R 0.00; shuffle p95 +0.30); stars hand 3 vs balneological +0.30 (R 0.58); herbal A vs balneological +0.01.
- Exploratory: herbal B agrees with itself (+0.38) and a little with stars (+0.25), not with herbal A (+0.01).
- Meaning: one scribe uses unrelated ending orders in two sections. GG-3's B-wide sharing is mostly balneological–stars; the ending order follows section/vocabulary more than language or scribe, which argues against one B grammar for this feature. No claim about meaning.

## P4-L-g (cloud, 26 Nov 2026): the weaker herbal A line-start rule is weaker choice, not vocabulary — CHOICE (`p4l_g/`)
- Pre-registered. JS(line-initial vs mid-line first glyph) herbal A 0.133, other A 0.209. Applying other-A lifts to the herbal mid-line mix gives 0.238, so the share due to lifts is 1.38 (CI 1.03–2.36): the vocabulary would give a *stronger* rule.
- Lifts correlate (ρ 0.72), but t (1.7 vs 9.6), d, y and s are weaker line-initially in herbal; q (1.95 vs 0.85) and o (1.72 vs 0.59) are line-initial in herbal only.
- Meaning: the line-start habit itself differs by section inside one hand and language (with GG-3b: section-level conventions). No claim about meaning.

## GG-3c (cloud, 26 Nov 2026): section ending order is general, not fixed word pairs — GENERAL ORDER (`gg3c/`)
- Pre-registered. Split-half ρ of adjacent ending-pair asymmetry: herbal A 0.48 → 0.42, balneological 0.53 → 0.46, stars 0.57 → 0.49 after removing every word bigram seen ≥ 3 times (8–16% of pairs); about 87% retained; shuffle ≈ 0. Herbal B (secondary) 0.41 → 0.33.
- Meaning: the section-specific ending order (GG-3b) acts on word pairs in general, not on stock phrases. Line-position order is part of it (not removed here). No claim about meaning.

## GG-3d (cloud, 26 Nov 2026): ending order with line position removed — NOT TESTABLE (`gg3d/`)
- Pre-registered; position-preserving permutation removes each ending's line-position profile. At herbal-B size (2,337 words) within-balneological residual ρ 0.29 vs control p95 0.30, so not testable. Descriptive: line position is a little under half of the within-section agreement (0.52 → 0.29); herbal B vs balneological residual −0.05, stars vs balneological +0.16 (same direction as GG-3b).

## GG-3e (cloud, 26 Nov 2026): adjacent-only ending order at full section size — NOT TESTABLE; most stars and herbal A ending order is line position (`gg3e/`)
- Pre-registered; GG-3d residual measure, ≈ 3,000-word halves, 200 reps. Within-section residual ρ: balneological +0.39, stars +0.19, herbal A +0.10; control p95 +0.21, so stars and herbal A fail the testability gate and no pair can be scored.
- Descriptive: with position in (GG-3c) stars 0.57 and herbal A 0.48, so their ending order is mostly line position; balneological keeps a real adjacent part. Balneological vs stars residual +0.18 (≈ stars' own within); herbal A vs either ≈ 0.
- Meaning: GG-3b's section-specific ending order is, outside balneological, mainly a section-specific line-position profile. No claim about meaning.

## P4-L-h (cloud, 26 Nov 2026): herbal A line-initial q-/o- words — particular word types, not a paragraph/label formula; not clustered on pages (`p4l_h/`)
- Pre-registered. Q1 MIXED: line-initial q/o tokens are no more often paragraph-first or label types than mid-line q/o tokens (0.34 vs 0.40, D CI [−0.13, +0.01]), but their type mix differs (JS p 0.003): qot-/ot- forms (qotchy, qotor, qotchor, otchol, otchor) and oaiin are enriched at line start; ol, o, or are not.
- Q2: raw per-page dispersion p 0.06 (no clear clustering). The pre-registered adjusted test read PAGE-LEVEL but flags 100% of unclustered permuted texts in a calibration check, so it is invalid and not counted.
- Meaning: the herbal A line-start q/o habit is section-wide and favours particular qot-/ot- words, not a start formula shared with paragraph openings or labels. No claim about meaning.

## S17-K-b (cloud, 26 Nov 2026): A-herbal cross-leaf bonus REPLICATES across transcriptions; tf-idf clearer (`s17k_b/`)
- Pre-registered. Cross-leaf neighbours (same quire, n 30), ratio to ≥ 6-apart baseline, leaf-shuffle null. Rare overlap: ZL 1.37 (p 0.051), IT2a-n 1.36 (0.047), RF1b-e 1.38 (0.045), CD2a-n 1.28 (0.14). tf-idf cosine: 1.30–1.42, p ≤ 0.006 in all four. Rule: REPLICATES.
- Exploratory stricter null (leaves shuffled only within their quire): tf-idf still p 0.006–0.013 (null 1.09–1.13), rare overlap p 0.05–0.09; the bonus is adjacency, not just same quire.
- Meaning: the binding keeps some original page sequence across leaves in Currier A herbal, independent of transcriber; still too weak for quire-level nesting ranks. No claim about meaning.

## S17-L-b (cloud, 26 Nov 2026): A-herbal one-page bonus, topic or carry? — NOT RESOLVED; coded plant type cannot account for it (`s17l_b/`)
- Pre-registered; 76 A-herbal pages with blind drawing codes. Far pairs with similar drawings: tf-idf 1.02 (p 0.20; decision measure), rare overlap 1.09 (p 0.002). d1 bonus 1.43 (tf-idf); among neighbours with dissimilar drawings 1.27, CI [0.82, 1.81] (n 24), so carry is not shown either.
- Descriptive: neighbours are no more alike in drawing than far pairs (2.96 vs 2.89 of 6 features), so a topic effect of ≤ 0.1 cannot make a 0.4–0.5 bonus through coded plant type; similar-drawing neighbours 1.57 vs dissimilar 1.27 suggests a small topic part.
- Meaning: the one-page bonus is mostly not "same plant type on neighbouring pages" as far as the coarse code sees; carry vs uncoded topic stays open. No claim about meaning.



## M1g / P5-M / H8-M (PC, 26 Nov 2026): glyph ambiguity map and MSI checks (`m1g/`, `msi/`)
**M1g (glyph ambiguity map):** gate PASS. At the 516 ZL/IT-disputed tokens the reader is far less sure than at agreed ones (p~1e-204), and it sides with IT about half the time (a/o 52%, k/t 54%, r/s 39%). Ink gain over a 2-glyph context model, held-out: k/t +0.31, ch/sh +0.34, ckh/cth +0.32, ch-vs-s +0.18 (DISTINCT IN INK); ch/ee +0.047, a/o +0.042, r/s +0.028, o/y +0.025, e/o +0.021 (PARTLY SEPARATED; context alone gives AUC 0.95-0.98). The reader prefers the other glyph on 2-5% of a/o and r/s tokens. No real pair is "one glyph"; the rule's e/h and h/s flags are EVA artefacts. Takeaway: a/o and r/s statistics at the 2-5% level carry real transcription noise; k/t and ch/sh are safe.

**P5-M (MSI erasures): NOT TESTABLE.** A UV-only-residue detector on f8r/26r/47r/93r/102v1 found 8 candidates, all on f8r and all non-writing; placebos gave 0-1. Blind rating of 84 crops: 0 erased writing, 0 backtracing. The detector also finds 0 on f1r, where Davis's UV-only margin writing is known, so it lacks sensitivity and "none found" can't be claimed. By eye nothing looked like underwriting, which agrees with Davis.

**H8-M (marginalia in MSI): descriptive.** f116v: same reading as in visible light. PCA removes a red smear over line 3 and sharpens line 1 (~3-6 letters easier, none MSI-only). Reading: "pox leber umen ... / +[mi]chiton oladabas + multos + te + cter cere + portas + ... / six + marix + morix + vix + abiar + maria + / alor cacca valsch ubren so nim gasmich o". umen, vix, valsch and ubren start with u/v forms, but "pox" has a looped p, so the evidence is mixed. f17r top margin gives the clearest MSI gain: the last two words are clear only at 365 nm (~9 letters UV-only): "[m]al[s]ier a[l/h]or k[u]e[z] hen pollemmia o?luco[s] or[c]h". The marginal ink is IR-transparent like the main text but fainter (870/365 contrast 0.05 vs 0.09-0.12). A faint outline drawing beside folio number 17 shows mainly in UV. No decipherment claim.


## D4-V2 (PC, 26 Nov 2026): Bax-style plant names with verified lists — **FAIL** (`d4v2/`)
Name lists verified from fetched sources: Leclerc's Ibn al-Baytar t.1 plus t.2 (43 genera) and Wellmann's Greek Dioscorides headwords (41 genera; botrys, skolymos, smilax and diktamnon rejected as different plants). Scored with the same Bax key as D4-V, on 45 and 43 pages (13 before). Arabic: rank 0.505 vs null 0.506, p 0.48; Timm 0.481 and glyph-shuffled 0.468 do better. Greek: 0.449 vs null 0.499, p 0.057, but glyph-shuffled words score 0.443, so word identity adds nothing. List quality no longer explains the D4 failure. Leclerc t.3 (~15 genera) could not be fetched.

## D4-V3 (26 Nov 2026): Leclerc t.3 added to the Arabic plant-name list — **FAIL** (`d4v3/`)
Leclerc t.3 fetched from HathiTrust (hvd.32044107259558). It verifies 8 more genera, not ~15: colocasia, lithospermum, geranium, gnaphalium, tragopogon, lychnis, hieracium, mentha (dictamnus, heracleum, acanthus rejected as different plants). Same D4-V2 scoring on 51 genera / 55 pages: rank 0.504 vs null 0.508 ± 0.026, p 0.45; Timm 0.481 and glyph-shuffled 0.496 do as well or better. With the complete Leclerc list the Arabic side of Bax-style plant naming is closed.


## B11d + B11f (PC, 26 Nov 2026): ring-page fixes — **NO FIX FOUND** (`b11df/`)
Under bundle-12 geometry the ring count matches ZL on 24 of 32 diagram pages. Sweeping REFIT_TOL, RING_GAP, RING_COVER and RING_OVERLAP one at a time changes none of the six misses (f69r +1, f70r1 -1, f70v2 +1, f72r2 -1, f72r3 -1, f72v3 +1), and some settings make it worse. The B11d label rule (a ring with >= 4 gaps of 2 x-heights and mean piece < 6 x-heights becomes labels) correctly retypes f67r2's inner label ring and changes no other page. No fit page has a label ring, though, so it can't lower the fit error, and under the pre-registered rule it was not carried to a reading run.

## S6-Z2-b (cloud, 26 Nov 2026): one-off share and local-edit rate added to the profile — fit still refuses fresh words; "unmodelled process" (`s6z/z2b/`)
- Pre-registered. S27 (one-off share) and S28 (one-offs within one edit of the previous 40 words) added to the FIT objective; Z2 mechanism refit on Z1b. TEST bands ±0.038 / ±0.020 from random sheet half-splits.
- Part-built share ≥ 0.05 in only 2/12 fits (5/12 kept the Z1b settings exactly). S27/S28 in band on 0/30 texts (Z1b, S6-Y and Timm also 0/30); S27 0.11–0.16 vs real 0.16–0.19, S28 0.18–0.23 vs real 0.10–0.11. 24-stat mean 20.20 (below the 20.53 floor), 5/6 directions. Not kept.
- Meaning: the profile was not just under-weighting one-offs; the real one-offs (more frequent, rarely edits of nearby words) come from a process missing from every S6 generator. No claim about meaning.
- Baseline added for A4-P: Z1b scored on 25 statistics (24 + A4) is 21.07 mean, 3/6 directions generalise on 25 (A4 in band on 7/30 texts) (`s6z/z5/score25_z1b.out`).


## OO (cloud, 26 Nov 2026, pre-registered): one-off words split into "small edits" and "free" — free ones are the long words; no drawing or subject clustering (`oneoffs/`)
- Table of all 5,526 ZL one-offs (14.3% of tokens): `oneoffs/oneoffs_table.csv`. EDIT1 36%, EDIT2 40%, FREE (3+ edits from every frequent and recent word) 24%.
- FREE ones average 8.4 characters (EDIT1 5.7). Real words of length 8 / 10 are one-offs 52% / 90% of the time vs S6-Z 24% / 38%.
- Structure: FREE are well-formed (trigram logprob −1.91 vs shuffled −4.00). Against generator one-offs, real one-offs (FREE and EDIT2 alike) have rarer glyphs (0.047 vs 0.032), lower glyph probability, and more onset+ending pairs unseen in common words (30% vs 19%); holds mid-line. FREE-specific pattern only after length matching: weak.
- Clusters (Holm): labels PASS (FREE share 0.33 vs 0.23, survives length control); line-first PASS but mostly length; circles fail; similar-plant pages fail (p 0.71); same-section p 0.036 fails Holm and matches EDIT one-offs at equal length. **Meaning test FAIL.**
- Transcription check PASS: 88% (IT2a-n), 95% (RF1b-e), 80.5% (a/o, r/s merged) of FREE stay FREE.
- Reading: real one-offs come from a long-word building process with new onset–ending pairings that no S6 generator has; it shows no sign of tracking subject matter.

## S6-Z4-d (cloud, 26 Nov 2026): per-section ending-order table on Z1b — not kept (`s6z/z4d/`)
- Pre-registered; Z3 table built per section inside each language (FIT only). Mean TEST 20.60, 4/6 directions (r0ab lost); keep bar 21.13. M2 misses 10 → 6 with no line-position cost (E2 5 → 6, lastlast 2 → 0), but S4_zipf 13 → 17, S3_sdlen 11 → 15. Fitted bE 0–1.15 (0 in 4/12). Z1b stays the reference.


## OO-N / OO-L / OO-G (cloud, 26 Nov 2026, pre-registered): one-offs as nouns? names? a long-word stream? (`oneoffs/REPORT_N.md`)
- **OO-N, nouns: not supported, and the test cannot separate nouns from a writing habit.** In 8 POS-tagged RIDGES German herbals the free one-offs are noun-rich (NN+NE 0.37–0.65 vs 0.22–0.27). At equal size, Voynich one-offs are mostly small edits (free 15–18% vs German 41–62%), and long Voynich words almost never recur (one-off share of long tokens 0.73–0.84 vs German 0.34–0.71). Topic nouns would recur locally. The Voynich's line-first excess of free words has no German counterpart; the generator has it too. On the pre-registered profile rule Voynich is inside the German range on 3.75/7 features vs generator 3.5/7: no better than generated text. EVA vs German letters limit F2.
- **OO-L, labels as a name stock: FAIL.** Label one-offs are no closer to each other across pages than matched paragraph one-offs (0.320 vs 0.323, p 0.32); free label one-offs are more dissimilar (0.403 vs 0.357).
- **OO-G probe, long-word one-off stream on S6-Z: FAIL.** S27 one-off share 0.17–0.21 (real 0.16–0.19; reference 0.09–0.12), S28 0.11–0.17 (real ~0.10; reference ~0.21), both in band 6/30 (reference 0/30). But length-10 one-off share is still short (0.69–0.87 vs 0.92–0.97), and the 24-stat mean drops to 19.53 (3/6 directions; reference 20.83, 5/6), with costs on edge, M2, ff, S3_sdlen. Long real one-offs keep line-edge and glyph-sequence habits that free pairing breaks.

## OO-SP (cloud, 26 Nov 2026, pre-registered): spelling patterns in free one-offs (`oneoffs/REPORT_SP.md`)
- Specific to free one-offs (differs from EDIT2 one-offs, unit-shuffled words and S6-Z one-offs, length-matched): **fewer doubled glyphs** (0.30 vs 0.38–0.48; ee 26 / ii 11 per 100 words vs GEN 36 / 23); **more 2+ gallows** (0.16 vs EDIT2 0.085, GEN 0.107); p/f pairs over-represented beyond GEN (ep 7.7× vs 3.4×, po 4.6× vs 2.3×, fch 3.8× vs 1.8×), mostly mid-line (e.g. chepchefy, choepchey).
- Not specific: repeated inner chunks (0.27, GEN 0.25); rare-glyph position (same as GEN). Compounds: 21% are exact joins of two common words (GEN 16%, German 2%); a one-edit-tolerant split works for 85% of free and 82% of GEN words, so it is uninformative.
- Reference catalogue (26 Nov, no new tests): all 1,328 free one-offs with placement, prefix/core/ending split, p/f positions and 133 start–ending pairs absent from recurring words, in `paper/oneoff_catalogue/` (for the paper edit with the control-hand results).


## Track 2 PC image tests (26 Nov 2026): P5-M-b, H8-M-b, B11j, B11k, P3-b
**P5-M-b (local-contrast UV erasure detector), NOT TESTABLE** (`p5mb/`). Calibration on f1r failed: density ratio 0.52 at t=2, against the >= 5 required. In the effaced signature, UV and red darkness go together (z 4.0 / 5.2, correlation 0.80), so the effaced ink is not UV-specific. Any "dark in UV, not in visible" detector misses it by design.
**H8-M-b (f17r margin hand vs f116v), INCONCLUSIVE** (`h8mb/`). The method is valid on month names (d 4.11, p 0.010). f17r vs f116v gives d 1.85, p 0.002, far below the control-hand distance of 3.51, and close to the imaging-only effect of 1.84. Neither same nor different hand is shown. The f17r drawing is in IR-transparent, iron-gall-like text ink (870/365 0.11), not the folio-number ink.
**B11j (f67r2 with the label rule), ADOPTED** (`b11j/`). Rings 2 -> 1, acer 0.633 -> 0.611, other pages identical. Rank p 0.031. The current machine transliteration is voynich_kraken_b13.txt.
**B11k (ring counts from ink cues), NO INK FIX** (`b11k/`). Fit error 2 / unseen 18 / exact 17 of 32, against the geometry baseline 1 / 8 / 24. It fixes f70v2 and f72v3 but breaks 9 pages. The border-circle cue never fired.
**P3-b (line-edge glyph shape, placement-matched), PASS, ROBUST** (`p3b/`). L vs M AUC 0.613 (p 0.005, placebo 0.487); RL vs RM 0.583 (p 0.005). The matched box control is at chance (0.514 / 0.518). Mask geometry alone gives 0.604 / 0.564, so the signal is mostly mask extent, not proven pen form. It may reflect the P4-L gap.


## M1g-b (cloud, 26 Nov 2026): doubtful a/o and r/s glyphs vs the statistics that use them (`m1gb/`)
186 doubtful glyphs (the M1g reader prefers the other glyph), on 40% of text lines. Dropping or swapping them changes near-copy rate, hapax share and the a/o share of rare types by < 1%, so those results are **ROBUST**. **a/o and r/s minimal-pair counts are SENSITIVE**: doubtful glyphs sit in minimal-pair words 2-3x more than random ones (drop: −19 of 725 a/o pairs, −16 of 248 r/s pairs vs control −1 to −9; swapping to the reader's choice removes pairs where random swaps add 13-52). No earlier finding rests on minimal-pair counts; future minimal-pair arguments should drop doubtful glyphs first.

**H10g (stroke-level masks + H10f gate), NOT TESTABLE** (`h10g/`). Masks cleared of line-above ink, cut at neighbour midpoints, and filtered for completeness. Gate: held-out-sheet accuracy 0.532 (need 0.70), p 0.27, on 1,315 Scribe 2/3 lines over 18 sheets. Only a trend for k (longer crossbar in Scribe 3, p 0.069) and t (p 0.13). The n-tail measure fails by eye. Threshold masks can't test Davis's stroke criteria; a trained per-glyph segmenter is needed.
**P4-L-c (f88v first-glyph column, box-free), NOT TESTABLE** (`p4lc/`). The v2 measure still lands on specks in about 5 of 16 lines. Hint only: on f88v the gap after glyph 1 is 0.74 xh vs 0.20 later (p 0.0065), with no such gap on f88r (p 0.26). Left-edge alignment is not shown (CI [-0.06, 0.78]). It needs letter boxes on f88v.

## B11b (cloud, 26 Nov 2026): machine vs ZL ring ends (`b11b/`)
On all 65 bundle-10 rings matched to ZL loci, the machine rings do show the ring-end -m lift (5.6, above a random-rotation 95th percentile of 4.0; ZL 7.9). The ZL vs machine gap is 6 vs 4 final -m words (Fisher p 0.74). Neither a different start (46% of machine rings start 1-5 words off, but re-rotation doesn't raise the lift) nor joined label text (length ratio 0.96) explains it. B10b's "no end rules in machine rings" was a small-sample effect; ring-end statistics have < 10 events per source and can't separate transcriptions.

## N1-b (cloud, 26 Nov 2026): re-keying-invariant word-order metric — FAIL (`n1b/`)
Conditioning the word-bigram gain on the previous word's last glyph does not make it invariant: 100 random first-glyph re-keyings raise it +0.43 bits (plain gain +0.50), because re-keying changes the vocabulary itself. With the pre-registered smoothing the held-out gain is negative even on Latin. Autokey ideas remain untestable; N1-c proposes body-level units with CV smoothing.

## S6-Z5 / A4-P full re-search (cloud, 26 Nov 2026): onset habit + A4 as statistic 25, refit on Z1b — not kept (`s6z/z5/`)
- Pre-registered. 25-stat TEST mean 21.00 vs Z1b 21.07 (bar 21.37); 24-stat 20.43 (floor 20.53); 4/6 directions on 25. A4 in band 17/30 texts (Z1b 7/30); original direction 25/25 on all 5 seeds.
- The fit gives B a larger habit than A in 4/6 directions (B-habit reading holds), but in r0ab B turns it off (A4 missed) and in r0ba A takes 0.144 (A4 overshoots); A4's FIT noise is too large to pin the rate down. Habit costs ~0.4 on the 24 (M2 10 → 13, d1d2 3 → 6). Z1b stays the reference.


## S16g (cloud, 26 Nov 2026): Italian calibrated, Voynich in Italian FAIL (`s16g/`)
With a clean Italian LM (Bruni, Ariosto, Machiavelli; no Dante, no OCR), the S16e decoder recovers Greshko's N52 key on Dante (0.887, was 0.194) and on held-apart Italian (0.901); shuffled control 0.087. The Voynich run in Italian fails every criterion: TEST M1 4.84 (bar 3.69), M2 0.212 (< 0.30), top-8 agreement 0.14, and glyph-shuffled Voynich (M2 0.357) and human gibberish (0.283) score better. A Naibbe-style verbose homophonic cipher over Latin, MHG, Occitan or Italian close to these corpora is now ruled out in all four languages. D1's lost core modules were rebuilt (`s16g/code/d1_rebuild/`) and validated by this calibration.

## S6-Z6 (cloud, 26 Nov 2026): last generator try — not kept; generator frozen at S6-Z1b (`s6z/z6/`)
A mid-line long-word spelling habit (fewer doubled e/i, extra inner p/f gallows in long new words) on top of S6-Z1b scores 21.00/24 mean TEST (5/6 directions) vs 20.83, inside the ±0.3 seed noise, so it is not kept. Where fitted (6/12 groups), it moves long one-off spelling toward the real text (doubled e/i 0.29-0.42 vs real 0.30 and Z1b 0.36-0.44; 2+ gallows 0.12-0.20 vs real 0.16), but none of the 24 statistics measures inner spelling. **S6-Z1b is final.** D6-P2, LE13e and S6-H-PC are parked with the freeze.

## P5-l (cloud, 26 Nov 2026): published corrections and overwrites, literature sweep — **reading only; ~16 scribal corrections, not 40** (`lit_corrections/published_corrections.csv`)
- Sources read: Zandbergen voynich.nu (writing.html "Apparent lack of corrections" gallery, folio pages), Stolfi (2004 retouching page, Note 075 report and Ninja posts), Pelling (Cipher Mysteries 2014, scan wishlist), Voynich Ninja printthreads 136, 3259, 4899 (replies login-gated, so only opening posts read), McCrone 2009 via Stolfi's sample table, Davis 2024 MSI press. Not reached: Glen Claston's transcription notes, the McCrone PDF itself, Davis's own blog post.
- **Scribal corrections in Voynichese:** 16 spots. Our 6 (P5-b) plus Zandbergen's gallery, which confirms emendations on f16r, f42r, f79r, f112r (ZL-flagged spots where the P5-b crops saw nothing, so those crops probably missed the word), f102v2, and adds **5 new**: f20v (an *s* corrected from "99"; also aStobbart, Ninja 3259), f24v, a second spot on f39r, f80r, f83r. Zandbergen gives images only, no line numbers. One more uncertain (f57r *r*, scraped or faded; Anton, Ninja 136) and one "overwritten text" on f86v (Pelling, no line).
- **Later retracing (Stolfi's "Retracer"):** f1r.2–3, f2r.8–10, f4r, f47r, f67r2, f116v.2/4 verbatim, and f30r, f31r, f57v, f70v1, f71r, f73v from summaries (unverified). Many glyphs, but a different claim (a later hand reinforcing faded ink, not scribal correction) and contested on the Ninja by oshfdk and others. Not usable as P5-k training labels for scribal overwrites.
- McCrone 2009 reports materials only; no corrections or erasures in the Voynichese text. Davis's MSI finds are the f1r margin columns and the effaced Tepenec ex libris (non-Voynichese, already used in P5-M).
- **Meaning:** the literature agrees corrections are rare (Zandbergen, Pelling). Published scribal corrections total about 16, so P5-k stays parked; no ~40-spot labelled set exists. Side point: Zandbergen's confirmations mean ~4 of P5-b's "nothing visible" spots are real corrections missed by crop centring, so the visible-light count of confirmed overwrites is about 10–11, not 6.


## Glyph segmenter and letter-level reruns (PC, 26 Nov 2026)
**GS (trained per-glyph segmenter, `glyphseg/`): PASSES validation.** A U-Net trained on rendered scenes built from 37,086 clean exemplars, cross-fitted over two sheet folds. Held-out IoU: k 0.95/0.94, t 0.95/0.93, n 0.98/0.98 (threshold baseline 0.81–0.88). By eye: k 92–94%, t 92%, word-final n 83–88% acceptable (gate 80%). Caveat: the tiles were scored by the same session, not by independent annotators.
**H10h (scribe gate with GS masks): NOT TESTABLE, third failure.** Accuracy 0.555 (need 0.70), p 0.21. The k-crossbar and n-tail measures now work by eye, and only a weak k trend repeats (p 0.10). Mask quality was not the problem: Davis's k/t/n criteria as measured here don't carry the Scribe 2/3 difference.
**P3-c (line-edge pen form, clipped GS masks): PASS, ROBUST, pen form.** L vs M AUC 0.641 (p 0.005), RL vs RM 0.587 (p 0.005); placebos and box control at chance. HOG-only (extent removed) 0.633 / 0.586, so the signal is pen form, not mask extent. Strongest: line-initial t 0.90, sh 0.72, line-final n 0.66; line-initial y often has a long down-left tail. Physical support for line-position-specific writing. **[Superseded by P3-e below: a control hand shows the line-initial effect as strongly, so this is ordinary scribal behaviour, not a Voynich-specific finding.]**
**P4-L-d (f88v first-glyph column, model boxes): NOT SUPPORTED.** Model letters match ZL at 94.4%. sd(e1) 0.62 vs sd(e2) 0.60 xh; no extra gap (p 0.58); f88r the same. The P4-L-c hint doesn't hold. Low power (about 16 lines per page).
**P4-S (f105r ink-session breaks): NOT FOUND.** The method is calibrated on f115r (p 0.001). f105r just fades down the page (0.55 -> 0.46), with no clean step and no odd line. 10 of 37 lines are unboxed, including line 23.

**P3-c by scribe and section:** the line-initial pen-form effect appears in every scribe and section with enough glyphs: Scribe 1 0.608, Scribe 2 0.604, Scribe 3 0.564; Biological 0.586, Herbal 0.601, Stars 0.604 (placebos <= 0.50; p 0.01-0.06). The line-final effect is uneven: Scribe 3 0.642 and Stars 0.622 (p 0.01), Scribe 1 0.570, Biological 0.563, Scribe 2 0.547, Herbal 0.531 (absent). No subset reverses.
**P3-d (descriptive figure, PC p3c/p3d_line_edge_masks.png):** mean masks of line-edge vs mid-line glyphs. Line-edge glyphs are more diffuse and sit higher; line-final n has extra ink in the upper bowl. Partly confounded by band-fit error at line ends, so use it as illustration, not evidence.

## P3-e (PC, 26 Nov 2026): control hand for the P3-c line-edge pen-form effect — **line-initial: ORDINARY; line-final: weak in both hands** (`p3e/`, PC `Voynich/p3e/`)
Pre-registered (`p3e/PREREG.md`, two deviations decided before outcomes, in `p3e/RESUME.md`). Control: BSB Clm 5905 (Ebersberg 1479, Vitus Auslasser; Latin Macer verse + remedy prose, gothic cursive), 336 text pages, 6,047 lines, 157k letters. Same pipeline as P3-c: Kraken (CATMuS-Medieval) letter cuts, GS segmenter retrained on this hand's own ~4,000 clean exemplars (rendered validation IoU 0.94–0.98, baseline 0.70–0.80), unchanged p3.py with placement matching, page-grouped CV, 200 permutations, W2/RP placebos and ellipse box control. P3_MINN = 40, 11 classes per arm.
| arm | control AUC (p) | HOG only | placebo | box control | Voynich P3-c AUC / HOG |
|---|---|---|---|---|---|
| line-initial (L vs M) | **0.681** (0.005) | 0.680 | W2 0.522 | 0.381 | 0.641 / 0.633 |
| line-final (RL vs RM) | 0.556 (0.005) | 0.554 | RP 0.532 | 0.432 | 0.587 / 0.586 |
- **Line-initial: the control passes and is stronger than the Voynich (HOG 0.680 vs 0.633).** Pre-registered outcome: the Voynich line-initial pen-form effect is **ordinary scribal behaviour**. By eye the control's line-initial letters are often enlarged or near-capital forms (long-stemmed l, h, f, p), the same kind of habit as the Voynich's flourished line-initial y and gallows. Strongest control classes: h 0.92, f 0.87, p 0.81.
- **Line-final:** the control fails the rule only because its RP placebo (0.532) exceeds half the effect, which formally reads "Voynich stronger", but the HOG gap is 0.03 (margin 0.07). Fair reading: both hands show at most a weak line-final effect.
- Box control is below 0.5 in the control (placement matching leaves ellipse features anti-informative); it does not affect the pass rule. Masks clean in ~44/48 montage tiles.
- **Consequence:** P3-c is no longer a Voynich-specific positive. The paper (v1.1) reports it as an ordinary/negative result. Caveats: one control manuscript, cursive with verse sections; Kraken cuts are coarser than the Voynich boxes (biases towards no effect, so the control's effect is if anything understated).
