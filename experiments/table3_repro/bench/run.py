"""Tune -> rolling refit -> predict at every origin -> score (same as accuracy.py).

python -m bench.run --method {patchtst,autoformer,last,cost,dismo} --dataset DS [--trials 20] [--pilot]
Outputs: bench_out/<method>/<ds>/{best_hp.json,preds.npz,score.json,timing.json}
"""
import argparse
import json
import os
import time

import numpy as np

from bench import data, protocol

W = data.W

SPACE = {   # paper Sec.5 search ranges
    "patchtst": dict(patch=[2, 4, 8, 16, 24], n_heads=[4, 8, 16], lr=[1e-3, 1e-4], dropout=[0, .1, .2, .3]),
    "autoformer": dict(n_heads=[2, 4, 8, 16], e_layers=[1, 2, 3], d_layers=[1, 2, 3], factor=[1, 2, 3],
                       lr=[1e-3, 1e-4]),
    "last": dict(latent=[16, 32, 64, 128], dropout=[.1, .2, .3], lr=[1e-3]),
    "cost": dict(repr=[160, 320, 640], alpha=[5e-4, 5e-3, 5e-2]),
}


def outdir(m, ds):
    d = os.path.join(W, "bench_out", m, ds)
    os.makedirs(d, exist_ok=True)
    return d


def make(m, hp, lc, lf, C, ds):
    from bench.adapters import METHODS
    hp = dict(hp, freq="d" if ds == "covid" else "w")
    return METHODS[m](hp, lc, lf, C, dates=data.dates(ds))


def tune(m, ds, Y, lf, trials, pilot, max_epochs=None, patience=None):
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    tr_end, va_end = data.split(ds)
    lcs = data.lc_choices(ds, m)

    def obj(trial):
        hp = {k: trial.suggest_categorical(k, v) for k, v in SPACE[m].items()}
        lc = trial.suggest_categorical("lc", lcs)
        t0 = time.time()
        f = make(m, hp, lc, lf, Y.shape[1], ds)
        if patience:
            f.patience = patience
        v = f.fit(Y[:va_end], tr_end, max_epochs=1 if pilot else max_epochs)
        print(f"trial {trial.number} hp={hp} lc={lc} val_mae={v:.6f} "
              f"epochs={getattr(f, 'epochs_run', '-')} secs={time.time() - t0:.1f}", flush=True)
        return v

    st = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=0))
    st.optimize(obj, n_trials=1 if pilot else trials)
    return st.best_params, st.best_value


def run_neural(m, ds, trials, pilot, max_epochs=None, patience=None):
    X = data.load(ds)
    k, l = X.shape[1:]
    Y = protocol.to2d(X)
    hs = data.horizons(ds)
    lf = max(hs)
    od = outdir(m, ds + ("_pilot" if pilot else ""))
    t0 = time.time()
    best, bv = tune(m, ds, Y, lf, trials, pilot, max_epochs, patience)
    t_tune = time.time() - t0
    lc = best.pop("lc")
    json.dump(dict(best, lc=lc, val_mae=bv), open(f"{od}/best_hp.json", "w"), indent=1)
    print("best", best, "lc", lc, "val", bv, flush=True)

    tr_end, va_end = data.split(ds)
    val_len = va_end - tr_end
    origins = data.origins(ds)
    refits = protocol.refit_points(origins, data.refit_every(ds))
    if pilot:
        refits = refits[:1]
        origins = [o for o in origins if o < refits[0] + data.refit_every(ds)]
    preds, fit_secs, f = {}, [], None
    for t in origins:
        if t in refits:
            s = time.time()
            f = make(m, best, lc, lf, Y.shape[1], ds)
            if patience:
                f.patience = patience
            f.fit(Y[:t], t - val_len, max_epochs=1 if pilot else max_epochs)
            fit_secs.append(time.time() - s)
            print(f"refit t={t} epochs={getattr(f, 'epochs_run', '-')} secs={fit_secs[-1]:.1f}", flush=True)
        preds[t] = protocol.to3d(f.predict(Y, t), k, l)
    sc = protocol.score(preds, X, hs)
    np.savez_compressed(f"{od}/preds.npz", **{str(t): p for t, p in preds.items()})
    json.dump({str(h): v for h, v in sc.items()}, open(f"{od}/score.json", "w"), indent=1)
    json.dump(dict(tune_secs=t_tune, fit_secs=fit_secs, total_secs=time.time() - t0,
                   n_refits=len(protocol.refit_points(data.origins(ds), data.refit_every(ds))),
                   trials=1 if pilot else trials, max_epochs=max_epochs, patience=patience), open(f"{od}/timing.json", "w"), indent=1)
    for h in hs:
        print(f"lf={h}\nMAE: {sc[h][0] / 100}\nRMSE: {sc[h][1] / 100}")


