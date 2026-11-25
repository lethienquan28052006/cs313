"""Smoke: each adapter fits briefly on pythonlib X[:260] and predicts finite (39,k,l).
Run one method per process:  python -m bench.test_adapters <method>"""
import sys
import time

import numpy as np

from bench import data, protocol

HP = {"patchtst": dict(n_heads=4, patch=8, lr=1e-3, dropout=0.1),
      "autoformer": dict(n_heads=4, e_layers=1, d_layers=1, factor=1, lr=1e-3),
      "last": dict(latent=16, dropout=0.1, lr=1e-3),
      "cost": dict(repr=160, alpha=5e-4)}

if __name__ == "__main__":
    m = sys.argv[1]
    from bench.adapters import METHODS
    X = data.load("pythonlib")
    k, l = X.shape[1:]
    Y = protocol.to2d(X)
    t0 = time.time()
    f = METHODS[m](HP[m], 104, 39, Y.shape[1], dates=data.dates("pythonlib"))
    v = f.fit(Y[:260], 208, max_epochs=2)
    p = protocol.to3d(f.predict(Y, 260), k, l)
    assert p.shape == (39, k, l), p.shape
    assert np.isfinite(p).all()
    print(f"OK {m} val_mae={v:.5f} shape={p.shape} secs={time.time() - t0:.1f}")
