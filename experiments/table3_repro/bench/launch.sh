#!/bin/sh
# usage: bench/launch.sh <method> <dataset> [extra args]  -> logs/bl_<method>_<ds><tag>.txt, pids/bl_<method>_<ds><tag>.pid
W=$(cd "$(dirname "$0")/.." && pwd)
m=$1; ds=$2; shift 2
tag=""; case "$*" in *--pilot*) tag=_pilot;; esac
name=bl_${m}_${ds}${tag}
cd $W
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CUDA_VISIBLE_DEVICES="" MPLBACKEND=Agg PYTHONWARNINGS=ignore \
  setsid -f nohup nice -n 19 $W/.venv/bin/python -u -m bench.run --method $m --dataset $ds "$@" > logs/$name.txt 2>&1 < /dev/null
sleep 2
pgrep -u $(id -u) -f "bench.run --method $m --dataset $ds( |$)" | head -1 > pids/$name.pid
echo "$name pid=$(cat pids/$name.pid)"
