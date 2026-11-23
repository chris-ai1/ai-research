#!/bin/bash
# usage: bench.sh label mode k m S tl extra-args...   -> one line
label=$1; mode=$2; k=$3; m=$4; S=$5; tl=$6; shift 6
out=$(timeout $((tl+60)) python3 -I /tmp/andreev_gap/verify/${SCRIPT:-min_circuit.py} --mode $mode --k $k --m $m --S $S --tl $tl "$@" | grep RESULT)
echo "$label | $out"
