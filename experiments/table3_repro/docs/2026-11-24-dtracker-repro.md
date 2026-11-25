# D-Tracker Table 3 Reproduction Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reproduce the D-Tracker column of Table 3 (KDD 2025): 5 GoogleTrends datasets (+ Covid-19 after approval), write REPORT.md comparing to paper with PASS/FAIL.

**Architecture:** Unmodified upstream repo + isolated venv. One `nice -n 19` background job per dataset via unchanged `bin/run.sh` (new wrapper scripts only); logs parsed by a small new script into a comparison table.

**Tech Stack:** Python 3.13.11 (system `python3`, venv only), numpy 2.5.5 / pandas 3.1.1 / tensorly 0.10.0 / lmfit 1.3.4 / statsmodels 0.15.0 / torch 2.15.0+cpu (full list: `WORKDIR/env.txt`).

**Spec:** user task messages of 2026-11-24 (pasted task steps 1–6 + safety constraints; plan amendment points 1–7). Paper: arXiv 2505.00242.

**Status as of 2026-11-24 13:21 (+07):** see "Status" lines under each task. Evidence = `ls`, `ps -u $USER`, log greps.

## Global Constraints

- WORKDIR = `<WORKDIR>` (replaces `~/dtracker_repro`: user restricted work to the DataMining folder). Repo at `WORKDIR/D-Tracker` (commit 11c181d).
- No sudo/apt/yum; no pip outside `.venv`; no `--user`; no conda base edits; no ~/.bashrc, /etc, crontab, systemd, NVIDIA/CUDA changes.
- Never kill processes not started by us; never delete files outside WORKDIR.
- Every job: `nice -n 19` with `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`; ≤ 5 parallel jobs; CPU only.
- **Background launch (JupyterHub):** every job started as `setsid nohup <cmd> > <log> 2>&1 & echo $! > WORKDIR/pids/<name>.pid`, so it survives closing the Jupyter terminal.
- Preflight: `df -h ~` ≥ 5GB free, `free -h`. Measured 2026-11-24: 19G free disk, 50G avail RAM, 32 cores → OK.
- Do not edit upstream code or `run.sh`. Variants = new scripts. Covid and init=1 runs need user approval first.
- Logs: `WORKDIR/logs/<name>.txt`. Paper values = code values × 100.
- **Match rule:** PASS if `|repro − paper| ≤ 0.02` (×10⁻² units) OR `|repro − paper| / paper ≤ 5%`; else FAIL. Applied per cell (dataset × horizon × metric).
- Never write "matches" without numbers.
- Tests use stdlib `unittest` (`.venv/bin/python -m unittest`); no pytest install.
- No git repo in DataMining → no commit steps; progress ledger = `WORKDIR/progress.md`.

## Review Focus

1. `main.py` does `shutil.rmtree` on its result dir at start → relaunching a dataset (or init=1 in the same tree) wipes init=0 results. Expected: never relaunch a running/finished dataset; back up `result/` before any variant.
2. Job dies mid-run (OOM/exception/terminal close) → log has Traceback or no `END` line while PID gone; parser must report "missing", not crash or print 0.
3. accuracy.py prints `lf=N`, `MAE:`, `RMSE:` per horizon; per-window lines look like `RMSE: x MAE: y` on one line — parser must only read the accuracy.py blocks and ×100.
4. PASS/FAIL edge: paper value 0.27 with repro 0.285 → abs diff 0.015 ≤ 0.02 → PASS even though 5.6% off; test both branches.
5. Non-determinism (lmfit/odeint, BLAS threads=1): runs once; report as hypothesis only.

---

### Task 1: Environment

**Status:** DONE (evidence: `.venv/bin/python` exists, all imports OK, `env.txt` written 13:14).

- [x] Step 1: `cd WORKDIR && python3 -m venv .venv`
- [x] Step 2: `.venv/bin/pip install -r D-Tracker/requirement.txt lmfit psutil` then `.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu` (both rc=0, log `logs/pip.txt`)
- [x] Step 3: Verify imports `numpy,pandas,tensorly,lmfit,statsmodels,torch,sklearn,seaborn,psutil,scipy` → ok. numpy 2.5.5 installed; no numpy-2 error seen so far, so `numpy<2` not tried (also no 3.13 wheel exists).
- [x] Step 4: `env.txt` = python version + `pip freeze`.

### Task 2: Smoke run pythonlib

