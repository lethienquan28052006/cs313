# D-Tracker hyperparameters and parameters — what each one is and why it exists

Sources: the paper (KDD '25, Table 2 notation, Sec. 3–5) and the official code (`src/main.py`, `src/dtracker.py`, `src/rank.py`, `src/MDL.py`, commit `11c181d`). Where the code and paper differ, both are given. Line numbers refer to the official code.

## 0. The model in one picture

At every time step D-Tracker looks at the **current window** — the last `lc` weeks of a tensor *keywords × countries × weeks* — and explains it as the sum of three parts:

```
X_current  ≈   trend           +   seasonal          +   outliers
          (reaction–diffusion)    (repeating pattern)   (rare spikes)
```

- **Trend** = a few hidden curves ("latent dynamics") that **grow or shrink** on their own (*reaction*) and **spread from one country group to another** (*diffusion*), mapped onto real keywords and countries by two weight matrices.
- **Seasonal** = a pattern that repeats every `seasonal_period` steps (e.g. the iPhone launch every autumn).
- **Outliers** = a sparse set of one-off spikes that would otherwise distort the trend.

The data then **streams** in 4 weeks at a time. Each time, D-Tracker fits a fresh model on the newest window and asks: *is it cheaper (in bits, MDL) to keep the old model or switch to the new one?* That's how it detects regime changes ("model switches", the dotted lines in Fig. 1a).

The paper says D-Tracker has **no hyperparameters to tune**: the sizes (`dk, dl, ds`), the outliers, and when to switch are all chosen automatically by MDL. What is left are a few **run settings** (window lengths, seasonal period) and **switches** for the ablation study. Those are listed below.

---

## 1. Run settings (command-line flags of `main.py`)

"Default" = value in `main.py` if the flag is omitted. "Used" = what `bin/run.sh` (the authors' script) and we used.

| Flag | Default | Used | What it is | Why it exists / what it changes |
|---|---|---|---|---|
| `--dataset` | device | each dataset | Which `data/<name>.csv.gz` to load | Covid uses columns `key, location_key, value`; others `query, geo, volume` |
| `--lc` | 104 | 104 (Covid 56) | **L_c**, length of the current window (weeks; days for Covid) | How much recent history one model sees. 104 weeks = 2 years, so every model sees each season twice. Longer = smoother but slower to react |
| `--lf` | 39 | 39 (Covid 21) | **L_f**, how far ahead to forecast | The longest forecast horizon. The paper scores 13 / 26 / 39 weeks (Covid 7 / 14 / 21 days) |
| `--start_date`, `--end_date` | 2010-01-01, 2022-12-31 | same (Covid 2020-01-01 → 2022-09-30) | Time range cut from the CSV | Defines the stream length (678 weeks for GoogleTrends) |
| `--init` | 0 | **0** in `run.sh` | How to pick the starting sizes `(dk, dl, ds)` | `0` = fixed (3, 2, 1) (`dtracker.py:491`). `1` = grid search by MDL cost (Sec. 4 of the paper). **The paper describes init=1; `run.sh` uses init=0** — our main suspect for the gaps to Table 3 |
| `--maxdk`, `--maxdl` | 4, 4 | 4, 4 | Upper limits on `dk`, `dl` | Bounds for grid search and RankUpdate. Lower limits are fixed at 2 (`rank.py`) |
| `--maxds` | 2 | 2 | Upper limit on `ds` | Paper says ds ∈ [0, 4]; code default is 2 |
| `--seasonal_period` | 52 | 52 | **n_p**, period of the seasonal pattern | Forecasts repeat the seasonal part every n_p steps (`gen_seasonal`). 52 = yearly for weekly data. **Covid is daily, yet the default is still 52**; we also tried 7 (weekly cycle) |
| `--rankupdate` | 0 | **1** | Turn RankUpdate on/off | After each model switch, try `dk±1, dl±1, ds±1` and keep the cheapest (MDL). Lets the model grow/shrink as new topics appear. Ablated in Fig. 3 ("w/o RankUpdate") |
| `--outlier` | 0 | **1** | Turn the outlier tensor on/off | When on, spikes are moved into a sparse X̂_o so they don't bend the trend. Ablated in Fig. 3 |
| `--ablation_seasonal` | 0 | 0 | Drop the seasonal part **from forecasts** | Ablation only. Note: the seasonal part is still *estimated*; it's just not added to the forecast (`gen_forecast`) |
| `--ablation_diffusion` | 0 | 0 | Freeze all diffusion strengths at 0 | Ablation only: groups evolve independently, no interest spreads between countries |
| `--stl` | 1 | **0** | Initialise trend/seasonal split with STL decomposition | `run.sh` turns it off: the first split is "Tucker trend, rest = seasonal" instead |
| `--stl_period` | 26 | 26 (unused when stl=0) | STL period | Only used if `--stl 1`. Still appears in the result folder name |

### Evaluation flags (`accuracy.py`)

| Flag | Used | Meaning |
|---|---|---|
| `--lf` | `13/26/39` (Covid `7/14/21`) | Horizons to score |
| `--start_timestep`, `--end_timestep` | 312, 636 (Covid 400, 968: our assumption) | Range of forecast origins scored (312 = start of 2016) |
| `dt` (hard-coded 4) | 4 | At horizon h, the score uses the 4-step block ending at h, i.e. steps h−3…h of each forecast, concatenated over all origins |

MAE and RMSE are on the min-max scaled tensor (all values in [0, 1]); Table 3 reports them ×10⁻².

---

## 2. Learned parameters (fitted automatically; nothing to set)

Notation from Table 2 of the paper; array names as saved in `result/.../model/t=<start>-/`.

| Symbol (file) | Shape | Meaning | Where you see it |
|---|---|---|---|
| **dk** | integer | number of **keyword dynamics** = number of hidden "interest patterns" | Fig. 1b/5: lines per panel |
| **dl** | integer | number of **location groups** (sets of countries that behave alike) | Fig. 1b/5: G1, G2, … |
| **ds** | integer | number of seasonal patterns (0 = no seasonality) | — |
| 𝒲(core) (`Wcore.npy`, `gen_Wcore.npy`) | lc × dk × dl | the hidden curves: dynamics *i* inside group *g* over time. `gen_Wcore` is what the reaction–diffusion equation generates (smooth); `Wcore` is the raw fitted factor | Fig. 1b/5, top row (thick vs thin lines) |
| **A** = {a_ig} (`A.npy`) | dk × dl | **growth rate** of dynamics *i* in group *g*. a > 0 → interest grows by itself, a < 0 → fades. Bounded to [−2, 2] | slope of the thick curves |
| **𝒟** = {d_igj} (`D.npy`) | dk × dl × dl | **diffusion strength**: how fast dynamics *i* spreads **from group j to group g**. Only acts when group j is ahead of g (term d·max(w_j − w_g, 0)). Bounded to [0, 1]; d_igg = 0 | Fig. 1b/5, arrows Gj → Gg |
| **w₀** (`X.npy`) | dk × dl | starting value of each hidden curve at the window start. Bounded to [10⁻⁴, 0.15] | left end of the thick curves |
| **W(key)** (`Wkey.npy`) | k × dk | how strongly each **keyword** belongs to each dynamic (non-negative) | Fig. 1b/5, heatmap |
| **W(loc)** (`Wloc.npy`) | l × dl | how strongly each **country** belongs to each group (non-negative). In the figures each country is coloured by its largest entry | Fig. 1b/5, map |
| **S(time), S(key), S(loc)** (`Stime/Skey/Sloc.npy`) | lc×ds, k×ds, l×ds | seasonal pattern (CP decomposition): its shape over one window, and how much each keyword/country follows it | not plotted |
| **X̂_o** | lc × k × l, sparse | outlier spikes. Chosen greedily: add the biggest residual as an outlier while that saves more bits than it costs | the spikes in Fig. 1a |

The reaction–diffusion equation for dynamics *i* in group *g* (from `dtracker.py:185`, time rescaled to [0, 1] over the window):

```
dw_ig/dt  =  a_ig · w_ig   +   Σ_j  d_igj · max(w_ij − w_ig, 0)
             (reaction)        (diffusion from groups that are ahead)
```

The trend tensor is then `trend[t, keyword, country] = Σ_i Σ_g  W(key)[keyword, i] · w_ig(t) · W(loc)[country, g]`.

---

## 3. Fixed constants inside the code (not flags)

| Constant | Value | Where | Role |
|---|---|---|---|
| step size `dt` | 4 | `DTracker.run` | the stream advances 4 weeks (days for Covid) at a time; one switch decision per step |
| initial ranks (init=0) | dk=3, dl=2, ds=1 | `dtracker.py:491` | starting sizes when not grid-searched |
| min ranks | dk≥2, dl≥2, ds≥0 | `rank.py` | lower limits for RankUpdate |
| grid search ranges (init=1) | dk, dl ∈ {2…4}, ds ∈ {0…maxds} | `grid_search` | 27 candidate models scored by MDL |
| ALS stop tolerance ε | 10⁻⁴ | `DTrackerModel.epsilon` | stop the alternating updates when error improves by < ε; also floor in multiplicative updates |
| parameter bounds | a∈[−2,2], d∈[0,1], w₀∈[10⁻⁴,0.15] | `slice_init_params` | keep the ODE stable |
| float cost c_F | 32 bits | `MDL.py` | bits to store one real number in the MDL model cost |
| zero tolerance | 10⁻³ | `MDL.py` | parameters below this are "zero" and cost nothing → MDL rewards sparse models |
| encoding cost | −log₂ Gaussian likelihood of residuals | `MDL.costE` | bits to describe the data given the model; trades off against the model cost |

**MDL in one line:** total cost = bits for the model (count of non-zero parameters × (log of sizes + 32)) + bits for the errors. Bigger models fit better (fewer error bits) but cost more to describe. The cheapest total wins. The same rule picks the ranks, the outliers, and whether to switch models.

---

## 4. Baseline hyperparameters (our Table 3 runs)

Search spaces follow Sec. 5 of the paper. Tuning: Optuna TPE (seed 0), trained before 2015, validated on 2015 (Covid: Jan 2021), early stopping on validation MAE, Adam, batch 32. **Reduced budget** (user-approved): PatchTST / LaST / CoST 5 trials, ≤ 30 epochs, patience 5. Autoformer: 20 trials, ≤ 100 epochs, patience 10.

| Method | Tuned (search space) | Fixed by us | What the tuned knobs do |
|---|---|---|---|
| PatchTST | patch ∈ {2,4,8,16,24}, heads ∈ {4,8,16}, lr ∈ {1e-3,1e-4}, dropout ∈ {0,.1,.2,.3}, lc ∈ {52,104,156} | d_model 16, d_ff 128, 3 layers, stride = patch, RevIN on | patch = how many weeks form one input "token"; heads = parallel attention views; RevIN normalises each series by its own recent level (this is why it behaves close to "repeat the last value") |
| Autoformer | heads ∈ {2,4,8,16}, enc layers ∈ {1,2,3}, dec layers ∈ {1,2,3}, factor ∈ {1,2,3}, lr, lc ∈ {52,104,156} | d_model 64, d_ff 128, moving avg 25, calendar features | factor = how many top autocorrelation lags are used; layers = depth |
| LaST | latent ∈ {16,32,64,128}, dropout ∈ {.1,.2,.3}, lr 1e-3, lc 104 | float64 | latent = size of the seasonal/trend latent space. **latent 128 needs ~24 GB RAM per job** |
| CoST | repr ∈ {160,320,640}, alpha ∈ {5e-4,5e-3,5e-2}, lc 104 | 600 epochs (≤30 in reduced budget), ridge α grid from the repo | repr = size of the learned representation; alpha = weight of the seasonal contrastive loss |
| DISMO | repo grid: c, s ∈ [2, 8], n_season 52 (Covid 7), window 104 (Covid 56) | repo defaults from `run_dismo_stream.sh` | c, s = number of latent components (picked by its own grid search) |

Chosen values per dataset (from `results/baselines/<method>/<ds>/best_hp.json`):

| Dataset | PatchTST (patch, heads, dropout, lc) | Autoformer (heads, enc, dec, factor, lc) | CoST (repr, alpha) |
|---|---|---|---|
| Device | 16, 8, 0, 52 | 4, 1, 3, 3, 104 | 640, 0.005 |
| Pythonlib | 16, 8, 0, 52 | 4, 3, 1, 2, 52 | 640, 0.005 |
| VoD | 16, 8, 0, 52 | 4, 1, 1, 3, 52 | 640, 0.005 |
| Chatapp | 16, 8, 0, 52 | 4, 1, 1, 2, 52 | 320, 0.05 |
| Language | 4, 4, 0.1, 104 | 16, 3, 2, 3, 104 | 640, 0.005 |
| Covid-19 | 4, 16, 0.3, 56 | 4, 2, 1, 2, 56 | 640, 0.005 |

lr = 1e-3 was chosen everywhere.

---

## 5. Things we noticed in the code (useful when explaining results)

1. **`run.sh` uses `init=0`** (fixed ranks 3/2/1), while the paper describes MDL grid search (init=1). With init=1 our match to Table 3 improves from 8/30 to 14/30 cells.
2. **Seasonal period for Covid** stays 52 by default although Covid is daily (a 7-day cycle is more natural). seasonal_period=7 gave slightly lower errors, still above the paper.
3. **RankUpdate scores candidate sizes without the outlier term** (`rank.py: costT` builds models with the default `outlier=False`), so its cost is not quite the same as the model it replaces.
4. **The seasonal ablation keeps estimating the seasonal part**; it only leaves it out of the forecast.
5. **Grid search starts from best cost 0** (`grid_search`), so a candidate is only accepted if its MDL cost is negative. This works because the Gaussian encoding cost becomes negative when errors are tiny, but it would silently return ranks (0, 0, 0) on noisier data.
