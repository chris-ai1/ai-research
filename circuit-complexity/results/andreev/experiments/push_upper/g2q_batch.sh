#!/bin/bash
cd /tmp/andreev_gap/push_upper
for RT in "4 4" "2 6" "3 6" "4 6" "2 8" "5 5" "4 8" "6 6" "3 10" "6 8"; do
  timeout 1300 python3 -I g2q.py $RT 3 1200 q
done
