# Source map — D-Tracker (arXiv:2505.00242v1)

This file is the ground truth for the two explainer documents. Claims and values in the documents must be traceable to an item below. Do not silently “correct” the paper: explain ambiguities in notes.

## Bibliographic record

- Title: *D-Tracker: Modeling Interest Diffusion in Social Activity Tensor Data Streams*
- Authors: Shingo Higashiguchi; Yasuko Matsubara; Koki Kawabata; Taichi Murayama; Yasushi Sakurai
- Venue: KDD '25, August 3–7, 2025, Toronto, ON, Canada
- DOI: `10.1145/3690624.3709192`
- arXiv: `2505.00242v1` [cs.SI], 1 May 2025
- Code: `https://github.com/Higashiguchi-Shingo/D-Tracker`
- Source snapshot: `sources/paper.html`, `sources/paper.pdf` (12-page arXiv PDF)
- Figure license shown by arXiv HTML: CC BY 4.0. Attribution is retained in `figure_manifest.tsv` and in document captions.

## Section coverage

- §1 “Introduction”: motivation, challenges, contributions, and preview in Figure 1.
- §2 “Related Work”: tensor analysis, time-series forecasting, social-activity modeling, and capability comparison in Table 1.
- §3 “Proposed Model”: Problem 1, reaction–diffusion background, factorization and parameter hierarchy in Table 2.
- §4 “Optimization Algorithms”: ModelEstimation, MDL compression, ModelUpdate, and streaming procedure.
- §5 “Experimental Evaluation”: Q1 accuracy, Q2 scalability, Q3 effectiveness, Tables 3–4 and Figures 3–7.
- §6 “Conclusion”: interpretability, automation, scalability, and experimental summary.
- Appendix A: initialization, detailed ModelEstimation Algorithm 2, complexity proof, ModelUpdate Algorithm 3 and RankUpdate Algorithm 4.
- Appendix B: baseline settings, hyperparameter protocol, dataset Table 4, and additional effectiveness results.

## Main narrative and claims

| Topic | Exact location | Verified content | How the explainer may use it |
|---|---|---|---|
| Problem setting | §1 “Introduction”, paragraphs 1–3 | Social activity data are high-dimensional tensor streams; trends, seasonality, diffusion, and outliers change over time. | Motivation and the three challenges. |
| Method summary | §1, paragraph 4 | Reaction–diffusion equation inside a tensor-decomposition framework; incremental updates and regime switching. | One-paragraph thesis of the paper. |
| Interpretable | §1, final bullet list; §6(a) | Latent dynamics and non-negative factors expose trends and location diffusion. | Explain, but do not equate with causal inference. |
| Automatic | §1, final bullet list; §6(b) | Latent dimensions and switching times are selected by MDL without manual tuning. | Qualify “parameter-free”: structure is learned, numerical optimizers still have settings. |
| Scalable | §1, final bullet list; §6(c) | Computation time is independent of total stream length because only a fixed window is processed incrementally. | Explain fixed-window scope; not O(1) in every variable. |
| Reported maximum speed-up | §1 final bullet | “up to 8.0x faster” than competitors. | Quote only as paper-reported; no independent derivation. |
| Reported maximum accuracy gain | §1 final bullet | “up to 57% improvement.” Metric/base are not stated at that location. | Quote with “reported” and refer to Table 3; do not invent the denominator. |
| Six streams | §5 “Datasets”; Appendix B.1 Table 4 | Five GoogleTrends streams (Device, Pythonlib, VoD, Chatapp, Language) plus Covid-19. | Dataset table. |
| Research questions | §5, Q1–Q3 | Accuracy, scalability, effectiveness. | Structure the experiment chapter. |
| Conclusion | §6 | Interpretable, automatic, scalable summary. | Separate claims from critical discussion. |

## Definitions, notation, and equations

Locations refer to the HTML equation labels and the printed numbers; HTML contains extra unnumbered equations.

