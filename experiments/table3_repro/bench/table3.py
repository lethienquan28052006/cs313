"""Build a Table-3-style table from our runs -> logs/table3.md.
python -m bench.table3"""
import json
import math
import os
import sys

import numpy as np

from bench import data, protocol

W = data.W
sys.path.insert(0, W)
from parse_results import PAPER, BASE_NAMES, BASE_MAE, parse_log  # noqa: E402

DS = ["device", "pythonlib", "vod", "chatapp", "programming", "covid"]
NAME = {"device": "Device", "pythonlib": "Pythonlib", "vod": "VoD", "chatapp": "Chatapp",
        "programming": "Language", "covid": "Covid-19"}
BL = ["dismo", "patchtst", "autoformer", "last", "cost"]
BLN = {"dismo": "DISMO", "patchtst": "PatchTST", "autoformer": "Autoformer", "last": "LaST", "cost": "CoST"}


def dtracker(ds, init1):
    if ds == "covid":
        name = "covid_sp52_init1" if init1 else "covid_sp52"
    else:
        name = f"{ds}_init1" if init1 else ds
    return parse_log(os.path.join(W, "logs", name + ".txt"))


def baseline(m, ds):
    """{lf: (mae, rmse, flag)}; flag '†' = forecasts clipped to [0,1] because raw diverged."""
    f = os.path.join(W, "bench_out", m, ds, "score.json")
    if not os.path.exists(f):
        return None
    sc = {int(k): tuple(v) for k, v in json.load(open(f)).items()}
    bad = any(not math.isfinite(v[0]) or v[0] > 10 for v in sc.values())
    if not bad:
        return {k: (a, b, "") for k, (a, b) in sc.items()}
    p = np.load(os.path.join(W, "bench_out", m, ds, "preds.npz"))
    preds = {int(t): np.clip(np.nan_to_num(p[t], nan=0.0, posinf=1.0, neginf=0.0), 0, 1) for t in p.files}
    cl = protocol.score(preds, data.load(ds), data.horizons(ds))
    return {k: (a, b, "†") for k, (a, b) in cl.items()}


def main():
    cols = ["D-Tracker (init=0)", "D-Tracker (init=1)"] + [BLN[m] for m in BL]
    out = ["# Table 3 reproduction (MAE / RMSE, ×10⁻², lower is better)", "",
           "Bold = best MAE in the row among our runs. `–` = not finished / failed. "
           "† = raw forecasts diverged; scored after clipping to [0,1] (our post-processing).", "",
           "| Dataset | lf | " + " | ".join(cols) + " |",
           "|---|---|" + "---|" * len(cols)]
    for ds in DS:
        runs = [dtracker(ds, False), dtracker(ds, True)]
        runs = [{k: (a, b, "") for k, (a, b) in r.items()} for r in runs]
        runs += [baseline(m, ds) for m in BL]
        for lf in data.horizons(ds):
            vals = [r.get(lf) if r else None for r in runs]
            maes = [round(v[0], 2) for v in vals if v]
            best = min(maes) if maes else None
            cells = []
            for v in vals:
                if not v:
                    cells.append("–")
                    continue
                s = f"{v[0]:.2f} / {v[1]:.2f}{v[2]}"
                cells.append(f"**{s}**" if round(v[0], 2) == best else s)
            out.append(f"| {NAME[ds]} | {lf} | " + " | ".join(cells) + " |")

    out += ["", "## Paper Table 3 MAE (×10⁻², for reference)", "",
            "| Dataset | lf | D-Tracker | " + " | ".join(BASE_NAMES) + " |",
            "|---|---|---|" + "---|" * len(BASE_NAMES)]
    for ds in DS:
        hs, maes, _ = PAPER[ds]
        for i, lf in enumerate(hs):
            row = BASE_MAE[ds][i]
            out.append(f"| {NAME[ds]} | {lf} | {maes[i]:.2f} | " + " | ".join(f"{v:.2f}" for v in row) + " |")
    txt = "\n".join(out) + "\n"
    open(os.path.join(W, "logs", "table3.md"), "w").write(txt)
    print(txt)
    write_csv(os.path.join(W, "logs", "table3.csv"))


def write_csv(path):
    """cs313 docs/interfaces.md sec.4 format: dataset,method,horizon,metric,value (x1e-2).
    source = ours | paper; note = clip01 when DISMO forecasts were clipped."""
    rows = ["dataset,method,horizon,metric,value,source,note"]
    for ds in DS:
        runs = {"D-Tracker (init=0)": dtracker(ds, False), "D-Tracker (init=1)": dtracker(ds, True)}
        runs = {k: {h: (a, b, "") for h, (a, b) in r.items()} for k, r in runs.items()}
        runs.update({BLN[m]: baseline(m, ds) for m in BL})
        for meth, r in runs.items():
            for h, v in sorted((r or {}).items()):
                note = "clip01" if v[2] else ""
                rows += [f"{ds},{meth},{h},MAE,{v[0]:.6f},ours,{note}", f"{ds},{meth},{h},RMSE,{v[1]:.6f},ours,{note}"]
        hs, maes, rmses = PAPER[ds]
        for i, h in enumerate(hs):
            rows += [f"{ds},D-Tracker,{h},MAE,{maes[i]},paper,", f"{ds},D-Tracker,{h},RMSE,{rmses[i]},paper,"]
            rows += [f"{ds},{n},{h},MAE,{v},paper," for n, v in zip(BASE_NAMES, BASE_MAE[ds][i])]
    open(path, "w").write("\n".join(rows) + "\n")


if __name__ == "__main__":
    main()
