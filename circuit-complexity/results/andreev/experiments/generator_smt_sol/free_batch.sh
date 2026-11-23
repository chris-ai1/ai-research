#!/usr/bin/env bash
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
set -eu
cd /tmp/andreev_gap/generator_smt_sol
export PYTHONPATH=/tmp/pydeps OPENBLAS_NUM_THREADS=1
for row in '2 6 0 6' '2 8 0 8' '3 4 0 8' '4 2 1 12' '4 3 1 16' '3 6 1 18'; do
 read -r k m r s <<< "$row"
 name=free_k${k}m${m}r${r}s${s}
 python3 engine.py --k "$k" --m "$m" --r "$r" --S "$s" --budget 100 --timeout 20000 --out "$name" > "$name.log" 2>&1
done
