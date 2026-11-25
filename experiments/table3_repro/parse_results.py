"""Parse accuracy.py output in logs/<name>.txt; compare to Table 3 (x1e-2)."""
import re
import sys
from pathlib import Path

LOGS = Path(__file__).resolve().parent / "logs"

# dataset -> horizons, MAE list, RMSE list (paper Table 3, x1e-2)
PAPER = {
    "device":      ([13, 26, 39], [0.84, 0.90, 0.97], [1.82, 1.95, 2.18]),
    "pythonlib":   ([13, 26, 39], [0.27, 0.32, 0.37], [1.42, 1.54, 1.78]),
    "vod":         ([13, 26, 39], [0.53, 0.59, 0.63], [1.58, 1.83, 2.02]),
    "chatapp":     ([13, 26, 39], [0.28, 0.34, 0.41], [0.83, 1.01, 1.24]),
    "programming": ([13, 26, 39], [0.31, 0.35, 0.40], [0.97, 1.14, 1.32]),
    "covid":       ([7, 14, 21],  [0.47, 0.70, 0.98], [1.40, 2.42, 3.65]),
}

# Table 3 baseline MAE (x1e-2), per dataset, rows = horizons in PAPER order.
# Source: arXiv 2505.00242 html v1 (extracted by summarizer; D-Tracker column cross-checked).
BASE_NAMES = ["DISMO", "FluxCube", "PatchTST", "Autoformer", "DeepAR", "LaST", "CoST"]
BASE_MAE = {
    "device":      [[1.08, 3.86, 1.39, 1.21, 2.14, 1.91, 1.63],
                    [1.19, 3.85, 1.54, 1.31, 2.21, 2.07, 1.80],
                    [1.22, 3.97, 1.21, 1.34, 2.37, 2.37, 1.74]],
    "pythonlib":   [[0.47, 0.86, 0.89, 0.49, 2.01, 0.71, 0.40],
                    [0.52, 0.93, 0.95, 0.47, 2.01, 0.86, 0.45],
                    [0.57, 1.09, 0.83, 0.42, 2.01, 0.92, 0.47]],
    "vod":         [[0.56, 2.83, 0.95, 0.56, 1.77, 2.91, 2.98],
                    [0.66, 2.83, 0.84, 0.74, 1.88, 2.53, 2.36],
                    [0.78, 2.79, 1.69, 1.13, 1.98, 1.55, 3.27]],
    "chatapp":     [[0.47, 1.47, 0.47, 0.84, 1.85, 2.66, 1.76],
                    [0.48, 1.48, 0.74, 0.81, 2.16, 2.34, 2.09],
                    [0.50, 1.47, 0.88, 0.54, 1.93, 2.18, 2.18]],
    "programming": [[0.94, 1.38, 0.41, 0.37, 1.98, 0.74, 0.40],
                    [1.12, 1.42, 0.50, 0.41, 2.03, 0.80, 0.47],
                    [1.36, 1.51, 0.51, 0.54, 2.01, 0.81, 0.49]],
    "covid":       [[1.12, 1.95, 1.60, 1.10, 4.60, 2.39, 1.23],
                    [1.33, 1.97, 2.04, 1.18, 2.30, 2.10, 1.45],
                    [1.58, 1.98, 2.24, 1.25, 2.61, 1.74, 1.72]],
}


def best_baseline(ds, lf):
    """(name or 'A/B' on tie, MAE) of the best Table-3 baseline."""
    row = BASE_MAE[ds][PAPER[ds][0].index(lf)]
    m = min(row)
    return "/".join(n for n, v in zip(BASE_NAMES, row) if v == m), m


def still_first(mae, ds, lf):
    """Compare at the paper's 2-decimal precision: 'yes' / 'tie' / 'no'."""
    a, b = round(mae, 2), best_baseline(ds, lf)[1]
    return "yes" if a < b else ("tie" if a == b else "no")


