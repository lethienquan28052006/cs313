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
