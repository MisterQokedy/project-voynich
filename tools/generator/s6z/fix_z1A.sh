#!/bin/bash
# rerun group A for directions where it failed (small-half chunk issue), Z1a and Z1b
C=./work/s6z/code; O=./work/s6z/out
export S6Z_STAGES='{"pc":[0,0.95],"mu":[0,0.6],"keepE":[0,1],"tX":[0.3,3],"bJ":[0,5],"bD":[0,12]}' S6Z_GRP=A
for RUN in r0ab r0ba r1ab r1ba; do
  export S6Z_RUN=$RUN
  [ -s $O/../cache/${RUN}_A/ws2_ref.json ] || python3 $C/prepz.py > /tmp/s6z/log/prep_${RUN}_A.out 2>&1
  [ -s $O/z1a/$RUN/part_A_904.json ] || S6Z_TAG=z1a S6Z_NOSEARCH=1 python3 $C/pickz.py > /tmp/s6z/log/z1a_${RUN}_A.out 2>&1 &
  if [ ! -s $O/z1b/$RUN/part_A_904.json ]; then
    rm -rf /tmp/s6z/z1b/${RUN}_A
    for w in 0 1 2; do S6Z_TAG=z1b python3 $C/searchz.py 27 $w > /tmp/s6z/log/z1b_s_${RUN}_A_$w.out 2>&1 & done; wait
    S6Z_TAG=z1b python3 $C/pickz.py > $O/../z1/pick_${RUN}_A.out 2>&1
  fi; wait
  echo "$RUN A done $(date -u +%H:%M)"
done
python3 $C/mergez.py z1a A,B; python3 $C/mergez.py z1b A,B
echo DONE > /tmp/s6z/z1fix.done
