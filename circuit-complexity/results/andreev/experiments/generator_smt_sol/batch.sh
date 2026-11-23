#!/usr/bin/env bash
# Copyright (c) 2026 Christian Reitwiessner
# Authors: Christian Reitwiessner
set -eu
cd /tmp/andreev_gap/generator_smt_sol
export PYTHONPATH=/tmp/pydeps OPENBLAS_NUM_THREADS=1
python3 lp_campaign.py --k 3 --m 3 --r 1 --rounds 5 --out lp_k3m3r1 > lp_k3m3r1.log 2>&1
python3 lp_campaign.py --k 3 --m 4 --r 1 --rounds 5 --out lp_k3m4r1 > lp_k3m4r1.log 2>&1
python3 lp_campaign.py --k 3 --m 6 --r 1 --rounds 5 --out lp_k3m6r1 > lp_k3m6r1.log 2>&1
python3 lp_campaign.py --k 4 --m 3 --r 1 --rounds 5 --out lp_k4m3r1 > lp_k4m3r1.log 2>&1
python3 lp_campaign.py --k 3 --m 4 --r -1 --rounds 4 --out lp_k3m4full > lp_k3m4full.log 2>&1
python3 lp_campaign.py --k 3 --m 6 --r -1 --rounds 3 --out lp_k3m6full > lp_k3m6full.log 2>&1
