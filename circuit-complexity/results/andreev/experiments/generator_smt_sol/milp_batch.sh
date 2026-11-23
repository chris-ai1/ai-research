#!/usr/bin/env bash
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
set -eu
cd /tmp/andreev_gap/generator_smt_sol
export PYTHONPATH=/tmp/pydeps OPENBLAS_NUM_THREADS=1
python3 sparse_milp.py --k 3 --m 4 --r 1 --seconds 180 --out milp_k3m4r1 > milp_k3m4r1.log 2>&1
python3 sparse_milp.py --k 3 --m 3 --r 2 --seconds 180 --out milp_k3m3r2 > milp_k3m3r2.log 2>&1
python3 sparse_milp.py --k 3 --m 3 --r -1 --seconds 180 --out milp_k3m3full > milp_k3m3full.log 2>&1
