# all remaining canvases 1..621, 4 parallel downloads, then OCR + harvest
W=$HOME/p3e_work
seq 1 621 | xargs -P4 -I{} bash -c 'n=$(printf %05d {}); f='$W'/img/p$n.jpg; [ -s $f ] || curl -s --retry 3 "https://api.digitale-sammlungen.de/iiif/image/v2/bsb00092488_$n/full/full/0/default.jpg" -o $f'
echo "== images $(ls $W/img | wc -l) $(date)"
bash $VOYNICH_DIR/p3e/code/run.sh ocr
bash $VOYNICH_DIR/p3e/code/run.sh harvest
~/micromamba/envs/voynich-letters/bin/python -I $VOYNICH_DIR/p3e/code/cnt.py
echo "== FETCH2 DONE $(date)"