**Status:** RUNNING (PID main.py 1190641, wrapper 1190636; at 13:21: 62 windows in log, 72 `t=*` dirs, no Traceback, no `lf=` block yet).

Wrapper `WORKDIR/run_one.sh <dataset>` (exists): sets venv PATH, thread env vars, `MPLBACKEND=Agg`, runs `nice -n 19 sh run.sh <dataset>`, prints `START`, `END ... rc= elapsed_s=`.

- [x] Step 1: Launched 13:14 in background — **with `nohup ... &` only, not `setsid`, no pid file** (launched before the setsid rule). Process is already re-parented to PID 1 and ignores SIGHUP, so it should survive; do NOT relaunch (rmtree would wipe progress).
- [ ] Step 1b: Record existing PIDs: `mkdir -p pids && pgrep -u $USER -f "main.py --dataset pythonlib" > pids/pythonlib.pid` (same for the 4 others).
- [ ] Step 2: Pass = `logs/pythonlib.txt` has 3 `lf=` blocks (13/26/39) with MAE/RMSE and `END ... rc=0`. Fail → superpowers:systematic-debugging, no code edits; ask if a fix needs a code change.

### Task 3: Remaining 4 datasets (device, vod, chatapp, programming)

**Status:** RUNNING — all 4 were launched at 13:15, ~60 s after pythonlib started. **Deviation:** they were started before the gate below was confirmed (old gate "ts= 4" was never checked). At 13:21: device 20 `t=*` dirs, vod 29, programming 52, chatapp 8 (chatapp's log shows no "current window" yet but has `t=*` dirs — output buffered). No Traceback in any log.

Gate for starting this task (for any future relaunch): pythonlib finished with 3 MAE/RMSE blocks, **or** `D-Tracker/result/pythonlib/lc=104/stl=26/rankupdate=1/ablation_s=0/ablation_d=0/outlier=1/stl=0/forecast/` contains ≥ 1 `t=*` dir. (Current state: second condition met, 72 dirs.)

- [x] Step 1: Launched (nohup, not setsid — see Task 2 Step 1). 5 jobs total = limit.
- [ ] Step 1b: pid files (Task 2 Step 1b).
- [ ] Step 2: Pass = each log has 3 `lf=` blocks + `END rc=0`; wall time from `elapsed_s`.

Future launches use: `setsid nohup ./run_one.sh <ds> > logs/<ds>.txt 2>&1 & echo $! > pids/<ds>.pid`.

### Task 4: Parse + report

**Status:** NOT DONE. `test_parse_results.py` drafted (pytest style, not run) → convert to unittest. `parse_results.py` not written.

**Files:** `WORKDIR/parse_results.py`, `WORKDIR/test_parse_results.py`, `WORKDIR/REPORT.md`.

**Interfaces:**
- `parse_log(path) -> dict[int, tuple[float, float]]` — lf → (MAE×100, RMSE×100); missing file / truncated → only complete lf blocks; `{}` if none.
- `verdict(repro: float, paper: float) -> str` — `"PASS"` if `abs(repro-paper) <= 0.02 or abs(repro-paper)/paper <= 0.05` else `"FAIL"`.
- `table(results: dict[str, dict[int, tuple]]) -> str` — markdown: dataset | lf | metric | paper | repro | Δ | Δ% | PASS/FAIL; "missing" when absent.
- CLI: `.venv/bin/python parse_results.py` prints table for all logs in `logs/`.

- [ ] Step 1: Tests (unittest): full log → {13:(0.27,1.42),26:(0.32,1.54),39:(0.37,1.78)}; per-window line `RMSE: 0.5 MAE: 0.4` ignored; truncated log → only lf=13; missing file → `{}` and table shows `missing`; `verdict(0.285,0.27)=="PASS"` (abs branch); `verdict(1.86,1.82)=="PASS"` (abs 0.04 >0.02, rel 2.2% → rel branch); `verdict(0.33,0.27)=="FAIL"`.
- [ ] Step 2: Run `.venv/bin/python -m unittest test_parse_results -v` → FAIL (no module), then implement, → PASS.
- [ ] Step 3: Paper values hard-coded exactly:
  Device MAE 0.84/0.90/0.97 RMSE 1.82/1.95/2.18; Pythonlib 0.27/0.32/0.37, 1.42/1.54/1.78; VoD 0.53/0.59/0.63, 1.58/1.83/2.02; Chatapp 0.28/0.34/0.41, 0.83/1.01/1.24; Programming (Language) 0.31/0.35/0.40, 0.97/1.14/1.32; Covid 7/14/21: MAE 0.47/0.70/0.98, RMSE 1.40/2.42/3.65.
- [ ] Step 4: REPORT.md: Python + packages (env.txt), exact commands, runtime per dataset, table with PASS/FAIL, deviations (nohup-not-setsid launch, early Task 3 start, 48 vs paper's 50 locations), hypotheses for FAILs (init=0 vs paper's grid-search init, package version drift, lmfit/odeint randomness).

### Task 5: Covid-19 row — ASK USER BEFORE RUNNING

**Status:** NOT STARTED.

**Files:** Create `WORKDIR/run_covid.sh` (do not touch `run.sh`). Same env/nice as `run_one.sh`; launch with setsid + `pids/covid.pid`; log `logs/covid.txt`.

Parameters (names verified in `main.py` / `accuracy.py`):
- `main.py --dataset covid --lc 56 --lf 21 --start_date 2020-01-01 --end_date 2022-09-30 --init 0 --rankupdate 1 --ablation_seasonal 0 --ablation_diffusion 0 --outlier 1 --stl 0`
  (main.py loads covid with facets `key, location_key`, value `value`.) Measured: date filter gives n = 990 days (2020-01-01 … 2022-09-16), equals paper's 990.
- `accuracy.py --dataset covid --lc 56 --lf 7/14/21 --start_timestep 400 --end_timestep 968 --rankupdate 1 --outlier 1 --stl 0`

How start/end were chosen (**assumption — repo and paper text give no Covid values**):
- `DTracker.run(dt=4)` saves forecasts at t = lc+4, lc+8, … < n−lf → t ∈ {60, 64, …, 968}. `accuracy.py` needs `t=<start>`…`<end` dirs to exist on that grid, step 4 (hard-coded `dt=4`).
- Paper: train 2020, validation Jan 2021 → test from Feb 2021. 2021-02-01 = index 397 → first grid point ≥ 397 is **400**.
- GoogleTrends analog: run.sh uses end 636 = last saved t, excluded (range end exclusive). Mirror: **end_timestep 968** (last t=968 excluded, last scored t=964).
- `seasonal_period=52`, `stl_period=26` defaults are weekly-oriented; paper value for daily Covid unknown. Plan runs defaults; a 7/7 variant is an open question for the user, not run.
- Paper: MAE 0.47/0.70/0.98, RMSE 1.40/2.42/3.65 (×10⁻²).

- [ ] Step 1: Ask user approval.
- [ ] Step 2: Write script, launch, pass = 3 `lf=` blocks (7/14/21) + `END rc=0`.
- [ ] Step 3: Add to parse table (Task 4 already has covid paper values).

### Task 6: init=1 variant — ASK USER BEFORE RUNNING

**Status:** NOT STARTED. Only for datasets with ≥ 1 FAIL cell in Task 4.

**Files:** Create `WORKDIR/run_variant.sh <dataset>` — same as run.sh flags but `--init 1`.

Isolation (main.py rmtree's `result/<ds>/lc=104/.../stl=0` and that path does **not** contain `init`, so init=1 in the same tree overwrites init=0):
- [ ] Step 1: Ask user approval with the FAIL list.
- [ ] Step 2: Backup: `cp -a D-Tracker/result WORKDIR/result_backup_init0_<date>`.
- [ ] Step 3: Run in a separate copy `cp -a D-Tracker WORKDIR/D-Tracker-init1` (code unchanged; results land in `D-Tracker-init1/result/`). Log `logs/<ds>_init1.txt`, pid `pids/<ds>_init1.pid`, setsid launch, ≤ 5 jobs total.
- [ ] Step 4: Parser reads `*_init1.txt` → extra rows tagged init=1.

### Out of scope (now): baselines

Not part of the current plan. **Requires external repos + GPU — waiting for user approval.** Nothing will be installed for them.
1. DISMO (Kawabata et al., 2023)
2. FluxCube (Murayama et al., 2022)
3. PatchTST (Nie et al., 2022)
4. Autoformer (Wu et al., 2021)
5. DeepAR (Salinas et al., 2020)
6. LaST (Wang et al., 2022)
7. CoST (Woo et al., 2022)
