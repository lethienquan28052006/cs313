#!/bin/sh
# usage: run_covid.sh <seasonal_period> [init=0]  -> runs in D-Tracker-covid-sp<sp>[-init1] (unchanged code copy)
W=$(cd "$(dirname "$0")" && pwd)
SP=$1
INIT=${2:-0}
SUF=""; [ "$INIT" = 1 ] && SUF=-init1
export PATH=$W/.venv/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg
cd $W/D-Tracker-covid-sp$SP$SUF/src || exit 1
s=$(date +%s); echo "START $(date -Is) covid seasonal_period=$SP init=$INIT"
nice -n 19 python3 main.py --dataset covid --lc 56 --lf 21 --start_date 2020-01-01 --end_date 2022-09-30 \
  --seasonal_period $SP --init $INIT --rankupdate 1 --ablation_seasonal 0 --ablation_diffusion 0 --outlier 1 --stl 0 \
  || { echo "END $(date -Is) rc=$? main failed"; exit 1; }
# start 400 = first t on grid 56+4k >= 2021-02-01 (idx 397); end 968 exclusive (mirrors run.sh 636). ASSUMPTION.
nice -n 19 python3 accuracy.py --dataset covid --lc 56 --lf 7/14/21 --start_timestep 400 --end_timestep 968 \
  --rankupdate 1 --outlier 1 --stl 0
rc=$?; echo "END $(date -Is) rc=$rc elapsed_s=$(( $(date +%s) - s ))"
