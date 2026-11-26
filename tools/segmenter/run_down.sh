#!/usr/bin/env bash
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd); V=$(dirname $(dirname "$HERE"))
PY=$HOME/micromamba/envs/voynich-letters/bin/python; REPO=$HOME/p2w/voynich-letters
W=$HOME/glyphseg_work; cp "$HERE"/*.py "$W"/; PS=$V/p3b/code/zl_parastart.json
echo "== feat noclip $(date)"; nice -n 10 "$PY" -I "$W/gsfeat.py" "$W/data" "$W/masks_model.npy" "$REPO" "$PS" "$W/feat_model"
mkdir -p $V/h10h/out; cp $W/feat_model/montage_* $V/h10h/out/
echo "== H10h $(date)"; nice -n 10 "$PY" -I "$V/h10h/code/h10f.py" "$W/feat_model" "$V/h10h/out" "$REPO" > $V/h10h/out/h10f.out 2>&1
echo "== feat clip $(date)"; nice -n 10 "$PY" -I "$W/gsfeat.py" "$W/data" "$W/masks_model.npy" "$REPO" "$PS" "$W/feat_clip" clip
mkdir -p $V/p3c/out; cp $W/feat_clip/montage_LM.png $V/p3c/out/
echo "== P3-c $(date)"; nice -n 10 "$PY" -I "$V/p3c/code/p3.py" "$W/feat_clip" "$V/p3c/out" 200 > $V/p3c/out/p3.out 2>&1
echo "== P4-S model masks $(date)"; bash $V/p4s_f105r/code/run.sh out_model "$W/masks_model.npy"
echo "== DONE $(date)"
