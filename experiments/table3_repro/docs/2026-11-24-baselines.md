# Table 3 Baselines Reproduction Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Scope (user, 2026-11-24):** only the 5 cloned repos — DISMO, PatchTST, Autoformer, LaST, CoST — plus D-Tracker. DeepAR and FluxCube are out (paper values only). No gluonts.

**Goal:** Produce MAE/RMSE (×10⁻²) for the 7 baselines of D-Tracker Table 3 on the 6 datasets × 3 horizons, using the same data, scaling, test origins and scoring as our D-Tracker runs. Then add them to REPORT.md next to the paper's numbers.

**Architecture:** One shared harness `bench/` (data loading, origins, refit schedule, scoring identical to `accuracy.py`). Each baseline gets a thin adapter around the **unmodified** official model code (cloned into `baselines/`), exposing `fit/predict`. One CLI runs tune → rolling refit → predict → score per (method, dataset). All runs are CPU only, 1 thread, `nice -n 19`, with `setsid` and pid files.

**Tech Stack:** existing `.venv` (Python 3.13, torch 2.15 cpu, numpy 2.5, pandas 3.1, lmfit, tensorly) + approved extra packages (Task 1).

**Spec:** the user's choice "All 7 baselines" (2026-11-24) + earlier constraints; paper arXiv 2505.00242 §5 (baseline settings); parent plan `2026-11-24-dtracker-repro.md`.

## Global Constraints

- WORKDIR `<WORKDIR>`. All code, data copies, results and logs stay inside it.
- No sudo/apt; pip only into `.venv`; no `--user`; no conda; no system files; no GPU (`CUDA_VISIBLE_DEVICES=""`).
- Every job: `setsid -f nohup … > logs/<name>.txt 2>&1 < /dev/null`, then the pid goes to `pids/<name>.pid` via `pgrep`. Every job also runs with `nice -n 19`, `OMP/OPENBLAS/MKL_NUM_THREADS=1` and `torch.set_num_threads(1)`.
- At most **5 concurrent jobs** in total, including any D-Tracker job.
- Never edit cloned repos (`baselines/*`). Adapters go in `bench/`. Record each repo's commit in REPORT.
- Disk: stop and ask if `df -h .` shows < 5 GB free (8.8 GB at plan time). Keep only predictions, not checkpoints.
- **Any single (method) whose pilot estimate exceeds 48 CPU-hours for all 6 datasets → stop and ask** before the full run.
- Match rule for comparing to the paper: PASS if |Δ| ≤ 0.02 or ≤ 5% (same as D-Tracker).

## Paper protocol → our protocol

| Item | Paper (§5) | Ours |
|---|---|---|
| Data / scaling | normalized [0,1] | `utils.load_tensor(..., scale="full")`, exactly as `main.py` (same tensor D-Tracker saw). Covid: 2020-01-01…2022-09-30 |
| Tensor → series | not stated | flatten (T,k,l) → (T, k·l) channels. DISMO consumes the tensor natively |
| Test origins | (D-Tracker: run.sh) | GT t ∈ range(312,636,4); Covid t ∈ range(400,968,4). Score `[l-4:l]` of each forecast, concatenated (= accuracy.py) |
| Horizons | 13/26/39; 7/14/21 | one model forecasts lf_max; sliced per horizon |
| Tuning split | GT train 2010–14 / val 2015; Covid train 2020 / val Jan 2021 | same (indices from `bench.data.split`) |
| Retrain | yearly (GT), monthly (Covid) | refit every 52 / 28 steps on all data < t, hparams fixed after tuning, early stopping on the last val block before t |
| Input length | GT {52,104,156} for PatchTST/Autoformer/DeepAR; others not stated; Covid 56 | same; LaST/CoST use 104 (GT) / 56 (Covid) |
| Search | Optuna or grid, ranges below | Optuna TPE, seed 0, **≤ 20 trials** per (method, dataset), objective = val MAE at lf_max |
| Hardware | Xeon + RTX A6000 | CPU, 1 thread (deviation, reported) |

