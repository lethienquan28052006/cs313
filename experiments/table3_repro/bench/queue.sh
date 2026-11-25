#!/bin/bash
# usage: bench/queue.sh "method:dataset" ...   runs via launch.sh, never more than 5 of OUR python jobs at once
W=$(cd "$(dirname "$0")/.." && pwd); cd $W
n_running(){ pgrep -u $(id -u) -f "bench.run --method|main.py --dataset" | wc -l; }
for job in "$@"; do
  while [ $(n_running) -ge 5 ]; do sleep 30; done
  bench/launch.sh ${job%%:*} ${job##*:} $EXTRA
  sleep 5
done
while [ $(pgrep -u $(id -u) -f "bench.run --method" | wc -l) -gt 0 ]; do sleep 60; done
echo "QUEUE DONE $(date -Is)"
