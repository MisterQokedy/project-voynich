#!/bin/bash
# S6-Z1: per-direction prep (A,B) -> Z1a (no search) -> Z1b (search 2x40 per group) ; restartable per run.
C=./work/s6z/code; O=./work/s6z/out
export S6Z_STAGES='{"pc":[0,0.95],"mu":[0,0.6],"keepE":[0,1],"tX":[0.3,3],"bJ":[0,5],"bD":[0,12]}'
for RUN in orig swap r0ab r0ba r1ab r1ba; do
  export S6Z_RUN=$RUN; mkdir -p /tmp/s6z/log
  for G in A B; do [ -s $O/../cache/${RUN}_$G/ws2_ref.json ] || S6Z_GRP=$G python3 $C/prepz.py > /tmp/s6z/log/prep_${RUN}_$G.out 2>&1 & done; wait
  if [ ! -s $O/z1a/$RUN/part_B_904.json ]; then
    for G in A B; do S6Z_GRP=$G S6Z_TAG=z1a S6Z_NOSEARCH=1 python3 $C/pickz.py > /tmp/s6z/log/z1a_${RUN}_$G.out 2>&1 & done; wait
  fi
  if [ ! -s $O/z1b/$RUN/part_B_904.json ]; then
    rm -rf /tmp/s6z/z1b/${RUN}_A /tmp/s6z/z1b/${RUN}_B
    for G in A B; do for w in 0 1; do S6Z_GRP=$G S6Z_TAG=z1b python3 $C/searchz.py 40 $w > /tmp/s6z/log/z1b_s_${RUN}_${G}_$w.out 2>&1 & done; done; wait
    for G in A B; do S6Z_GRP=$G S6Z_TAG=z1b python3 $C/pickz.py > $O/../z1/pick_${RUN}_$G.out 2>&1 & done; wait
  fi
  echo "$RUN done $(date -u +%H:%M)"
done
python3 $C/mergez.py z1a A,B; python3 $C/mergez.py z1b A,B
echo DONE > /tmp/s6z/z1.done
