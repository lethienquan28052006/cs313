# D-Tracker reproduction — Table 3, D-Tracker column (GoogleTrends, 5 datasets)

Date: 2026-11-24. WORKDIR: `<WORKDIR>`
(used instead of `~/dtracker_repro` because work is restricted to the DataMining folder).
Paper: Higashiguchi et al., "D-Tracker", KDD 2025 (arXiv 2505.00242). Code: github.com/Higashiguchi-Shingo/D-Tracker @ `11c181d` (unmodified).

## Bottom line (updated after init=1 and Covid runs, 2026-11-24 16:37)

- **init=0 (run.sh as shipped):** 8 / 30 cells PASS.
- **init=1 (MDL grid-search init, as described in the paper):** 14 / 30 PASS. Pythonlib becomes almost exact (5/6 PASS; RMSE 1.426/1.549/1.780 vs paper 1.42/1.54/1.78). Device gets worse (0/6), because errors drop further *below* the paper.
- **Covid-19:** 0 / 6 PASS with seasonal_period=52 and 1 / 6 PASS with seasonal_period=7; both have errors *higher* than the paper.
- **Ranking:** In every row of every run, D-Tracker's MAE is still lower than the best baseline from the paper's Table 3. The one exception is VoD lf=13 with init=1, which is a tie at 2 decimals (see "MAE rank" below).
- Not reproduced within tolerance overall. The init hypothesis is partly confirmed: Pythonlib looks as if the paper used init=1. No single setting matches all datasets.

### Previous summary (init=0 only)

**Not reproduced within the agreed tolerance**: 8 / 30 cells PASS (rule: |Δ| ≤ 0.02 or ≤ 5%, units ×10⁻²).
Most numbers are within about 15% of the paper. The closest exceptions are programming MAE (all 3 PASS) and vod MAE at lf 13/26. Errors are on average **lower** than the paper for chatapp, device and pythonlib, and **higher** for vod and programming RMSE.
The prime suspect is identified (see Hypotheses §1): `run.sh` uses `init=0` → fixed initial ranks (3,2,1) instead of the paper's MDL grid search.

## Environment

- Python 3.13.11 (system `python3`), venv `.venv` (no system/user packages touched).
- Key packages: numpy 2.5.5, pandas 3.1.1, scipy 1.18.1, tensorly 0.10.0, lmfit 1.3.4, statsmodels 0.15.0, scikit-learn 1.9.1, matplotlib 3.11.2, seaborn 0.13.2, psutil 7.2.2, torch 2.15.0+cpu. Full `pip freeze`: `env.txt`.
- `numpy<2` was not needed (no numpy-2 errors) and has no wheel for Python 3.13 anyway.
- Machine: 32 cores, 62 GiB RAM; preflight 19 GB disk free.

## Commands

```sh
python3 -m venv .venv
.venv/bin/pip install -r D-Tracker/requirement.txt lmfit psutil
.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
# per dataset, via run_one.sh (venv on PATH, OMP/OPENBLAS/MKL_NUM_THREADS=1, MPLBACKEND=Agg):
nice -n 19 sh D-Tracker/bin/run.sh <dataset>     # unchanged run.sh: lc=104 lf=39 init=0 rankupdate=1 outlier=1 stl=0
#   -> main.py ... ; accuracy.py --lf 13/26/39 --start_timestep 312 --end_timestep 636
.venv/bin/python parse_results.py                # -> logs/table.md
```

Launch: `nohup ./run_one.sh <ds> > logs/<ds>.txt 2>&1 &` (5 jobs in parallel). **Deviation:** started with
`nohup` only, not `setsid` (the setsid rule was added later); PIDs recorded afterwards in `pids/`. All jobs finished.

## Runtime (wall clock, 5 jobs in parallel, nice 19, 1 thread each)

| dataset | start | end | elapsed | rc | model switches |
|---|---|---|---|---|---|
| pythonlib | 13:14:44 | 13:29:01 | 857 s (14.3 min) | 0 | 28 |
| programming | 13:15:48 | 13:30:07 | 859 s (14.3 min) | 0 | 11 |
| vod | 13:15:48 | 13:44:08 | 1700 s (28.3 min) | 0 | 32 |
| device | 13:15:48 | 13:54:28 | 2320 s (38.7 min) | 0 | 12 |
| chatapp | 13:15:48 | 14:18:07 | 3739 s (62.3 min) | 0 | 30 |

