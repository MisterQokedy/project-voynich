#!/usr/bin/env bash
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
PY=$HOME/micromamba/envs/voynich-letters/bin/python
W=$HOME/glyphseg_work; cp "$HERE"/*.py "$W"/
for f in 0 1; do
  echo "== train fold $f $(date)"
  "$PY" -I "$W/train.py" "$W/data" $f "$W/model_f$f" ${1:-30} ${2:-600}
done
echo "== ALL DONE $(date)"
