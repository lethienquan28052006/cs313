#!/bin/sh
# usage: run_variant.sh <dataset>  -> init=1 run in D-Tracker-init1 (unchanged code); flags = run.sh except --init 1
W=$(cd "$(dirname "$0")" && pwd)
export PATH=$W/.venv/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg
cd $W/D-Tracker-init1/src || exit 1
s=$(date +%s); echo "START $(date -Is) dataset=$1 init=1"
nice -n 19 python3 main.py --dataset "$1" --lc 104 --lf 39 --init 1 --rankupdate 1 \
  --ablation_seasonal 0 --ablation_diffusion 0 --outlier 1 --stl 0 || { echo "END $(date -Is) rc=$? main failed"; exit 1; }
nice -n 19 python3 accuracy.py --dataset "$1" --lc 104 --lf 13/26/39 --start_timestep 312 --end_timestep 636 \
  --rankupdate 1 --outlier 1 --stl 0
rc=$?; echo "END $(date -Is) rc=$rc elapsed_s=$(( $(date +%s) - s ))"
