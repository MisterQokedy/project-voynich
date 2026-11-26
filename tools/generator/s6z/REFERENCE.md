# S6-Z reference generator (frozen 26 Nov 2026) = S6-Z1b

**What it is.** S6-Y (copy-and-vary + slot words + line rules + junction rules + page drift) run **separately for Currier A and Currier B**. Each language builds all its tables from its own FIT pages and has its own fitted copy, mutation, ending-keep, line-end, junction and drift settings. Pages are generated per language and merged back into the 202 manuscript slots.

**Files.**
- Settings per direction and language: `out/S6Z_reference/<run>/best_<A|B>.json` (frozen copy of `out/z1b/`).
- Held-out texts: `out/S6Z_reference/<run>/gen_<900..904>.json` (202 slots; score TEST pages only).
- Code: `code/shimz.py` (direction + language isolation), `code/basez.py` (generator), `code/pickz.py` (generation), `code/mergez.py`, `code/scorez.py` (24-stat rule + controls + A–B gap).
- Regenerate one language for one direction: `S6Z_RUN=<run> S6Z_GRP=<A|B> S6Z_TAG=<new> S6Z_NOSEARCH=1 S6Z_BASE='./work/s6z/out/S6Z_reference/{RUN}/best_{GRP}.json' python3 code/pickz.py` (needs `pip install optuna scipy`; run `code/prepz.py` once per run/group first, it fills `cache/`).

**Scores (6 directions × 5 seeds, held-out TEST, split-independent bands).** Mean 20.83/24; 5/6 directions generalise (the first S6 version to pass the any-split rule); every text beats Timm+rules (6–15) and shuffle (11–13) controls. Page drift (stat 26) is inherited from S6-Y.

See `REPORT.md` for what it reproduces and what it still misses.

**FROZEN FOR GOOD (26 Nov 2026, after S6-Z6).** The last try (Z6, long-word gallows habit, `z6/REPORT.md`) reached 21.00 vs 20.83, inside seed noise, so S6-Z1b is final for the paper. No further generator mechanisms.