| Item | HTML label / printed number | Verified content | Notes for explainer |
|---|---|---|---|
| General reaction–diffusion background | `S3.Ex1` (unnumbered) | ∂u_i/∂t = f(u_i) + Σ_j D(u_j−u_i). | Chemistry analogy; D is diffusion strength. |
| Model decomposition | `S3.EGx1`, Eq. (1) | 𝒳^c ≈ 𝒳̂_d + 𝒳̂_s + 𝒳̂_o. | Trend + seasonal + sparse outlier. |
| Trend factorization | `S3.EGx2`, Eq. (2) | 𝒳̂_d = 𝒲^(core) ×_key W^(key) ×_loc W^(loc). | Explain dimensions `d_k × d_l × L_c`, `d_k × k`, `d_l × l`. |
| Latent reaction–diffusion | `S3.E3`, Eq. (3) | dw_ij/dt = a_ij w_ij + Σ_j' d_ijj'(w_ij'−w_ij). | `a_ij` growth; `d_ijj'` transport to dynamics `ij`. |
| Univariate derivative | `S3.EGx3` (unnumbered) | d𝒳_uv/dt is a weighted sum of latent reaction–diffusion derivatives. | Shows how latent patterns project to keyword/location series. |
| Seasonal factorization | `S3.EGx4`, Eq. (4) | 𝒳̂_s = S^(time) ×_key S^(key) ×_loc S^(loc). | PARAFAC-like seasonal component. |
| Trend estimation | `S4.EGx5`, Eq. (5) | Joint least-squares fit of reaction–diffusion parameters and initial state with other terms fixed. | LM solving step. |
| Multiplicative factors | `S4.EGx6`–`S4.EGx7`, Eq. (6)–(7) | P, Q, W update; X_d^(mode), G^(mode) unfoldings. | Present as “update one factor while holding others fixed”; no need to derive NTD. |
| Seasonal ALS | `S4.EGx8`–`S4.EGx9`, Eq. (8)–(9) | Khatri–Rao/Hadamard products and pseudoinverse update. | Explain ALS, not every linear-algebra identity. |
| MDL total cost | `S4.EGx10`, Eq. (10) | ⟨𝒳;ℱ⟩ = ⟨ℱ⟩ + ⟨𝒳|ℱ⟩. | Model description cost + data encoding cost. |
| Parameter costs | `S4.EGx11`–`S4.EGx13` (unnumbered) | Cost of Θ, θ_d, θ_s, and outlier tensor; `c_F = 32` bits. | Explain nonzero counts and `log*`; avoid pretending this is Shannon-optimal. |
| Data cost | `S4.EGx14` (unnumbered) | Negative log-likelihood under Gaussian residual. | Fits residuals rather than raw values. |
| Streaming forecast problem | `S3.SS1`, Problem 1 | Given `L_c` window, learn time-varying dynamics and forecast `L_f` steps. | Define inputs and outputs explicitly. |

### Symbol dimensions

- `k`, `l`: keyword and location counts; `L_c`: current window; `L_f`: forecast horizon.
- `d_k`, `d_l`, `d_s`: latent keyword, location, seasonal dimensions.
- `𝒲^(core) ∈ R^(d_k×d_l×L_c)`; `W^(key) ∈ R_+^(d_k×k)`; `W^(loc) ∈ R_+^(d_l×l)`.
- `S^(time) ∈ R^(d_s×L_c)`; `S^(key) ∈ R^(d_s×k)`; `S^(loc) ∈ R^(d_s×l)`.
- `A ∈ R^(d_k×d_l)`; `𝒟 ∈ R^(d_k×d_l×d_l)`.
- `θ = {A, 𝒟}`; `θ_d = {W^(key), W^(loc), θ}`; `θ_s = {S^(time), S^(key), S^(loc)}`; `Θ = {θ_d, θ_s, 𝒳̂_o}`; `ℱ = {Θ_1,…,Θ_N}`.
- Observation tensor shape in this paper: `(time, keyword, location)` in Table 4; model equations use `k × l × L_c`. State the convention once to avoid ambiguity.

### Paper ambiguities / likely typos (must be surfaced, not copied as fact)

1. §3.3 says `d_l ≪ k`; the shape of `W^(loc)` and the surrounding text imply `d_l ≪ l`. The explainer uses `d_k ≪ k`, `d_l ≪ l`.
2. Algorithm 4's candidate list in Appendix A.4 repeats `(d_k,d_l+1,d_s)` and omits `(d_k+1,d_l,d_s)`. Explain the intended “change one rank by ±1” search and note the printed duplication.
3. Algorithm 1 initializes from `𝒳_[0:L_c]`, while the stream loop defines windows ending at `t_c`; explain initialization as the first complete window.
4. MDL outlier cost uses `log n` but the streaming model cost is evaluated on a fixed current window; `n` is not separately defined near the cost. Present the formula literally and flag the scope ambiguity.
5. The Text says diffusion parameter `d_ijj' > 0` controls direction, while `𝒟 ∈ R_+` is presented as non-negative; the sign of `(w_ij'−w_ij)` also determines flow. Explain both conditions rather than calling a non-negative coefficient “negative diffusion.”
6. The main text says “Covid-19 dataset ... daily” and Q1 uses horizons 7/14/21 steps as 1/2/3 weeks; clarify that these are daily time steps aggregated to weekly horizons in the evaluation wording.
7. The paper’s “parameter-free” claim refers to automatic model selection, not the absence of numeric optimizer/training settings; Appendix B.1 documents search ranges and framework hyperparameters.
8. HTML figure IDs are malformed (`S5.F4` groups ablation plus scalability images) and printed Figure 4/5 ordering differs from IDs. Refer to visual figure numbers, never HTML IDs.

## Algorithms

| Algorithm | Printed location | Inputs → outputs | Steps to explain |
|---|---|---|---|
| 1 D-Tracker | §4; Appendix A | Tensor stream → full parameter set and forecasts | Initialize first window; for each current window estimate candidate; update/switch model and ranks; forecast. |
| 2 ModelEstimation | Appendix A.2 | `𝒳^c,d_k,d_l,d_s` → `Θ` | STL+PARAFAC+NTD initialization; ALS loop: reaction–diffusion/LM, W factors, S factors, sparsify outlier; iterate to convergence. |
| 3 ModelUpdate | Appendix A.4 | `𝒳^c,ℱ,Θ',ranks` → updated ℱ/ranks | Accept candidate only if total MDL cost decreases; then RankUpdate. |
| 4 RankUpdate | Appendix A.4 | Current ranks/cost → updated ranks | Try one-rank ±1 candidates, re-estimate, keep lower cost. Printed candidate list has the duplication noted above. |