Search spaces (exact, from paper):
- DISMO: none (repo's own grid search on ranks, `run_dismo_stream.sh` settings).
- FluxCube: hidden {16,32,64}; loss weight {0.1,0.2,0.3}; 2000 epochs, early stop.
- PatchTST: patch len = stride ∈ {2,4,8,16,24}; heads {4,8,16}; lr {1e-3,1e-4}; dropout {0,.1,.2,.3}; 100 ep, ES.
- Autoformer: heads {2,4,8,16}; e_layers {1,2,3}; d_layers {1,2,3}; factor {1,2,3}; lr {1e-3,1e-4}; 100 ep, ES.
- DeepAR: layers {2,3,4}; hidden {32,64,128,256}; lr {1e-3,5e-3,1e-4}; dropout {0,.1,.2,.3}; 100 ep, ES.
- LaST: latent {16,32,64,128}; dropout {.1,.2,.3}; lr 1e-3; 1000 ep, ES.
- CoST: repr dim {160,320,640}; loss weight {5e-4,5e-3,5e-2}; 600 ep.

## Code sources (checked 2026-11-24)

| Method | Source | Commit | Status |
|---|---|---|---|
| DISMO | github.com/kokikwbt/dismo | afa7c28 | cloned; targets Python 3.8 + pandas 1.2. Needs `termcolor`, `tqdm` |
| PatchTST | github.com/yuqinie98/PatchTST (`PatchTST_supervised/models/PatchTST.py`) | 204c21e | cloned; model code needs only torch |
| Autoformer | github.com/thuml/Autoformer (`models/Autoformer.py`) | 51c7d41 | cloned; model code needs only torch |
| LaST | github.com/zhycs/LaST | 5f60862 | cloned; torch only |
| CoST | github.com/salesforce/CoST | 7bb5271 | cloned; needs `einops` |
| DeepAR | GluonTS `DeepAREstimator` (torch) | pip | package, needs `gluonts[torch]` (pulls `lightning`) |
| FluxCube | **no public code found** (GitHub search, authors' pages) | — | **decision needed** (Task 7) |

## Review Focus

1. Leakage: training/validation windows must end strictly before origin t; the scaler is global (same as D-Tracker; noted in REPORT, not "fixed").
2. Horizon slice off-by-one: forecast step i (0-based) = time t+i, and the block for lf=l = steps l-4…l-1, the same as `Xf[l-4:l]`. Test this against D-Tracker's saved `Xf.npy`.
3. Flatten order: (T,k,l) → (T,k·l) → back must round-trip exactly.
4. Old-API breakage in 2021-era repos (numpy 2, pandas 3, torch 2.15): adapters call only the model classes; if a model class itself breaks, record it and ask. No edits to cloned code.
5. Runtime blow-up on 1 CPU thread (k·l ≈ 336–432 channels): pilot timing is mandatory before full runs.

---

### Task 1: Extra packages (venv only)

**Files:** append to `env.txt`.
- [ ] `.venv/bin/pip install optuna einops termcolor tqdm` → rc 0; `pip freeze` diff appended to `env.txt`. Expected: torch stays 2.15.0+cpu (check `pip freeze | grep torch`). If pip tries to replace torch with a CUDA build → abort and ask.
- [ ] Import check: `import optuna, einops, termcolor, tqdm`.

### Task 2: Harness `bench/`

**Files:** `bench/data.py`, `bench/protocol.py`, `bench/test_bench.py`.

**Interfaces (Produces):**
- `load(ds) -> np.ndarray (T,k,l)`: imports `utils` from `D-Tracker/src` and calls `load_tensor` with main.py's exact args (covid dates 2020-01-01…2022-09-30).
- `origins(ds) -> list[int]`, `horizons(ds) -> list[int]`, `lc_choices(ds, method) -> list[int]`, `refit_every(ds) -> int` (52 | 28), `split(ds) -> (train_end, val_end)`.
- `to2d(X) -> (T, k*l)`, `to3d(Y, k, l)`.
- `score(preds: dict[int, np.ndarray (lf_max,k,l)], X, hs) -> dict[int, (mae100, rmse100)]` using `utils.MAE` and `tensorly.metrics.regression.RMSE` on concatenated blocks.
- `class Forecaster(Protocol)`: `fit(X_train (T,k,l), X_val (V,k,l), hp: dict, lc: int, lf: int) -> None`; `predict(X_ctx (lc,k,l)) -> (lf,k,l)`.

- [ ] Tests first (unittest):
  (a) `score` on D-Tracker's saved `Xf.npy/Xf_hat.npy` for pythonlib reproduces `logs/pythonlib.txt` lf=13/26/39 values ×100 (to 1e-9);
  (b) round-trip `to3d(to2d(X)) == X`;
  (c) `origins("device") == list(range(312,636,4))`, `origins("covid") == list(range(400,968,4))`;
  (d) `split("device")` indices point to the first weeks of 2015 / 2016; `split("covid")` to 2021-01-01 / 2021-02-01.
- [ ] `bench/run.py --method M --dataset D [--trials 20] [--pilot]`: tune (Optuna) → rolling refit at origins where `(t - origins[0]) % refit_every == 0` → predict at every origin → `bench_out/M/D/preds.npz` + `score.json` + `best_hp.json` + timing. `--pilot` = 1 trial and 1 refit, prints seconds per fit and an estimated total.

### Task 3–8: Adapters (one task each, same pattern)

Order: PatchTST, Autoformer, LaST, CoST, DISMO (DeepAR dropped).
**Files:** `bench/adapters/<method>.py` implementing `Forecaster`; imports the model class from `baselines/<repo>` via `sys.path` (no copy, no edit).
- [ ] Test: on pythonlib with X[:260], fit 2 epochs → predict shape (39,k,l), all finite.
- [ ] Pilot on device (largest k) → estimate CPU-hours for 6 datasets. > 48 h → stop and ask (options: fewer trials, fixed hp from the paper's mid-range, subset of datasets).
- [ ] Full run: 6 datasets, ≤ 5 concurrent jobs overall, logs `logs/bl_<method>_<ds>.txt`.

DISMO note: the repo is driven by its own `main.py` with `--dataset gtrends --query <name>` and its own data folder. The adapter calls the `dismo` package API on our tensor instead of its CLI. If the package API cannot run on our tensor without code edits → record and ask.

### Task 9: FluxCube — DROPPED by user (report paper value, 'not run')

No public implementation. Options to present: (a) report "n/a (no code)", paper value only; (b) reimplement from the paper (reaction-diffusion + RNN, PINN-style loss): new code, so the result is a reimplementation, not a reproduction. Nothing is done until the user decides.

### Task 10: Report

- [ ] `parse_results.py --baselines`: reads `bench_out/*/*/score.json` → table per dataset × lf: paper vs ours for each baseline, PASS/FAIL, and the "D-Tracker #1 on MAE?" column recomputed with **our** baseline numbers.
- [ ] REPORT.md section "Baselines": commits, packages, protocol table (above), tuning budget, runtime per method, deviations (CPU, ≤ 20 trials, 48 vs 50 locations, Covid origins assumption).
