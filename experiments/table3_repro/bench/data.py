"""Same tensors / dates / test origins as D-Tracker (main.py + accuracy.py)."""
import contextlib
import functools
import io
import os
import sys

import numpy as np
import pandas as pd

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(W, "D-Tracker", "src")
DATA = os.path.join(W, "D-Tracker", "data")
GT = ["device", "pythonlib", "vod", "chatapp", "programming"]
ALL = GT + ["covid"]

_RANGE = {"covid": ("2020-01-01", "2022-09-30")}
_DEFAULT = ("2010-01-01", "2022-12-31")           # main.py defaults


def _range(ds):
    return _RANGE.get(ds, _DEFAULT)


@functools.lru_cache(maxsize=None)
def load(ds):
    """(T, k, l) min-max scaled tensor, exactly as main.py builds it."""
    # load D-Tracker/src/utils.py (unmodified) under a private name: CoST has its own `utils`
    import importlib.util
    spec = importlib.util.spec_from_file_location("dtracker_utils", os.path.join(SRC, "utils.py"))
    utils = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(utils)
    s, e = _range(ds)
    kw = (dict(facets=["key", "location_key"], values="value") if ds == "covid"
          else dict(facets=["query", "geo"], values="volume"))
    with contextlib.redirect_stdout(io.StringIO()):
        X = utils.load_tensor(os.path.join(DATA, ds + ".csv.gz"), time_key="date",
                              start_date=s, end_date=e, scale="full", **kw)
    return np.asarray(X, dtype=float)


@functools.lru_cache(maxsize=None)
def dates(ds):
    s, e = _range(ds)
    d = pd.to_datetime(pd.read_csv(os.path.join(DATA, ds + ".csv.gz"), usecols=["date"])["date"])
    d = d[(d >= s) & (d <= e)]
    return pd.DatetimeIndex(sorted(d.unique()))


def horizons(ds):
    return [7, 14, 21] if ds == "covid" else [13, 26, 39]


def origins(ds):
    # GT: run.sh 312..636 step 4; Covid: assumption documented in run_covid.sh
    return list(range(400, 968, 4)) if ds == "covid" else list(range(312, 636, 4))


def refit_every(ds):
    return 28 if ds == "covid" else 52


def split(ds):
    """(train_end, val_end): first index of val period / first index of test period."""
    d = dates(ds)
    a, b = ("2021-01-01", "2021-02-01") if ds == "covid" else ("2015-01-01", "2016-01-01")
    return int((d < a).sum()), int((d < b).sum())


def lc_choices(ds, method):
    if ds == "covid":
        return [56]
    return [52, 104, 156] if method in ("patchtst", "autoformer") else [104]
