#!/usr/bin/env bash
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
set -eu
cd /tmp/andreev_gap/generator_smt_sol
export PYTHONPATH=/tmp/pydeps OPENBLAS_NUM_THREADS=1
python3 sparse_milp.py --k 3 --m 4 --r -1 --seconds 300 --out milp_k3m4full > milp_k3m4full.log 2>&1
python3 sparse_milp.py --k 3 --m 6 --r -1 --seconds 300 --out milp_k3m6full > milp_k3m6full.log 2>&1