## Complexity

- §4.1 Lemma 1 (HTML labels it Lemma 4.1): ModelEstimation is `O(d_k d_l^2 + k d_k + l d_l)`.
- Appendix A.3 proof retains `#iter` in an intermediate bound and treats it as “a negligibly small constant.”
- The complexity excludes seasonal/outlier updates, window length `L_c`, ODE integration, and the multiple trials in RankUpdate; do not overstate it as the complexity of the entire stream algorithm.
- Scalability claim depends on fixed-length windows and incremental processing. Figure 4 shows wall-clock time versus stream length and average time; Figure 4 is split into `scalability.png` and `avgtime.png`.

## Experimental settings

| Item | Verified setting |
|---|---|
| GoogleTrends streams | Weekly search volumes; various keywords; 48 countries in prose, but Table 4 tensor shapes use 50 locations; 2010–2022. Note this prose/table inconsistency if reporting country counts. |
| Covid-19 | Daily infections/deaths; 50 countries; Jan 2020–Sep 2022. |
| Normalization | Maximum 1, minimum 0. |
| GoogleTrends window/horizons | `L_c=104`; `L_f ∈ {13,26,39}` steps (3/6/9 months). |
| Covid window/horizons | `L_c=56`; `L_f ∈ {7,14,21}` steps (1/2/3 weeks). |
| Baselines | DISMO, FluxCube, PatchTST, Autoformer, DeepAR, LaST, CoST. |
| Metrics | MAE and RMSE; Table 3 values are `×10^-2`. Lower is better. |
| Ablation | Remove diffusion, seasonal, outlier, or RankUpdate; degradation rate `(L_full−L_abl)/L_full`; horizon 26 weeks or 14 days. |
| Hardware | Intel Xeon Platinum 8268 2.9 GHz, RTX A6000 GPU, 512 GB memory. |
| D-Tracker initialization search | `(d_k,d_l) ∈ [2,4]`, `d_s ∈ [0,4]`, minimizing Eq. (10). This is an initialization search, not the ongoing RankUpdate search. |

