#!/bin/bash
# Fair benchmark: original-equivalent encoding vs improved defaults, same seeds, run concurrently.
# usage: bench_fair.sh MODE k,m S SEEDS...
cd /tmp/andreev_gap/verify_opus; mkdir -p fair
mode=$1; km=$2; S=$3; shift 3
for seed in "$@"; do
  timeout 3000 python3 -I min_circuit.py $mode $km --only $S --tl 2700 --seed $seed --sym none --tactic qflra --order natural > fair/${mode}_${km}_${S}_orig_$seed.log 2>&1 &
  timeout 3000 python3 -I min_circuit.py $mode $km --only $S --tl 2700 --seed $seed > fair/${mode}_${km}_${S}_new_$seed.log 2>&1 &
done
wait
