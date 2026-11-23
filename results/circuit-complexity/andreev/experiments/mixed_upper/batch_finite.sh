#!/bin/bash
cd /tmp/andreev_gap/mixed_upper
for m in 1 2 3 4 5 6 7 8 10 12; do
  for pool in axis bsrich half; do
    timeout 1200 python3 -I exp_finite.py --k 2 --m $m --pool $pool --milp 300 2>&1 | grep -E "RESULT|MILP|Traceback|Error" 
  done
done
