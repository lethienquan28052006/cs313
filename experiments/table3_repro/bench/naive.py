"""Naive reference forecasts, scored exactly like accuracy.py. python -m bench.naive"""
import json, os
import numpy as np
from bench import data, protocol

def naive(ds):
    X = data.load(ds); hs = data.horizons(ds); lf = max(hs)
    sp = 7 if ds == "covid" else 52
    out = {}
    for name, fn in {
        "last value": lambda t: np.repeat(X[t - 1][None], lf, 0),
        "seasonal naive": lambda t: np.stack([X[t - sp + (h % sp)] for h in range(lf)]),
        "mean of last 4": lambda t: np.repeat(X[t - 4:t].mean(0)[None], lf, 0),
    }.items():
        out[name] = protocol.score({t: fn(t) for t in data.origins(ds)}, X, hs)
    return out

if __name__ == "__main__":
    res = {ds: {k: {str(h): v for h, v in r.items()} for k, r in naive(ds).items()} for ds in data.ALL}
    json.dump(res, open(os.path.join(data.W, "logs", "naive.json"), "w"), indent=1)
    for ds, r in res.items():
        print(ds, {k: " ".join(f"{v[0]:.2f}" for v in s.values()) for k, s in r.items()})
