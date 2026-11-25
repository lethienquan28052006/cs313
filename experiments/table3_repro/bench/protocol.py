"""Windowing, refit schedule and scoring identical to D-Tracker's accuracy.py."""
import numpy as np

DT = 4  # accuracy.py block length


def to2d(X):
    return X.reshape(X.shape[0], -1)


def to3d(Y, k, l):
    return Y.reshape(Y.shape[0], k, l)


def windows(Y, lc, lf, lo, hi):
    """Samples with target start tau in [max(lo, lc), hi - lf]; input Y[tau-lc:tau], target Y[tau:tau+lf]."""
    taus = range(max(lo, lc), hi - lf + 1)
    xi = np.stack([Y[t - lc:t] for t in taus]) if len(taus) else np.empty((0, lc, Y.shape[1]))
    yi = np.stack([Y[t:t + lf] for t in taus]) if len(taus) else np.empty((0, lf, Y.shape[1]))
    return xi, yi


def refit_points(origins, every):
    return [t for t in origins if (t - origins[0]) % every == 0]


def score(preds, X, hs):
    """preds: {t: (lf_max,k,l)}. Returns {lf: (MAE*100, RMSE*100)} as accuracy.py (concat blocks)."""
    from tensorly.metrics.regression import RMSE
    out = {}
    ts = sorted(preds)
    for l in hs:
        true = np.concatenate([X[t + l - DT:t + l] for t in ts])
        hat = np.concatenate([preds[t][l - DT:l] for t in ts])
        out[l] = (float(np.mean(np.abs(hat - true))) * 100, float(RMSE(true, hat)) * 100)
    return out