No Tracebacks. Warnings only: pandas `obj.round has no effect` (utils.py:97) and matplotlib "more than 20 figures".

## Comparison (×10⁻², code value × 100)

| dataset | lf | MAE paper | MAE repro | Δ% | | RMSE paper | RMSE repro | Δ% | |
|---|---|---|---|---|---|---|---|---|---|
| Device | 13 | 0.84 | 0.775 | −7.7% | FAIL | 1.82 | 1.716 | −5.7% | FAIL |
| Device | 26 | 0.90 | 0.847 | −5.9% | FAIL | 1.95 | 1.879 | −3.7% | PASS |
| Device | 39 | 0.97 | 0.916 | −5.6% | FAIL | 2.18 | 2.090 | −4.1% | PASS |
| Pythonlib | 13 | 0.27 | 0.257 | −4.9% | PASS | 1.42 | 1.192 | −16.1% | FAIL |
| Pythonlib | 26 | 0.32 | 0.283 | −11.5% | FAIL | 1.54 | 1.328 | −13.8% | FAIL |
| Pythonlib | 39 | 0.37 | 0.324 | −12.3% | FAIL | 1.78 | 1.560 | −12.4% | FAIL |
| VoD | 13 | 0.53 | 0.547 | +3.1% | PASS | 1.58 | 1.681 | +6.4% | FAIL |
| VoD | 26 | 0.59 | 0.614 | +4.1% | PASS | 1.83 | 1.959 | +7.0% | FAIL |
| VoD | 39 | 0.63 | 0.665 | +5.6% | FAIL | 2.02 | 2.209 | +9.4% | FAIL |
| Chatapp | 13 | 0.28 | 0.254 | −9.1% | FAIL | 0.83 | 0.780 | −6.0% | FAIL |
| Chatapp | 26 | 0.34 | 0.302 | −11.1% | FAIL | 1.01 | 0.957 | −5.3% | FAIL |
| Chatapp | 39 | 0.41 | 0.354 | −13.7% | FAIL | 1.24 | 1.155 | −6.9% | FAIL |
| Language | 13 | 0.31 | 0.315 | +1.7% | PASS | 0.97 | 1.020 | +5.1% | FAIL |
| Language | 26 | 0.35 | 0.349 | −0.3% | PASS | 1.14 | 1.274 | +11.8% | FAIL |
| Language | 39 | 0.40 | 0.387 | −3.2% | PASS | 1.32 | 1.561 | +18.3% | FAIL |

Full table with absolute Δ: `logs/table.md`. PASS = |Δ| ≤ 0.02 or |Δ|/paper ≤ 5%.

Pattern: of the 22 FAILs, 15 are *better* than the paper (chatapp, device, pythonlib) and 7 are worse (vod, programming RMSE).
Error still grows with horizon in every dataset, as in the paper.

## Hypotheses for the gaps (not verified unless stated)

1. **Initialization (verified in code, effect unverified).** `run.sh` sets `init=0`. In `dtracker.py:517-530`, `init=0` skips the grid search and uses defaults `init_dk=3, init_dl=2, init_ds=1` (`dtracker.py:491`); all 5 logs show `Best dk: 3, dl: 2, ds: 1`. The paper says the initial ranks come from an MDL grid search over (d_k, d_l) ∈ [2,4], d_s ∈ [0,4]. Note that the code's grid uses `max_ds=2` (main.py default), not 4. RankUpdate (`rankupdate=1`) changes ranks later, so the start point affects the whole stream. → Test with Task 6 (init=1), pending approval.
2. **Package version drift.** Pyc files in the repo show Python 3.10/3.11; we use 3.13 + numpy 2.5 / pandas 3.1 / tensorly 0.10 / lmfit 1.3.4 / scipy 1.18. Changes in NNLS/Tucker/HALS, lmfit optimizers or `odeint` tolerances can shift fitted parameters and model-switch decisions (11–32 switches per stream, each one a branching point).
3. **Data preprocessing.** pandas 3 warns that `round("D")` on datetime has no effect (utils.py:97); with the older pandas the authors used, it may have behaved differently. This was not checked. The repo data has 48 locations while the paper's table gives 50, so the released data may differ from what produced Table 3.
4. **Run-to-run randomness.** Each dataset ran once. Thread count (1) and BLAS build can change float results; the size of this effect was not measured.
5. **Evaluation window.** We used run.sh's 312…636 step 4 (= test 2016-01 … 2022-03). If the paper used different bounds, the averages differ. This cannot be checked from the paper text.

