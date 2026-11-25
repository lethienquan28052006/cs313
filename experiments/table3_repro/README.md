# Table 3 reproduction: D-Tracker + 5 baselines

Re-runs the **official D-Tracker code** (unmodified, commit `11c181d`) and 5 baselines (DISMO, PatchTST, Autoformer, LaST, CoST) on the paper's 6 datasets, and compares with Table 3 of the paper.
This folder holds **only our own scripts and small result summaries**. The author code and baseline repos are cloned locally (no license → not committed, see `third_party/README.md`).

Full write-up of the D-Tracker part: [`REPORT.md`](REPORT.md). Results table: [`results/table3.md`](results/table3.md), CSV: [`results/table3.csv`](results/table3.csv).

## Status (2026-11-25)

| Part | Status |
|---|---|
| D-Tracker init=0 (as `bin/run.sh`), 5 GoogleTrends datasets | done; 8/30 cells within ±0.02 or ±5% of paper |
| D-Tracker init=1 (MDL rank search) | done; 14/30 cells pass |
| D-Tracker Covid-19 (seasonal period 52 and 7, init 0 and 1) | done; errors higher than paper |
| DISMO, Autoformer (full budget) | done, 6 datasets |
| PatchTST, CoST (**reduced budget**) | done, 6 datasets |
| LaST (reduced budget) | **not done**: 4 jobs died silently (likely out of memory), Covid NaN crash, programming still running |

## Results (MAE / RMSE, ×10⁻², lower is better)

