#!/bin/sh
# usage: run_one.sh <dataset>  -> logs/<dataset>.txt ; unchanged upstream run.sh
W=$(cd "$(dirname "$0")" && pwd)
export PATH=$W/.venv/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg
cd $W/D-Tracker/bin
s=$(date +%s); echo "START $(date -Is)"
nice -n 19 sh run.sh "$1"
rc=$?; echo "END $(date -Is) rc=$rc elapsed_s=$(( $(date +%s) - s ))"
