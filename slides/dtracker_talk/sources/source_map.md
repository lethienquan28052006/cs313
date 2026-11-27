# D-Tracker talk — verified source map

This is the claim ledger for `slides/dtracker_talk/`. Paper-reported material must trace to this map. Illustrative teaching examples and future team reproduction results must be labeled separately and must never be presented as measurements from this paper.

## 0. Canonical source validation

- Title: *D-Tracker: Modeling Interest Diffusion in Social Activity Tensor Data Streams*.
- Authors: Shingo Higashiguchi, Yasuko Matsubara, Koki Kawabata, Taichi Murayama, Yasushi Sakurai.
- Venue: Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.1 (KDD '25), August 3–7, 2025, Toronto, Canada; 12 pages.
- DOI: `10.1145/3690624.3709192` — PDF p. 1, ACM reference block.
- arXiv: `2505.00242v1` [cs.SI], 1 May 2025 — PDF p. 1 header.
- Paper code/dataset link printed in abstract: `https://github.com/Higashiguchi-Shingo/D-Tracker` — PDF p. 1.
- Requested source URL: `https://arxiv.org/pdf/2505.00242`.
- Canonical in-repo file: `slides/paper_explore/sources/paper.pdf` (already tracked; not duplicated).
- Validation date: 2026-11-27. Direct arXiv download and canonical file both contain 5,004,454 bytes, 12 readable pages, 72,157 extracted text characters, and identical metadata title.
- Both SHA-256: `8f3d301da12cbd17ec19cfcd6cb666654ded0fef06f57054826abf887ef9f715`.
- Native executor read all 12 pages, including Appendix A and B. DeepSeek was delegated visual review first but its deployment rejected image input; actual visual review is delegated to Nemotron VL, at most 4 images per prompt. Text claims below come from PDF extraction and printed captions, not native visual interpretation.
- The fuller legacy evidence record is `slides/paper_explore/sources/source_map.md`; this file governs the final-project talk.

## 1. Full coverage checklist

| Paper location | Content reviewed | Deck role |
|---|---|---|
| §1, pp. 1–3 | Motivation, three challenges, Figure 1 preview, three claimed properties | Problem and key findings |
| §2, p. 3 | Tensor analysis, forecasting, social-activity modeling; Table 1 | Optional related-work context |
| §3.1–3.3, pp. 4–5 | Problem 1, reaction–diffusion background, Eq. (1)–(4), parameter sets | Core methodology |
| §4.1, pp. 5–6 | ModelEstimation and ALS updates | Training intuition |
| §4.2–4.3, pp. 6–7 | MDL, model switching, rank update, Algorithm 1 | Automatic/streaming behavior |
| §5, pp. 7–9 | Q1–Q3, datasets, baselines, metrics, ablation, scalability, effectiveness | Experiments and findings |
| §6, p. 9 | Interpretable/automatic/scalable conclusion | Closing |
| Appendix A, pp. 10–11 | Initialization, Algorithms 2–4, complexity proof | Backup/reproduction setup |
| Appendix B, pp. 11–12 | Dataset Table 4, baseline/hyperparameter protocol, hardware, Figures 6–7 | Experiment setup and additional evidence |

## 2. Problem and motivation

| Claim | Exact evidence |
|---|---|
| Social activity data include web searches, purchases, posts and infections; the goal is to discover temporal patterns and forecast future activity. | §1, p. 1, opening paragraphs and abstract. |
| Web-search data can be represented as a third-order tensor stream with attributes keyword, location and time. | §1, p. 1; §3.1, p. 4. |
| Challenge 1 is complex temporal behavior: trends and seasonality vary by keyword/location; interest can diffuse between locations; streams can contain sudden outliers. | §1, pp. 1–2; §3.3, p. 4. |
| Challenge 2 is dynamic change: trends, seasonality and diffusion change over time, so one historical model can become obsolete. | §1, p. 2; §3.3, p. 5. |
| Challenge 3 is high dimensionality and an unbounded time mode, increasing computation and hurting interpretability. | §1, p. 2. |
| Problem 1 input is the recent `L_c`-long tensor window `𝒳^c`; required outputs are time-varying trends, seasonal patterns and interest diffusion plus an `L_f`-step forecast `X_(t_c+L_f)`, continuously. | Problem 1, §3.1, p. 4. |
| The observed stream has `X_t ∈ N^(k×l)`, and observations through `t_c` form `𝒳 ∈ N^(k×l×t_c)`; the recent window is used because retaining everything is constrained by time/memory. | §3.1, p. 4. |
| “Diffusion” is an assumption/inspired model of attention flowing from high-interest to low-interest locations, analogous to chemical concentration; it is not a causal-identification result. | §3.2, p. 4; §1 interpretation relies on model parameters and factors. |

## 3. Big idea and claimed properties

| Claim | Exact evidence |
|---|---|
| D-Tracker incorporates a reaction–diffusion system into tensor decomposition, incrementally updates parameters and switches models as patterns change. | §1, p. 2; §4 overview, p. 5. |
| Interpretable: latent dynamics and non-negative keyword/location factors expose compact trends/diffusion relationships. | §1 contributions, pp. 2–3; §3.3 interpretability paragraph, p. 5; §6(a), p. 9. |
| Automatic: latent dimensions and switching times are chosen with an MDL objective. | §1 contributions, p. 3; §4.2–4.3, pp. 6–7. |
| Scalable: incremental fixed-window processing makes reported computation time independent of total series length. This is not a claim that every operation is constant in every variable. | §1 contributions, p. 3; Figure 4 discussion, §5 Q2, p. 8; Lemma 1 and Appendix A.3, pp. 6, 10. |
| Paper reports “up to 8.0x faster” and “up to 57% improvement” across six real streams. The immediate sentence does not identify the exact baseline/denominator; quote only as paper-reported, not independently recomputed. | §1 contributions, p. 3. |
| Device preview: eight keywords in 50 countries; models switching at dotted vertical lines; latent dynamics are 3 keyword groups × 2 location groups in the illustrated periods. | §1.1, p. 2 and Figure 1 caption text. |

## 4. Model definitions and mechanics

### 4.1 Three residual components — Eq. (1)

- `𝒳^c ≈ 𝒳̂_d + 𝒳̂_s + 𝒳̂_o` — §3.3, Eq. (1), p. 4.
- `𝒳̂_d`: trend tensor containing trend and diffusion patterns; `𝒳̂_s`: seasonal tensor; `𝒳̂_o`: outlier tensor — same location.
- The outlier tensor is assumed sparse because remarkable abnormal behavior is assumed rare — §3.3, p. 5.

### 4.2 Trend/diffusion factorization — Eq. (2)

- `𝒳̂_d = 𝒲^(core) ×_key W^(key) ×_loc W^(loc)` — §3.3, Eq. (2), p. 4.
- Shapes: `𝒲^(core) ∈ R^(d_k×d_l×L_c)`, `W^(key) ∈ R_+^(d_k×k)`, `W^(loc) ∈ R_+^(d_l×l)` — same location and Table 2, p. 3.
- `d_k`, `d_l` are latent keyword/location dimensions; nonnegative projection factors are intended to preserve the direction of latent relationships during reconstruction — §3.3 interpretability, p. 5.
- Paper prints `d_l << k`; dimensions imply `d_l << l`. Treat as a likely typo and surface it only in technical backup if needed — §3.3, p. 4.

### 4.3 Latent reaction–diffusion — Eq. (3)

- `dw_ij/dt = a_ij w_ij + Σ_j' d_ijj'(w_ij' − w_ij)`, for `1≤i≤d_k, 1≤j≤d_l` — §3.3, Eq. (3), p. 4.
- The first term is reaction/local growth; the second is diffusion between latent dynamics — §3.2–3.3, pp. 4–5.
- `a_ij > 0` corresponds to increasing latent dynamics and `a_ij < 0` to decreasing dynamics — §3.3, p. 5.
- `d_ijj' > 0` describes diffusion from `w_ij'` toward `w_ij`; the sign of `(w_ij'−w_ij)` also determines the instantaneous direction of change — §3.3, p. 5.
- `A ∈ R^(d_k×d_l)`, `𝒟 ∈ R^(d_k×d_l×d_l)`, `θ={A,𝒟}`; `f_θ(θ,w_0,L)` generates an `L`-long latent trajectory from initial value `w_0` — Definition 1, p. 5.
- `θ_d={W^(key),W^(loc),θ}` — Definition 2, p. 5.
- Observed keyword/location derivatives are nonnegative weighted multilinear projections of latent reaction–diffusion derivatives — unnumbered derivative equation and interpretability paragraph, §3.3, p. 5.

### 4.4 Seasonal component — Eq. (4)

- `𝒳̂_s = S^(time) ×_key S^(key) ×_loc S^(loc)` — §3.3, Eq. (4), p. 5.
- `S^(time) ∈ R^(d_s×L_c)`, `S^(key) ∈ R^(d_s×k)`, `S^(loc) ∈ R^(d_s×l)`; `d_s` is the number of latent seasonal patterns — same location.
- `θ_s={S^(time),S^(key),S^(loc)}` — Definition 3, p. 5.
- Initialization obtains seasonal factors using STL followed by PARAFAC on the seasonal component — Appendix A.1, p. 10.

### 4.5 Parameter hierarchy and model sequence

- Single model `Θ={θ_d,θ_s,𝒳̂_o}` — Definition 4, pp. 5–6.
- Full stream representation `ℱ={Θ_1,…,Θ_N}` — Definition 5 and §4 overview, p. 5.
- Multiple models represent changing pattern regimes rather than one fixed parameter set for all history — §3.3 and Figure 1 discussion, pp. 2, 5.

## 5. Estimation, automatic selection and streaming

| Item | Exact procedure and anchor |
|---|---|
| Initialization | STL separates trend/seasonal/residual; PARAFAC initializes seasonal factors; nonnegative Tucker decomposition initializes trend keyword/location factors. Appendix A.1, p. 10. |
| Algorithm 1 D-Tracker | Initialize first window and ranks; for each current window estimate candidate `Θ'`; call ModelUpdate; forecast `t_c+L_f`; return full parameter set and predicted stream. Algorithm 1, p. 5. |
| ALS loop | Alternate reaction–diffusion update, trend factor update, seasonal factor update and residual outlier sparsification while other parameters are fixed; repeat until convergence. §4.1, p. 6; Algorithm 2, Appendix A.2, p. 10. |
| Reaction–diffusion update | Nonlinear least squares for system parameters and initial state, with Levenberg–Marquardt used for optimization. Eq. (5) and footnote 1, p. 6. |
| Trend factors | Nonnegative multiplicative Tucker-style updates using mode unfoldings. Eqs. (6)–(7), p. 6. |
| Seasonal factors | Alternating least-squares updates with other components removed from the residual. Eqs. (8)–(9), p. 6. |
| Outliers | Sparsify `𝒳^c−𝒳̂_d−𝒳̂_s`; keep entries only when they reduce MDL total cost, avoiding a manual anomaly threshold. §4.1.3, p. 6. |
| MDL objective | `⟨𝒳;ℱ⟩ = ⟨ℱ⟩ + ⟨𝒳|ℱ⟩`: model description cost plus data encoding cost. Eq. (10), §4.2, p. 6. |
| Cost definitions | Model cost sums nonzero-parameter encoding costs; float cost `c_F=32 bits`; data cost is Gaussian residual negative log-likelihood in bits. §4.2 and footnote 2, p. 6. |
| Model switching | Add candidate model only if doing so lowers total cost versus retaining the current full set. §4.3, p. 7; Algorithm 3, p. 11. |
| RankUpdate | Re-estimate nearby ranks and keep a lower-cost choice; prose says change only one rank by one, assuming gradual structural changes. §4.3, p. 7; Algorithm 4, p. 11. |
| Printed Algorithm 4 issue | Candidate list repeats `(d_k,d_l+1,d_s)` and omits `(d_k+1,d_l,d_s)`; if explaining the intended ±1 neighborhood, flag this printed duplication rather than silently copying it. Algorithm 4, p. 11. |
| Complexity | Lemma 1 states ModelEstimation `O(d_k d_l^2 + k d_k + l d_l)`. Appendix A.3 treats iteration count as a negligibly small constant. The stated lemma does not summarize every seasonal/outlier/ODE/RankUpdate cost. §4.1, p. 6; Appendix A.3, p. 10. |
| Runtime spikes | Figure 4 discussion attributes small wall-clock spikes to RankUpdate, which invokes ModelEstimation multiple times. §5 Q2, p. 8. |

## 6. Experimental research questions and setup

### 6.1 Research questions — §5, p. 7

- Q1 Accuracy: how accurately does D-Tracker forecast future values?
- Q2 Scalability: how does computation time scale?
- Q3 Effectiveness: how well does it extract latent dynamic patterns?

### 6.2 Datasets — §5 p. 7 and Appendix B.1 Table 4 p. 11

- Five weekly GoogleTrends streams cover 2010–2022; Covid-19 has daily infection/death counts from January 2020 to September 2022.
- All data are normalized to minimum 0 and maximum 1 — §5 Datasets, p. 7.
- Table 4 uses `(time, keyword, location)` shapes; model equations use `(keyword, location, time)`. State the convention to avoid apparent shape mismatch.

| ID | Dataset | Exact Table 4 shape | Keywords/signals |
|---|---|---:|---|
| 1 | Device | `(676,8,50)` | Apple Watch, Fitbit, Galaxy, Google Pixel, Macbook, Xperia, iPad, iPhone |
| 2 | Pythonlib | `(676,7,50)` | matplotlib, numpy, pandas, pytorch, scipy, sklearn, tensorflow |
| 3 | VoD | `(676,7,50)` | Apple TV, DAZN, HBO, Prime Video, hulu, netflix, youtube |
| 4 | Chatapp | `(676,8,50)` | facebook, instagram, slack, snapchat, tiktok, twitter, viber, whatsapp |
| 5 | Language | `(676,9,50)` | CSS, HTML, Java, JavaScript, PHP, Ruby, SQL, python, swift |
| 6 | Covid-19 | `(990,2,50)` | new infected, new deceased |

- Prose says GoogleTrends data cover 48 countries, while Table 4 shapes contain 50 locations; do not assert a reconciled country count. Cite the inconsistency if relevant — §5 p. 7 versus Table 4 p. 11.

### 6.3 Forecast protocol — §5 Q1 p. 7

- Baselines: DISMO, FluxCube, PatchTST, Autoformer, DeepAR, LaST, CoST.
- Metrics: MAE and RMSE; Table 3 values are scaled `×10^-2`; lower is better.
- D-Tracker `L_c=104` for GoogleTrends; horizons `L_f∈{13,26,39}` weekly steps, described as 3/6/9 months.
- D-Tracker `L_c=56` for Covid-19; horizons `L_f∈{7,14,21}` daily steps, described as 1/2/3 weeks.
- Ablation removes diffusion, seasonality, outlier handling or RankUpdate; horizon is 26 weeks or 14 days. Degradation formula printed as `(L_full−L_abl)/L_full`; Figure 3 caption calls bar labels “improvement rate.” Use the paper's terms without silently changing the sign convention.

### 6.4 Training, tuning and hardware — Appendix B.1 p. 11

- PatchTST/Autoformer/DeepAR: 100 epochs with early stopping; FluxCube: 2000 with early stopping; LaST: 1000 with early stopping; CoST: 600.
- Periodic retraining: every year for GoogleTrends and every month for Covid-19. Do not call all baselines strictly one-shot offline.
- PatchTST/Autoformer/DeepAR use `L_c∈{52,104,156}` on GoogleTrends and select best results; Covid baselines except FluxCube use `L_c=56`.
- Hyperparameter tuning: GoogleTrends first five years (text says 2010–2014) training and 2015 validation; Covid 2020 training and January 2021 validation; Optuna or grid search.
- D-Tracker initialization grid: `(d_k,d_l)∈[2,4]`, `d_s∈[0,4]`, minimizing Eq. (10). This differs from ongoing RankUpdate.
- Hardware: Intel Xeon Platinum 8268 2.9 GHz CPU, RTX A6000 GPU, 512 GB memory.

## 7. Exact Table 3 D-Tracker values — p. 8

All values below are direct Table 3 entries with scale `×10^-2`; they are paper results, not team reproduction.

| Dataset | `L_f` | MAE | RMSE |
|---|---:|---:|---:|
| Device | 13 | 0.84 | 1.82 |
| Device | 26 | 0.90 | 1.95 |
| Device | 39 | 0.97 | 2.18 |
| Pythonlib | 13 | 0.27 | 1.42 |
| Pythonlib | 26 | 0.32 | 1.54 |
| Pythonlib | 39 | 0.37 | 1.78 |
| VoD | 13 | 0.53 | 1.58 |
| VoD | 26 | 0.59 | 1.83 |
| VoD | 39 | 0.63 | 2.02 |
| Chatapp | 13 | 0.28 | 0.83 |
| Chatapp | 26 | 0.34 | 1.01 |
| Chatapp | 39 | 0.41 | 1.24 |
| Language | 13 | 0.31 | 0.97 |
| Language | 26 | 0.35 | 1.14 |
| Language | 39 | 0.40 | 1.32 |
| Covid-19 | 7 | 0.47 | 1.40 |
| Covid-19 | 14 | 0.70 | 2.42 |
| Covid-19 | 21 | 0.98 | 3.65 |

The sentence above the table states D-Tracker outperforms competitors in MAE on all datasets and greatly reduces RMSE; it also says RMSE is sensitive to large errors and discusses comparable RMSE performance. Preserve both the main outcome and qualification — §5 Q1, p. 7.

### Selected Table 3 comparison used on the main results slide

The main slide uses `L_f=26` for GoogleTrends and `L_f=14` for Covid-19 so that the complete 18-row table is not squeezed onto one slide. “Best baseline” is the smallest of the seven baseline MAE values in the same Table 3 row. “Reduction” is independently arithmetic from those direct entries: `100 × (best_baseline_MAE − D-Tracker_MAE) / best_baseline_MAE`; it is not a quoted paper claim and is not a reproduction result. All MAEs retain the table's `×10^-2` scale.

| Dataset | `L_f` | D-Tracker MAE | Best baseline | Baseline MAE | Recomputed reduction |
|---|---:|---:|---|---:|---:|
| Device | 26 | 0.90 | DISMO | 1.19 | 24.4% |
| Pythonlib | 26 | 0.32 | CoST | 0.45 | 28.9% |
| VoD | 26 | 0.59 | DISMO | 0.66 | 10.6% |
| Chatapp | 26 | 0.34 | DISMO | 0.48 | 29.2% |
| Language | 26 | 0.35 | Autoformer | 0.41 | 14.6% |
| Covid-19 | 14 | 0.70 | Autoformer | 1.18 | 40.7% |

## 8. Ablation, scalability and interpretation findings

| Finding | Exact evidence |
|---|---|
| Seasonal modeling helps high-seasonality Device, Language and Covid-19; diffusion helps especially VoD and Chatapp; outlier handling helps some datasets; RankUpdate supports adaptation. These contributions are dataset-dependent. | Figure 3 discussion, §5 Q1, p. 7. |
| Seasonal/outlier terms may not improve accuracy when such patterns are absent/rare; Language (Dataset 5) did not benefit from diffusion. | Figure 3 discussion continuation, pp. 7–8. |
| Figure 4 left evaluates wall-clock time on Pythonlib; D-Tracker is reported independent of stream length with RankUpdate spikes. Figure 4 right reports fastest average time among compared methods. | §5 Q2, p. 8. |
| Pythonlib: two selected models correspond to Jun 2013–May 2015 and Mar 2020–Feb 2022; `d_k` changes from 2 to 3. | Figure 5 caption/discussion, p. 8. |
| Pythonlib 2013–2015: text interprets Dynamics #1 as pandas-associated diffusion from locations including North America/Australia to Asian countries, mainly China. | §5 Q3, pp. 8–9. |
| Pythonlib 2020–2022: text describes growing interest in numpy/pandas/pytorch in China, decreasing tensorflow-associated dynamics, and diffusion toward China for a group including matplotlib/numpy/pandas. These are model interpretations, not causal or independent behavioral measurements. | §5 Q3, p. 9. |
| Figure 6 reports Device forecast examples: three devices in the US and Galaxy in five countries; text highlights seasonal iPhone forecasts and country-varying Galaxy decline. | Figure 6 caption/text, Appendix B.2 pp. 11–12. |
| Figure 7 reports changing ChatApp/Facebook diffusion patterns between 2010–2012 and 2016–2018. The last paragraph's Group 2/Group 3 wording should be checked against its printed map before quoting a destination; do not silently resolve it. | Appendix B.2, p. 12. |

## 9. Critical-reading boundaries and reproduction scope

- No team reproduction has been run in this task. No result in this map may be relabeled as reproduced, verified by implementation, or observed on team hardware.
- Interpretability is a property of the factorization and equation parameters; the paper does not establish causal interventions.
- The paper's automatic/“parameter-free” language refers to automatic structure selection; Appendix B still documents initialization search ranges, optimizer choices and baseline training hyperparameters.
- Fixed-window scalability does not mean all tensor operations or RankUpdate are O(1).
- Dataset-dependent ablations argue against claiming diffusion/seasonality/outlier components always help every stream.
- Any future team reproduction should explicitly record data version/order, train-validation-test protocol, input window, horizon, normalization, initialization/rank settings, stopping rules, hardware and runtime/MAE/RMSE before filling the reserved slides.
- Teaching examples using three fictional products/countries or small hand-computed numbers are illustrative constructions only; they are not datasets or results from the paper.
