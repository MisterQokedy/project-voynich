#!/usr/bin/env bash
# download pages (canvases 10..600 step 7, full res) + CATMuS model, then kraken segment+ocr to ALTO
set -uo pipefail
P=$VOYNICH_DIR/p3e
W=$HOME/p3e_work; mkdir -p $W/img $W/alto
BIN=$HOME/micromamba/envs/voynich-letters/bin
for i in $(seq 10 7 600); do
  n=$(printf %05d $((i+1)))
  [ -s $W/img/p$n.jpg ] || curl -s "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00092488_$n/full/full/0/default.jpg" -o $W/img/p$n.jpg
done
echo "== images $(ls $W/img | wc -l) $(date)"
cd $W
[ -n "$(ls $W/*.mlmodel 2>/dev/null)" ] || $BIN/kraken get 10.5281/zenodo.12743230 2>&1 | tail -3
ls ~/.local/share/htrmopo/*/ 2>/dev/null; find ~ -name "*.mlmodel" -newer $P/PREREG.md 2>/dev/null | head
echo "== model $(date)"
