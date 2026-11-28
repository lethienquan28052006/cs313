#!/bin/sh
# usage: run_ablation.sh <dataset> <variant>   variant: nodiff | noseason | nooutlier | norank
# Fig.3 ablation on top of the official init=0 config (run.sh / run_covid.sh sp=52). Unchanged code.
# After scoring, the bulky forecast/ snapshots of THIS variant are deleted (disk is tight); log/ and model/ kept.
W=$(cd "$(dirname "$0")" && pwd)
ds=$1; v=$2
R=1; S=0; D=0; O=1
case $v in nodiff) D=1;; noseason) S=1;; nooutlier) O=0;; norank) R=0;; *) echo "bad variant $v"; exit 2;; esac
export PATH=$W/.venv/bin:$PATH OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 MPLBACKEND=Agg
if [ "$ds" = covid ]; then
  cd $W/D-Tracker-covid-sp52/src || exit 1
  LC=56; LF=21; HS=7/14/21; ST=400; EN=968; EXTRA="--start_date 2020-01-01 --end_date 2022-09-30 --seasonal_period 52"
else
  cd $W/D-Tracker/src || exit 1
  LC=104; LF=39; HS=13/26/39; ST=312; EN=636; EXTRA=""
fi
s=$(date +%s); echo "START $(date -Is) dataset=$ds variant=$v rankupdate=$R ablation_s=$S ablation_d=$D outlier=$O"
nice -n 19 python3 main.py --dataset $ds --lc $LC --lf $LF $EXTRA --init 0 --rankupdate $R \
  --ablation_seasonal $S --ablation_diffusion $D --outlier $O --stl 0 || { echo "END $(date -Is) rc=$? main failed"; exit 1; }
nice -n 19 python3 accuracy.py --dataset $ds --lc $LC --lf $HS --start_timestep $ST --end_timestep $EN \
  --rankupdate $R --ablation_seasonal $S --ablation_diffusion $D --outlier $O --stl 0
rc=$?
rm -rf "../result/$ds/lc=$LC/stl=26/rankupdate=$R/ablation_s=$S/ablation_d=$D/outlier=$O/stl=0/forecast"
echo "END $(date -Is) rc=$rc elapsed_s=$(( $(date +%s) - s ))"