def compare_table(r0, r1):
    """init=0 vs init=1 vs paper, per cell, + MAE rank vs best paper baseline."""
    rows = ["| dataset | lf | metric | paper | init=0 | v | init=1 | v | best baseline (MAE) | #1 MAE? paper / init=0 / init=1 |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for ds in r0:
        hs, maes, rmses = PAPER[ds]
        for i, lf in enumerate(hs):
            bn, bv = best_baseline(ds, lf)
            for j, (metric, pv) in enumerate((("MAE", maes[i]), ("RMSE", rmses[i]))):
                cells = []
                for res in (r0.get(ds, {}), r1.get(ds, {})):
                    if lf in res:
                        cells += [f"{res[lf][j]:.3f}", verdict(res[lf][j], pv)]
                    else:
                        cells += ["missing", ""]
                rank = ""
                if metric == "MAE":
                    rank = " / ".join([still_first(pv, ds, lf)] + [
                        still_first(res[lf][0], ds, lf) if lf in res else "missing"
                        for res in (r0.get(ds, {}), r1.get(ds, {}))])
                base = f"{bn} {bv:.2f}" if metric == "MAE" else ""
                rows.append(f"| {ds} | {lf} | {metric} | {pv:.2f} | " + " | ".join(cells) + f" | {base} | {rank} |")
    return "\n".join(rows)


_BLOCK = re.compile(r"^lf=(\d+)\s*\nMAE:\s*(\S+)\s*\nRMSE:\s*(\S+)\s*$", re.M)


def parse_log(path):
    """lf -> (MAE*100, RMSE*100); only complete accuracy.py blocks."""
    p = Path(path)
    if not p.exists():
        return {}
    return {int(lf): (float(m) * 100, float(r) * 100)
            for lf, m, r in _BLOCK.findall(p.read_text(errors="replace"))}


def verdict(repro, paper):
    d = abs(repro - paper)
    return "PASS" if d <= 0.02 + 1e-12 or d / paper <= 0.05 + 1e-12 else "FAIL"


def base(name):
    return name.split("_")[0]


def table(results):
    rows = ["| run | lf | metric | paper | repro | Δ | Δ% | verdict |",
            "|---|---|---|---|---|---|---|---|"]
    for name, res in results.items():
        hs, maes, rmses = PAPER[base(name)]
        for i, lf in enumerate(hs):
            for j, (metric, pv) in enumerate((("MAE", maes[i]), ("RMSE", rmses[i]))):
                if lf not in res:
                    rows.append(f"| {name} | {lf} | {metric} | {pv:.2f} | missing | | | missing |")
                    continue
                rv = res[lf][j]
                rows.append(f"| {name} | {lf} | {metric} | {pv:.2f} | {rv:.3f} | {rv - pv:+.3f} "
                            f"| {100 * (rv - pv) / pv:+.1f}% | {verdict(rv, pv)} |")
    return "\n".join(rows)


def main(names=None):
    names = names or sorted(p.stem for p in LOGS.glob("*.txt") if base(p.stem) in PAPER)
    print(table({n: parse_log(LOGS / f"{n}.txt") for n in names}))


def main_compare():
    gt = ["device", "pythonlib", "vod", "chatapp", "programming"]
    r0 = {d: parse_log(LOGS / f"{d}.txt") for d in gt}
    r1 = {d: parse_log(LOGS / f"{d}_init1.txt") for d in gt}
    print(compare_table(r0, r1))
    print("\nCovid-19 (init=0; columns = seasonal_period 52 | seasonal_period 7)\n")
    print(compare_table({"covid": parse_log(LOGS / "covid_sp52.txt")},
                        {"covid": parse_log(LOGS / "covid_sp7.txt")})
          .replace("paper / init=0 / init=1", "paper / sp=52 / sp=7")
          .replace("init=0 |", "sp=52 |").replace("init=1 |", "sp=7 |"))


if __name__ == "__main__":
    if sys.argv[1:] == ["--compare"]:
        main_compare()
    else:
        main(sys.argv[1:] or None)