Table 4 dataset shapes and keywords:

| ID | Name | Keywords | Shape (time, keywords, locations) |
|---|---|---|---|
| 1 | Device | Apple Watch, Fitbit, Galaxy, Google Pixel, Macbook, Xperia, iPad, iPhone | `(676,8,50)` |
| 2 | Pythonlib | matplotlib, numpy, pandas, pytorch, scipy, sklearn, tensorflow | `(676,7,50)` |
| 3 | VoD | Apple TV, DAZN, HBO, Prime Video, hulu, netflix, youtube | `(676,7,50)` |
| 4 | Chatapp | facebook, instagram, slack, snapchat, tiktok, twitter, viber, whatsapp | `(676,8,50)` |
| 5 | Language | CSS, HTML, Java, JavaScript, PHP, Ruby, SQL, python, swift | `(676,9,50)` |
| 6 | Covid-19 | new infected, new deceased | `(990,2,50)` |

## Selected Table 3 values

Use only values copied from Table 3. All are `×10^-2`; best per row is bold in the paper.

| Dataset | L_f | D-Tracker MAE | D-Tracker RMSE |
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

The paper states D-Tracker has the best MAE on all datasets and “greatly reduces RMSE,” but also says some RMSE results are comparable because RMSE is sensitive to large errors. Preserve both statements.

## Figures and tables used

| Printed item | Files | Purpose / caption source |
|---|---|---|
| Figure 1 | `Figure1_a.png`, `Figure1_b.png` | Regime-switching fit; latent dynamics/factors/diffusion. |
| Figure 2 | `overview.png` | Trend + seasonal + outlier overview. |
| Figure 3 | `drop_rate.png` | Ablation improvements. |
| Figure 4 | `scalability.png`, `avgtime.png` | Scalability and average time. |
| Figure 5 | `Wcore_2014.png`, `W_2014.png`, `diff_2014.png`, `Wcore_2020.png`, `W_2020.png`, `diff_2020.png` | Pythonlib modeling over two periods. |
| Figure 6 | `device.png`, `galaxy.png` | Forecast examples. |
| Figure 7 | `Wcore.png`, `Wloc.png`, `Wkey.png`, `diff_facebook.png`, `diff_2016.png` | Chatapp modeling and Facebook diffusion. |
| Table 1 | no bitmap | Capability comparison across methods. |
| Table 2 | no bitmap | Symbols. |
| Table 3 | no bitmap | MAE/RMSE comparison. |
| Table 4 | no bitmap | Dataset descriptions. |

## Critical-reading notes supported by the paper

- Interpretability is structural: latent groups and non-negative projections; the paper does not establish causality from observed diffusion.
- A missing diffusion improvement in the Language dataset is explicitly reported in §5; this is evidence against forcing the diffusion interpretation everywhere.
- Ablation “w/o seasonal” and “w/o outlier” can fail to improve when those patterns are absent or rare, as the paper states.
- The full training/evaluation protocol uses future data for periodic retraining and hyperparameter tuning on validation years; do not describe every baseline as strictly one-shot offline.
- Covid-19 data are observational; forecast accuracy does not imply epidemiological mechanism.
