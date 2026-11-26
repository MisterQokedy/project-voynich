#!/bin/bash
# S6-Y: six directions in sequence. Restartable: a run whose out/<run>/gen_S6-Y_904.json exists is skipped.
C=./work/s6y/code; O=./work/s6y/out
for RUN in orig swap r0ab r0ba r1ab r1ba; do
  export S6Y_RUN=$RUN
  [ -s $O/$RUN/gen_S6-Y_904.json ] && continue
  rm -rf /tmp/s6y/$RUN; mkdir -p /tmp/s6y/$RUN $O/$RUN; cd /tmp/s6y/$RUN
  python3 $C/prep.py > $O/$RUN/prep.out 2>&1
  for w in 0 1 2 3; do python3 $C/search.py 40 $w > w$w.out 2> w$w.err & done; wait
  python3 $C/pick.py > $O/$RUN/pick.out 2>&1
done
echo DONE > /tmp/s6y/chain.done