## init=1 runs (Task 6)

Script: `run_variant.sh <ds>` = run.sh flags with `--init 1`, run in `D-Tracker-init1/` (unchanged copy of code + data). init=0 results backed up first to `result_backup_init0_20261124/` (655 MB). Launched with `setsid nohup`; pids in `pids/<ds>_init1.pid` (wrapper) and `pids/<ds>_init1.main.pid`.
Deviation: `$!` after `setsid` held a PID of setsid's own fork (job-control process-group leader), so pid files were rewritten via `pgrep` right after launch.

Note: the code's grid search covers d_k, d_l ∈ [2,4] and d_s ∈ [0, max_ds=2] (main.py default). The paper describes d_s ∈ [0,4].

| dataset | init ranks chosen (dk, dl, ds) | init=0 ranks | start | end | elapsed | rc | model switches (init=0 → init=1) |
|---|---|---|---|---|---|---|---|
| pythonlib | (2, 2, 0) | (3, 2, 1) | 14:35:46 | 14:49:28 | 822 s | 0 | 28 → 37 |
| programming | (4, 4, 0) | (3, 2, 1) | 14:35:46 | 15:18:31 | 2565 s | 0 | 11 → 12 |
| vod | (2, 3, 2) | (3, 2, 1) | 14:35:46 | 15:25:26 | 2980 s | 0 | 32 → 30 |
| device | (2, 3, 2) | (3, 2, 1) | 14:35:46 | 15:27:06 | 3080 s | 0 | 12 → 13 |
| chatapp | (4, 3, 2) | (3, 2, 1) | 14:35:46 | 16:06:55 | 5469 s | 0 | 30 → 31 |

PASS per dataset (of 6): init=0 → init=1: device 2→0, pythonlib 1→5, vod 2→3, chatapp 0→3, programming 3→3.

## Covid-19 (Task 5)

Script: `run_covid.sh <sp>`; runs in separate unchanged code copies `D-Tracker-covid-sp52/` and `D-Tracker-covid-sp7/` (result path has no seasonal_period, so the copies keep the two variants apart). Logs `logs/covid_sp52.txt`, `logs/covid_sp7.txt`; pids `pids/covid_sp{52,7}.pid`.

```sh
main.py --dataset covid --lc 56 --lf 21 --start_date 2020-01-01 --end_date 2022-09-30 --seasonal_period <52|7> \
        --init 0 --rankupdate 1 --ablation_seasonal 0 --ablation_diffusion 0 --outlier 1 --stl 0
accuracy.py --dataset covid --lc 56 --lf 7/14/21 --start_timestep 400 --end_timestep 968 --rankupdate 1 --outlier 1 --stl 0
```