Bold = best MAE in the row among our runs. `–` = not finished. † = DISMO forecasts diverged; scored after clipping to [0,1] (our post-processing, not DISMO's). Covid D-Tracker = seasonal period 52.

| Dataset | lf | D-Tracker (init=0) | D-Tracker (init=1) | DISMO | PatchTST | Autoformer | LaST | CoST |
|---|---|---|---|---|---|---|---|---|
| Device | 13 | 0.78 / 1.72 | 0.77 / 1.70 | 0.98 / 1.99 | **0.61 / 1.55** | 1.33 / 2.40 | – | 1.80 / 3.28 |
| Device | 26 | 0.85 / 1.88 | 0.83 / 1.83 | 1.01 / 2.05 | **0.64 / 1.59** | 1.38 / 2.50 | – | 1.87 / 3.38 |
| Device | 39 | 0.92 / 2.09 | 0.89 / 2.04 | 1.06 / 2.21 | **0.68 / 1.67** | 1.70 / 2.91 | – | 1.85 / 3.39 |
| Pythonlib | 13 | 0.26 / 1.19 | 0.30 / 1.43 | 2.08 / 12.71† | **0.22 / 0.98** | 0.37 / 1.17 | – | 0.50 / 2.62 |
| Pythonlib | 26 | 0.28 / 1.33 | 0.32 / 1.55 | 2.14 / 12.73† | **0.26 / 1.18** | 0.41 / 1.39 | – | 0.52 / 2.64 |
| Pythonlib | 39 | 0.32 / 1.56 | 0.37 / 1.78 | 0.70 / 3.57† | **0.30 / 1.43** | 0.60 / 1.67 | – | 0.53 / 2.67 |
| VoD | 13 | 0.55 / 1.68 | 0.56 / 1.76 | 1.80 / 9.05† | **0.28 / 0.85** | 0.61 / 1.59 | – | 1.24 / 3.76 |
| VoD | 26 | 0.61 / 1.96 | 0.62 / 2.01 | 2.09 / 9.66† | **0.34 / 1.05** | 0.69 / 1.80 | – | 1.26 / 3.85 |
| VoD | 39 | 0.67 / 2.21 | 0.66 / 2.18 | 2.45 / 10.36† | **0.40 / 1.22** | 0.94 / 2.06 | – | 1.27 / 3.91 |
| Chatapp | 13 | 0.25 / 0.78 | 0.26 / 0.80 | 0.46 / 1.23 | **0.14 / 0.40** | 0.49 / 1.19 | – | 1.16 / 3.90 |
| Chatapp | 26 | 0.30 / 0.96 | 0.31 / 0.99 | 0.49 / 1.30 | **0.19 / 0.54** | 0.55 / 1.38 | – | 1.28 / 4.34 |
| Chatapp | 39 | 0.35 / 1.15 | 0.36 / 1.22 | 0.52 / 1.40 | **0.23 / 0.69** | 0.79 / 1.72 | – | 1.40 / 4.79 |
| Language | 13 | 0.32 / 1.02 | 0.30 / 0.92 | 0.65 / 1.75 | **0.20 / 0.74** | 0.55 / 1.18 | – | 0.63 / 1.87 |
| Language | 26 | 0.35 / 1.27 | 0.33 / 1.17 | 0.70 / 1.87 | **0.24 / 1.02** | 0.59 / 1.25 | – | 0.62 / 1.82 |
| Language | 39 | 0.39 / 1.56 | 0.37 / 1.48 | 0.77 / 2.08 | **0.29 / 1.28** | 0.72 / 1.40 | – | 0.60 / 1.77 |
| Covid-19 | 7 | 0.65 / 1.96 | 0.64 / 1.95 | 0.78 / 2.02 | **0.21 / 1.03** | 0.76 / 2.22 | – | 0.53 / 2.19 |
| Covid-19 | 14 | 0.89 / 2.92 | 0.90 / 2.92 | 0.91 / 2.50 | **0.31 / 1.49** | 0.82 / 2.49 | – | 0.54 / 2.22 |
| Covid-19 | 21 | 1.18 / 4.09 | 1.20 / 4.11 | 1.02 / 2.99 | **0.42 / 1.93** | 1.07 / 2.90 | – | 0.55 / 2.25 |


Paper values for all 8 methods are in [`results/table3.md`](results/table3.md) (second table).

### Read this before using the numbers

1. **PatchTST wins every row here; in the paper it loses to D-Tracker everywhere.** Not yet checked for future-data leakage in our wrapper (`bench/adapters.py`). Treat this column as unverified.
2. **Budget differs from the paper.** PatchTST / LaST / CoST: 5 Optuna trials, max 30 epochs, early-stop patience 5. Autoformer / DISMO: 20 trials, 100 epochs (DISMO: repo grid settings). CPU only, 1 thread.
3. **Reduced model width** to fit CPU: PatchTST `d_model=16` (repo's small-data setting), Autoformer `d_model=64`.
4. DeepAR and FluxCube were **not run** (paper numbers only).
5. D-Tracker gaps vs paper: main suspect is the `init` flag (`run.sh` uses `init=0`, fixed ranks); see REPORT.md "Hypotheses".

## Baseline protocol (`bench/`)

| Item | Choice |
|---|---|
| Data | same tensor and min-max scaling as D-Tracker (`bench/data.py` loads D-Tracker's own `utils.load_tensor`) |
| Input | tensor (T, K, L) flattened to (T, K·L) |
| Forecast origins | GoogleTrends t = 312, 316, …, 632 (as `run.sh`); Covid t = 400, 404, …, 964 (our assumption) |
| Scoring | identical to D-Tracker `accuracy.py` (4-step blocks at each horizon); checked to 1e-9 on D-Tracker outputs (`bench/test_bench.py`) |
| Tuning split | GoogleTrends: train < 2015, val 2015; Covid: val Jan 2021. Optuna TPE, seed 0 |
| Refit | every 52 steps (GoogleTrends) / 28 (Covid) |
| CPU shims | `.cuda()` made a no-op, LaST `topk_mask` CPU version, DISMO tensorly name aliases — all at runtime, repo files untouched |

Repos used (shallow clones, unmodified): DISMO `afa7c28`, PatchTST `204c21e`, Autoformer `51c7d41`, LaST `5f60862`, CoST `7bb5271`.

## Setup (to re-run)

```bash
cd experiments/table3_repro
git clone https://github.com/Higashiguchi-Shingo/D-Tracker            # commit 11c181d
mkdir baselines && cd baselines                                       # only for bench/
git clone https://github.com/<owner>/<repo> ...                        # DISMO, PatchTST, Autoformer, LaST, CoST (commits above)
cd .. && python3 -m venv .venv && .venv/bin/pip install <versions in env.txt>
```

Python 3.13.11; full package list in `env.txt` (`env_before_baselines.txt` = D-Tracker only). Folders `D-Tracker*/`, `baselines/`, `bench_out/`, `logs/` are git-ignored.

## How to run

All jobs: `nice -n 19`, 1 thread (`OMP/OPENBLAS/MKL_NUM_THREADS=1`), no GPU, ≤ 5 at once.

| What | Command | Output |
|---|---|---|
| D-Tracker init=0 | `./run_one.sh device` | `logs/device.txt` |
| D-Tracker init=1 | `./run_variant.sh device` (needs copy `D-Tracker-init1/`) | log |
| Covid | `./run_covid.sh 52 [1]` (needs copy `D-Tracker-covid-sp52[-init1]/`) | log |
| Baseline | `bench/launch.sh patchtst device --trials 5 --max-epochs 30 --patience 5` | `bench_out/<m>/<ds>/` |
| Queue | `EXTRA="..." bench/queue.sh patchtst:device cost:vod ...` | — |
| Paper vs ours | `python parse_results.py --compare` | `logs/compare.md` |
| This table | `python -m bench.table3` | `logs/table3.md`, `logs/table3.csv` |
| Tests | `python -m unittest test_parse_results bench.test_bench` | — |

`main.py` deletes its own result folder, so each variant (init, seasonal period) runs in its own copy of the D-Tracker folder.

## Files

| Path | Content |
|---|---|
| `REPORT.md` | D-Tracker reproduction report: environment, runtimes, per-cell comparison, hypotheses, pandas warning |
| `results/table3.md`, `table3.csv` | table above + paper values. CSV columns `dataset,method,horizon,metric,value` (docs/interfaces.md §4) plus `source` (ours/paper) and `note` (clip01) |
| `results/compare.md` | paper vs init=0 vs init=1, PASS/FAIL per cell |
| `results/baselines/<method>/<dataset>/` | `score.json`, `best_hp.json`, `timing.json` per run |
| `bench/` | baseline harness (our code): data, protocol, adapters, run, table |
| `docs/` | plans and progress ledger written during the work |
