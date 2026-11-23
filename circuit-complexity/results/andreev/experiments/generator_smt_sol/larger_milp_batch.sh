#!/usr/bin/env bash
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
set -eu
cd /tmp/andreev_gap/generator_smt_sol
export PYTHONPATH=/tmp/pydeps OPENBLAS_NUM_THREADS=1
python3 sparse_milp.py --k 3 --m 6 --r 1 --seconds 300 --out milp_k3m6r1 > milp_k3m6r1.log 2>&1
python3 sparse_milp.py --k 4 --m 2 --r 1 --seconds 300 --out milp_k4m2r1 > milp_k4m2r1.log 2>&1
python3 sparse_milp.py --k 4 --m 3 --r 1 --seconds 300 --out milp_k4m3r1 > milp_k4m3r1.log 2>&1