- Parameter name `--seasonal_period` verified in `main.py:29` (default 52). `stl_period` left at its default of 26 in both variants (it is not used when stl=0 and also appears in the result path that accuracy.py reads).
- Tensor: 990 days × 2 keys × 48 locations (paper: 990 × 2 × 50).
- **Assumptions:** start_timestep 400 = first saved t on grid 56+4k at or after 2021-02-01 (index 397; paper: train 2020, val Jan 2021); end_timestep 968 exclusive (mirrors run.sh's 636 = last saved t, excluded). Forecasts were saved for t = 60…968.
- init=0 → initial dk=3 > 2 keywords: tensorly warns `Trying to compute SVD with n_eigenvecs=3, which is larger than min(matrix.shape)=2. Setting n_eigenvecs to 2.` (191× for n_eigenvecs=3 and 45× for n_eigenvecs=4 in the sp52 log). The default init is not valid for a 2-key tensor; init=1 (grid starts at dk=2) was **not** run for Covid.

| variant | start | end | elapsed | rc | model switches |
|---|---|---|---|---|---|
| seasonal_period=52 | 16:08:18 | 16:37:20 | 1742 s | 0 | 101 |
| seasonal_period=7 | 16:08:18 | 16:32:34 | 1456 s | 0 | 70 |

## Full comparison: paper vs init=0 vs init=1 (×10⁻²)

`v` = PASS/FAIL (|Δ| ≤ 0.02 or ≤ 5%). Last column: is D-Tracker's MAE strictly below the best **baseline** MAE in the paper's Table 3? Values compared at the paper's 2-decimal precision. Baseline numbers come from the paper and were not re-run; they were extracted from the arXiv HTML by a summarizer. The D-Tracker column of that extraction equals the user-provided values, but the baseline columns were not checked cell by cell.

| dataset | lf | metric | paper | init=0 | v | init=1 | v | best baseline (MAE) | #1 MAE? paper / init=0 / init=1 |
|---|---|---|---|---|---|---|---|---|---|
| device | 13 | MAE | 0.84 | 0.775 | FAIL | 0.765 | FAIL | DISMO 1.08 | yes / yes / yes |
| device | 13 | RMSE | 1.82 | 1.716 | FAIL | 1.697 | FAIL |  |  |
| device | 26 | MAE | 0.90 | 0.847 | FAIL | 0.832 | FAIL | DISMO 1.19 | yes / yes / yes |
| device | 26 | RMSE | 1.95 | 1.879 | PASS | 1.834 | FAIL |  |  |
| device | 39 | MAE | 0.97 | 0.916 | FAIL | 0.895 | FAIL | PatchTST 1.21 | yes / yes / yes |
| device | 39 | RMSE | 2.18 | 2.090 | PASS | 2.037 | FAIL |  |  |
| pythonlib | 13 | MAE | 0.27 | 0.257 | PASS | 0.299 | FAIL | CoST 0.40 | yes / yes / yes |
| pythonlib | 13 | RMSE | 1.42 | 1.192 | FAIL | 1.426 | PASS |  |  |
| pythonlib | 26 | MAE | 0.32 | 0.283 | FAIL | 0.324 | PASS | CoST 0.45 | yes / yes / yes |
| pythonlib | 26 | RMSE | 1.54 | 1.328 | FAIL | 1.549 | PASS |  |  |
| pythonlib | 39 | MAE | 0.37 | 0.324 | FAIL | 0.366 | PASS | Autoformer 0.42 | yes / yes / yes |
| pythonlib | 39 | RMSE | 1.78 | 1.560 | FAIL | 1.780 | PASS |  |  |
| vod | 13 | MAE | 0.53 | 0.547 | PASS | 0.555 | PASS | DISMO/Autoformer 0.56 | yes / yes / tie |
| vod | 13 | RMSE | 1.58 | 1.681 | FAIL | 1.764 | FAIL |  |  |
| vod | 26 | MAE | 0.59 | 0.614 | PASS | 0.616 | PASS | DISMO 0.66 | yes / yes / yes |
| vod | 26 | RMSE | 1.83 | 1.959 | FAIL | 2.008 | FAIL |  |  |
| vod | 39 | MAE | 0.63 | 0.665 | FAIL | 0.657 | PASS | DISMO 0.78 | yes / yes / yes |
| vod | 39 | RMSE | 2.02 | 2.209 | FAIL | 2.175 | FAIL |  |  |
| chatapp | 13 | MAE | 0.28 | 0.254 | FAIL | 0.256 | FAIL | DISMO/PatchTST 0.47 | yes / yes / yes |
| chatapp | 13 | RMSE | 0.83 | 0.780 | FAIL | 0.801 | PASS |  |  |
| chatapp | 26 | MAE | 0.34 | 0.302 | FAIL | 0.306 | FAIL | DISMO 0.48 | yes / yes / yes |
| chatapp | 26 | RMSE | 1.01 | 0.957 | FAIL | 0.988 | PASS |  |  |
| chatapp | 39 | MAE | 0.41 | 0.354 | FAIL | 0.359 | FAIL | DISMO 0.50 | yes / yes / yes |
| chatapp | 39 | RMSE | 1.24 | 1.155 | FAIL | 1.215 | PASS |  |  |
| programming | 13 | MAE | 0.31 | 0.315 | PASS | 0.300 | PASS | Autoformer 0.37 | yes / yes / yes |
| programming | 13 | RMSE | 0.97 | 1.020 | FAIL | 0.918 | FAIL |  |  |
| programming | 26 | MAE | 0.35 | 0.349 | PASS | 0.334 | PASS | Autoformer 0.41 | yes / yes / yes |
| programming | 26 | RMSE | 1.14 | 1.274 | FAIL | 1.174 | PASS |  |  |
| programming | 39 | MAE | 0.40 | 0.387 | PASS | 0.373 | FAIL | CoST 0.49 | yes / yes / yes |
| programming | 39 | RMSE | 1.32 | 1.561 | FAIL | 1.482 | FAIL |  |  |

Covid-19 (init=0; columns = seasonal_period 52 | seasonal_period 7)

| dataset | lf | metric | paper | sp=52 | v | sp=7 | v | best baseline (MAE) | #1 MAE? paper / sp=52 / sp=7 |
|---|---|---|---|---|---|---|---|---|---|
| covid | 7 | MAE | 0.47 | 0.649 | FAIL | 0.594 | FAIL | Autoformer 1.10 | yes / yes / yes |
| covid | 7 | RMSE | 1.40 | 1.956 | FAIL | 1.717 | FAIL |  |  |
| covid | 14 | MAE | 0.70 | 0.895 | FAIL | 0.814 | FAIL | Autoformer 1.18 | yes / yes / yes |
| covid | 14 | RMSE | 2.42 | 2.922 | FAIL | 2.447 | PASS |  |  |
| covid | 21 | MAE | 0.98 | 1.176 | FAIL | 1.076 | FAIL | Autoformer 1.25 | yes / yes / yes |
| covid | 21 | RMSE | 3.65 | 4.089 | FAIL | 3.375 | FAIL |  |  |


### MAE rank vs. baselines: notes

- **VoD lf=13** (best baselines DISMO = Autoformer = 0.56): paper D-Tracker 0.53 → #1. init=0 0.5466 → 0.55 < 0.56 → #1, margin 0.013. init=1 0.5555 → rounds to 0.56 → **tie** at the paper's precision; the unrounded value is 0.0045 below 0.56. This is the closest call in the whole table.
- Next-smallest margins: VoD lf=26 (DISMO 0.66): init=1 0.616 (−0.044) and init=0 0.614 (−0.046). Pythonlib lf=39 init=1 0.366 vs Autoformer 0.42 (−0.054). Programming lf=13 init=0 0.315 vs Autoformer 0.37 (−0.055).
- All other rows, Covid included, have a margin above 0.055.

## Pandas warning (verbatim, once per run, in every log)

```
<WORKDIR>/D-Tracker/src/utils.py:97: UserWarning: obj.round has no effect with datetime, timedelta, or period dtypes. Use obj.dt.round(...) instead.
  tmp[time_key] = tmp[time_key].round(sampling_rate)
```

(The path changes per code copy, e.g. `D-Tracker-init1/src/utils.py:97`.) Meaning: in pandas 3.1.1, `Series.round("D")` on a datetime column is a no-op, so dates are **not** rounded to the day. The input dates are already at day/week resolution (weekly Sundays for GoogleTrends, daily for Covid), and the tensors have the expected lengths (678 weeks, 990 days). So the no-op probably changes nothing, but this was not verified against an older pandas.

Other warnings: matplotlib `More than 20 figures have been opened` (memory only); tensorly SVD clipping on Covid (above).

## Disk

WORKDIR uses 3.6 GB (results 655 MB init=0 + 655 MB backup + 659 MB init=1 + 120 MB Covid, plus the venv). The free space on `/` dropped from 19 GB to 8.8 GB during the session, most of it from other users. The backup can be deleted once the init=0 results are no longer needed.

## Not done / pending approval

- Covid with init=1 (the default init dk=3 is larger than the 2 keys); Covid with other start/end windows.
- Repeated runs to measure run-to-run randomness.
- Baselines (DISMO, FluxCube, PatchTST, Autoformer, DeepAR, LaST, CoST) — out of scope, need external repos + GPU.

## Files

`run_one.sh`, `run_variant.sh`, `run_covid.sh`, `parse_results.py` (`--compare`), `test_parse_results.py` (unittest 9/9 OK), `logs/<ds>[_init1].txt`, `logs/covid_sp{52,7}.txt`, `logs/table.md`, `logs/compare.md`, `pids/`, `env.txt`, `progress.md`, results in `D-Tracker/result/<ds>/...`.
