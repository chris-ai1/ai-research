#!/bin/sh
# usage: run_search.sh N STEPS RESTARTS "x1 x2 ..."   (runs all jobs in parallel, one process each)
N=$1; STEPS=$2; R=$3; XS=$4; HERE=$(dirname "$0")
for name in direct derivative; do for x in $XS; do for r in $(seq 0 $((R-1))); do
  echo "$name $N $x $STEPS $((17*r+x))"
done; done; done | OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 xargs -P 18 -L 1 ${PY:-python3} -I "$HERE/derivative_search.py"
