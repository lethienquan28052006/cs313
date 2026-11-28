# SDD ledger — plan: <PROJECT>/docs/superpowers/plans/2026-11-24-dtracker-repro.md
Ruling: ledger in WORKDIR/progress.md, no commits — DataMining not a git repo — cost: no git history
Pre-flight: Task4 consumes logs from Task2/3; format = accuracy.py "lf=N / MAE: x / RMSE: y"
Task 1: complete (imports ok, numpy 2.5.5, env.txt)
Task 2/3 Step1b: pids recorded 2026-11-24T13:22:52+07:00
Task 4 parser: complete (unittest 5/5 OK)
Task 2/3: complete (5 logs rc=0, 3 lf blocks each). Task 4: complete (REPORT.md; 8/30 PASS)
Task 6: launched 5 init1 jobs 2026-11-24T14:35:51+07:00, backup result_backup_init0_20261124
Ruling: setsid forks (job-control pgrp leader) so $! was stale; pid files rewritten via pgrep (wrapper + .main.pid). Future: use setsid -f + pgrep
Task 5: launched covid sp52 sp7 2026-11-24T16:08:21+07:00
Task 5+6: complete 2026-11-24T16:38:26+07:00; REPORT updated (init1 14/30, covid sp52 0/6 sp7 1/6)
Covid init1 sp52/sp7 launched 2026-11-24T17:04:51+07:00
Baselines: harness tests 7/7, smoke 4/4; pilots launched 2026-11-24T17:46:11+07:00
Covid init1 done: sp52 rc=0 2554s, sp7 rc=0 1573s
Ruling: DISMO tensorly aliases (kruskal_to_tensor->cp_to_tensor, unfolding_dot_khatri_rao) at runtime; LaST/CoST CPU shims (.cuda no-op, topk_mask cpu) at runtime; no repo file edits — cost: if alias semantics differ, DISMO numbers wrong
Pilots done 2026-11-24T17:59:10+07:00: per-epoch device patchtst 35s, autoformer 1s, last 130s, cost ~12s(x600ep), dismo 6s/step. Launch queue dismo+autoformer x6
Ruling (user-approved): patchtst/last/cost reduced budget --trials 5 --max-epochs 30 --patience 5
DISMO+Autoformer full runs done 20:15 (12/12 rc ok). DISMO diverges: pythonlib 9/81 origins nan/huge, vod 3/81 huge; report raw + clip[0,1] variant (labelled). Reduced-budget queue last/patchtst/cost x6 started 2026-11-24T20:42:39+07:00
2026-11-24T22:25:42+07:00 queue1 (claude bg shell) killed at session end; 5 LaST jobs survived (setsid). Relaunched remaining 13 jobs as detached queue2 (pids/queue2.pid, logs/queue2.txt)
2026-11-25T16:51:09+07:00 table3 built: bench/table3.py -> logs/table3.md. LaST: 4 GT jobs died silently ~00:04-00:29 mid trial 2 (likely OOM, unverified), covid NaN crash; only programming alive. PatchTST best MAE in all 18 rows (unexpected; leakage check pending).
2026-11-28T10:14:22+07:00 Fig3 ablation queue started (24 jobs: 6 ds x nodiff/noseason/nooutlier/norank, init=0 base, forecast/ deleted after scoring). pids/ablation_queue.pid
2026-11-28T10:15:44+07:00 Leakage test (bench/test_leakage.py): patchtst/autoformer/cost forecasts unchanged (diff 0) when future scrambled -> no leak. Naive refs (bench/naive.py, logs/naive.json): last-value beats D-Tracker in most rows (e.g. chatapp lf13 0.14 vs D-Tracker 0.25, paper 0.28). PatchTST ~ naive level -> plausible. Note: tuning val ends idx 313 (2016-01-01) vs first origin 312: 1-week overlap, hp-selection only.
2026-11-28T10:20:41+07:00 figs/make_figs.py: fig1a, fig1b(2010,2019 device), fig5a/b (pythonlib models t=176, t=528 init0), table3_mae chart done -> figs/out. HYPERPARAMETERS.md written. table3 now has naive column. Waiting ablation (bg waiter baj6932vw).