def run_dismo(ds, pilot):
    """Streaming as run_dismo_stream.sh: window wd, slide 4, grid search init, forecast at window end."""
    import sys
    import contextlib
    import io
    sys.path.insert(0, os.path.join(W, "baselines", "dismo"))
    # tensorly>=0.6 renamed these (same signatures); alias at runtime, repo files untouched
    import tensorly as tl
    from tensorly.cp_tensor import unfolding_dot_khatri_rao
    tl.kruskal_to_tensor = tl.cp_to_tensor
    tl.unfolding_dot_khatri_rao = unfolding_dot_khatri_rao
    import dismo
    X = data.load(ds)
    hs = data.horizons(ds)
    lf = max(hs)
    wd = 56 if ds == "covid" else 104
    n_season = 7 if ds == "covid" else 52
    origins = data.origins(ds)
    if pilot:
        origins = origins[:3]
    od = outdir("dismo", ds + ("_pilot" if pilot else ""))
    t0 = time.time()
    model = dismo.DISMO(X.shape[1:], minc=2, maxc=8, mins=2, maxs=8, n_season=n_season, n_trial=5,
                        max_time=1, online_max_iter=5, interaction_type="full", use_self_interaction=False,
                        normalize_ml_projection=False, regime_shift=True, use_carrying_capacity=True,
                        non_negative_seasonality=False, init_complemenatry_matrices=True)
    init = X[:wd]
    with contextlib.nullcontext():  # dismo redirects fd-level stdout itself
        model.grid_search(init, t=0, max_iter=5)
        model.initialize(init, t=0, max_iter=5)
    print("init c,s =", model.c, model.s, "secs", round(time.time() - t0, 1), flush=True)
    preds, upd = {}, []
    for t in range(0, origins[-1] - wd + 1, 4):
        tau = t + wd
        cur = X[t:tau]
        s = time.time()
        with contextlib.nullcontext():  # dismo redirects fd-level stdout itself
            model.update(cur, t=t)
        if tau in origins:
            with contextlib.nullcontext():  # dismo redirects fd-level stdout itself
                pred = model.fit_predict(lf, cur, t, return_full_sequence=True)
            pred = pred[0] if isinstance(pred, (list, tuple)) else pred
            preds[tau] = np.asarray(pred)[-lf:]
        upd.append(time.time() - s)
        if tau % 52 == 0:
            print(f"tau={tau} secs/step={np.mean(upd[-13:]):.2f}", flush=True)
    sc = protocol.score(preds, X, hs)
    np.savez_compressed(f"{od}/preds.npz", **{str(t): p for t, p in preds.items()})
    json.dump({str(h): v for h, v in sc.items()}, open(f"{od}/score.json", "w"), indent=1)
    json.dump(dict(total_secs=time.time() - t0, step_secs=upd), open(f"{od}/timing.json", "w"))
    for h in hs:
        print(f"lf={h}\nMAE: {sc[h][0] / 100}\nRMSE: {sc[h][1] / 100}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--trials", type=int, default=20)
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--max-epochs", type=int, default=None)   # reduced budget (user-approved deviation)
    ap.add_argument("--patience", type=int, default=None)
    a = ap.parse_args()
    print("START", time.strftime("%Y-%m-%dT%H:%M:%S"), vars(a), flush=True)
    if a.method == "dismo":
        run_dismo(a.dataset, a.pilot)
    else:
        run_neural(a.method, a.dataset, a.trials, a.pilot, a.max_epochs, a.patience)
    print("END", time.strftime("%Y-%m-%dT%H:%M:%S"), flush=True)
