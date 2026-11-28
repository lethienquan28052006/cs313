#!/bin/bash
# usage: ablation_queue.sh "ds:variant" ...  ; <=5 of our python jobs; waits if disk < 5.5G free
W=$(cd "$(dirname "$0")" && pwd); cd $W
n_running(){ pgrep -u $(id -u) -f "bench.run --method|main.py --dataset" | wc -l; }
free_g(){ df -BG --output=avail ~ | tail -1 | tr -dc 0-9; }
for job in "$@"; do
  ds=${job%%:*}; v=${job##*:}; name=abl_${ds}_${v}
  while [ $(n_running) -ge 5 ] || [ $(free_g) -lt 6 ]; do sleep 30; done
  setsid -f nohup sh run_ablation.sh $ds $v > logs/$name.txt 2>&1 < /dev/null
  sleep 3
  pgrep -u $(id -u) -f "run_ablation.sh $ds $v" | head -1 > pids/$name.pid
  echo "$name pid=$(cat pids/$name.pid) $(date -Is) free=$(free_g)G"
  sleep 5
done
while [ $(pgrep -u $(id -u) -f "run_ablation.sh" | wc -l) -gt 0 ]; do sleep 60; done
echo "ABLATION QUEUE DONE $(date -Is)"
