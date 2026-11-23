#!/bin/bash
cd /tmp/andreev_gap/work
until [ $(ls m2_all_*.json 2>/dev/null | wc -l) -ge 12 ]; do sleep 20; done
echo done
