#!/usr/bin/env bash
# P3-e pipeline: kraken -> harvest -> GS train (2 folds) -> infer -> features (GS clip, box control) -> p3.py
set -uo pipefail
P=$VOYNICH_DIR; E=$P/p3e
W=$HOME/p3e_work; BIN=$HOME/micromamba/envs/voynich-letters/bin; PY=$BIN/python
MODEL=$HOME/.local/share/htrmopo/fef4968a-652b-5c8b-a6f0-1a1162abe8ec/catmus-medieval.mlmodel
echo "model $MODEL"
mkdir -p $W/alto $W/code; cp $E/code/*.py $P/glyphseg/code/train.py $P/glyphseg/code/infer.py $P/p3c/code/p3.py $W/code/
step=${1:-all}
if [[ $step == all || $step == ocr ]]; then
  echo "== ocr $(date)"
  for f in $W/img/*.jpg; do b=$(basename $f .jpg); [ -s $W/alto/$b.xml ] && continue
    $BIN/kraken -a -i $f $W/alto/$b.xml segment -bl ocr -m "$MODEL" > /dev/null 2>>$W/ocr.err || echo "ocr fail $b"; done
  echo "alto $(ls $W/alto | wc -l)"
fi
if [[ $step == all || $step == harvest ]]; then
  echo "== harvest $(date)"; $PY -I $W/code/harvest_ctl.py $W/img $W/alto $W/data | tail -4
fi
if [[ $step == all || $step == train ]]; then
  for f in 0 1; do echo "== train fold $f $(date)"; $PY -I $W/code/train.py $W/data $f $W/model_f$f 30 600 | tail -2; done
  echo "== infer $(date)"; $PY -I $W/code/infer.py $W/data $W | grep -v "^real fold" | tail -20; cp $W/eval_render.json $E/
fi
if [[ $step == all || $step == feat ]]; then
  echo "== feat $(date)"
  $PY -I $W/code/gsfeat_ctl.py $W/data $W/masks_model.npy $W/feat_clip clip
  $PY -I $W/code/gsfeat_ctl.py $W/data box $W/feat_box
  mkdir -p $E/out; cp $W/feat_clip/montage_real_LM.png $E/out/
fi
if [[ $step == all || $step == p3 ]]; then
  echo "== p3 GS clip $(date)"; P3_MINN=${P3_MINN:-80} $PY -I $W/code/p3.py $W/feat_clip $E/out/gs 200 | grep -E "group sizes|AUC|VERDICT"
  echo "== p3 box $(date)"; P3_MINN=${P3_MINN:-80} $PY -I $W/code/p3.py $W/feat_box $E/out/box 50 | grep -E "AUC|VERDICT"
fi
echo "== DONE $(date)"
