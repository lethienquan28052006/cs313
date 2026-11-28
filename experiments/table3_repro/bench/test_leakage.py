"""Leakage check: a forecast made at origin tau must not change when the data after tau changes.
Also checks that training only touches Y[:t] (fit gets a truncated array).
python -m bench.test_leakage <method>   (one method per process)"""
import sys

import numpy as np

from bench import data, protocol
from bench.test_adapters import HP

if __name__ == "__main__":
    m = sys.argv[1]
    from bench.adapters import METHODS
    X = data.load("pythonlib")
    Y = protocol.to2d(X)
    f = METHODS[m](HP[m], 104, 39, Y.shape[1], dates=data.dates("pythonlib"))
    f.fit(Y[:260].copy(), 208, max_epochs=1)
    tau = 300
    p1 = f.predict(Y, tau)
    Y2 = Y.copy()
    rng = np.random.default_rng(0)
    Y2[tau:] = rng.random(Y2[tau:].shape)          # scramble the future
    p2 = f.predict(Y2, tau)
    Y3 = Y.copy()
    Y3[:tau - 104] = rng.random(Y3[:tau - 104].shape)  # scramble far past (outside lc window)
    p3 = f.predict(Y3, tau)
    d_future = float(np.max(np.abs(p1 - p2)))
    d_past = float(np.max(np.abs(p1 - p3)))
    print(f"{m}: max|pred change| future-scrambled={d_future:.3e}  far-past-scrambled={d_past:.3e}")
    assert d_future < 1e-9, f"LEAK: {m} forecast depends on data after tau"
    print(f"OK {m} no future leakage")
