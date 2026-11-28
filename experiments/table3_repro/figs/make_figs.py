"""Figures in the style of the D-Tracker paper (Fig. 1, 3, 5) + a Table-3 summary chart.
Reads D-Tracker's own saved outputs (official code, init=0 = bin/run.sh config).
python figs/make_figs.py  ->  figs/out/*.png, *.pdf
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Polygon  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.dirname(HERE)
sys.path.insert(0, W)
from bench import data  # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# validated categorical palette (dataviz reference, light mode), fixed order
SERIES = ["#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac", "#008a17", "#6a4ce2", "#ec4647"]
INK, INK2, GRID, GRAY = "#191919", "#666666", "#e6e6e6", "#b3b3b3"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRAY, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False})

RUN = {"init0": "D-Tracker/result", "init1": "D-Tracker-init1/result"}


def rdir(ds, root="init0", R=1, S=0, D=0, O=1):
    lc = 56 if ds == "covid" else 104
    base = os.path.join(W, RUN.get(root, root))
    return os.path.join(base, ds, f"lc={lc}", "stl=26", f"rankupdate={R}", f"ablation_s={S}",
                        f"ablation_d={D}", f"outlier={O}", "stl=0")


def names(ds):
    df = pd.read_csv(os.path.join(data.DATA, ds + ".csv.gz"), usecols=["query", "geo"])
    return sorted(set(df["query"])), sorted(set(df["geo"]))


def switches(r):
    return [0] + [int(x) for x in open(os.path.join(r, "log", "model_switch.txt")).read().split()]


def model(r, ts):
    m = os.path.join(r, "model", f"t={ts}-")
    return {k: np.load(os.path.join(m, k + ".npy")) for k in ["Wcore", "Wkey", "Wloc", "A", "D"]}


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


# ------------------------------------------------------------------ world map
_GEO = None


def geo():
    global _GEO
    if _GEO is None:
        g = json.load(open(os.path.join(HERE, "assets", "ne_110m_countries.geojson")))
        _GEO = {}
        for f in g["features"]:
            p = f["properties"]
            code = p["ISO_A2_EH"]
            geom = f["geometry"]
            polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
            _GEO.setdefault(code, {"polys": [], "xy": (p["LABEL_X"], p["LABEL_Y"])})["polys"] += polys
    return _GEO


def draw_map(ax, fill):
    """fill: {iso2: color}; others light gray."""
    for code, c in geo().items():
        if code == "AQ":
            continue
        for poly in c["polys"]:
            ax.add_patch(Polygon(np.asarray(poly[0]), closed=True, fc=fill.get(code, "#f2f2f2"),
                                 ec="white", lw=0.3))
    ax.set_xlim(-170, 180)
    ax.set_ylim(-58, 84)
    ax.set_aspect("equal")
    ax.axis("off")


def group_centroid(codes):
    xy = np.array([geo()[c]["xy"] for c in codes if c in geo()])
    return xy.mean(0)


# ------------------------------------------------------------------ Fig 1b / 5 panel
GROUP_FILL = ["#c9bdf5", "#a6dbae", "#f8c6da", "#f9db99"]   # light violet / green / magenta / yellow


def diffusion_diagram(ax, D, dl, dk):
    """Nodes = location groups on a circle; arrow j->g colored by dynamics i, width ~ d_i,g,j."""
    ang = np.pi / 2 + 2 * np.pi * np.arange(dl) / dl
    pos = np.c_[np.cos(ang), np.sin(ang)] * (0.62 if dl > 2 else 0.55)
    if dl == 2:
        pos = np.array([[-0.6, 0.0], [0.6, 0.0]])
    dmax = D.max() if D.max() > 0 else 1
    shown = 0
    for i in range(dk):
        for g in range(dl):
            for j in range(dl):
                v = D[i, g, j]
                if g == j or v <= 0.05 * dmax:
                    continue
                rad = 0.18 + 0.14 * i
                ax.add_patch(FancyArrowPatch(pos[j], pos[g], connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                             mutation_scale=16, lw=1.2 + 5 * v / dmax, color=SERIES[i],
                                             shrinkA=26, shrinkB=26, zorder=2))
                ax.text(-1.0, -1.0 - 0.17 * shown, f"Dyn #{i + 1}: G{j + 1} → G{g + 1}   d = {v:.2f}",
                        fontsize=8, color=INK, ha="left")
                ax.plot([-1.15, -1.06], [-0.975 - 0.17 * shown] * 2, color=SERIES[i], lw=3)
                shown += 1
    for g in range(dl):
        ax.add_patch(plt.Circle(pos[g], 0.2, fc=GROUP_FILL[g % 4], ec=INK2, lw=0.8, zorder=3))
        ax.text(*pos[g], f"G{g + 1}", ha="center", va="center", fontsize=12, weight="bold", zorder=4)
    if not shown:
        ax.text(0, -1.0, "no diffusion between groups (all d ≈ 0)", ha="center", fontsize=8, color=INK2)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.05 - 0.17 * max(shown, 1), 1.0)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Interest diffusion between groups", loc="left")


def period_panel(ds, ts, title, name, root="init0"):
    r = rdir(ds, root)
    m = model(r, ts)
    m["gen"] = np.load(os.path.join(r, "model", f"t={ts}-", "gen_Wcore.npy"))
    kw, loc = names(ds)
    d = data.dates(ds)
    lc, dk, dl = m["Wcore"].shape
    t = d[ts:ts + lc]
    group = m["Wloc"].argmax(1)                      # each country -> group with the largest W(loc)
    fig = plt.figure(figsize=(13, 8))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.5], hspace=0.32)
    top = gs[0].subgridspec(1, dl, wspace=0.22)
    # top: latent dynamics W(core) generated by the reaction-diffusion system, one panel per location group
    for g in range(dl):
        ax = fig.add_subplot(top[0, g])
        for i in range(dk):
            ax.plot(t, m["Wcore"][:, i, g], color=SERIES[i], lw=0.6, alpha=0.35)
            ax.plot(t, m["gen"][:, i, g], color=SERIES[i], lw=2.2, label=f"Dynamics #{i + 1}")
        ax.set_title(f"Group G{g + 1}: latent dynamics W(core)" if dl <= 2 else f"G{g + 1}: W(core)", loc="left")
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.tick_params(axis="x", labelrotation=30, labelsize=7)
        if g == 0:
            ax.legend(fontsize=7, loc="upper left")
    bot = gs[1].subgridspec(1, 3, width_ratios=[0.9, 2.6, 1.3], wspace=0.08)
    # keyword factor W(key)
    ax = fig.add_subplot(bot[0, 0])
    Wk = m["Wkey"] / (m["Wkey"].max(0, keepdims=True) + 1e-12)
    ax.imshow(Wk, cmap="Blues", vmin=0, vmax=1, aspect="auto")
    ax.set_yticks(range(len(kw)), kw)
    ax.set_xticks(range(dk), [f"#{i + 1}" for i in range(dk)])
    ax.set_xlabel("Dynamics")
    ax.set_title("Keyword factor W(key)", loc="left")
    for (a, b), v in np.ndenumerate(Wk):
        ax.text(b, a, f"{v:.2f}", ha="center", va="center", fontsize=7, color="white" if v > 0.6 else INK)
    # location groups map
    ax = fig.add_subplot(bot[0, 1])
    draw_map(ax, {loc[c]: GROUP_FILL[group[c] % 4] for c in range(len(loc))})
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc=GROUP_FILL[g % 4], ec=INK2, label=f"G{g + 1} ({int((group == g).sum())} countries)")
                       for g in range(dl)], loc="lower left", fontsize=8)
    ax.set_title("Location factor W(loc): each country → its strongest group", loc="left")
    # diffusion diagram
    diffusion_diagram(fig.add_subplot(bot[0, 2]), m["D"], dl, dk)
    fig.suptitle(title + f"   (model window {t[0].date()} – {t[-1].date()}, dk={dk}, dl={dl})",
                 x=0.01, ha="left", fontsize=12, weight="bold")
    fig.text(0.01, 0.005, "Thick lines: dynamics generated by the reaction–diffusion system; thin: fitted factor. "
             "Arrow Gj→Gg: interest in dynamics #i flows from group j to group g (strength d).",
             fontsize=8, color=INK2)
    save(fig, name)
    return {"ts": ts, "start": str(t[0].date()), "end": str(t[-1].date()), "dk": dk, "dl": dl,
            "groups": {f"G{g + 1}": [loc[c] for c in range(len(loc)) if group[c] == g] for g in range(dl)},
            "A": m["A"].round(3).tolist(), "D": m["D"].round(3).tolist()}


def pick(r, date, ds):
    """model whose window starts closest to `date`."""
    d = data.dates(ds)
    idx = int((d < pd.Timestamp(date)).sum())
    return min(switches(r), key=lambda s: abs(s - idx))


# ------------------------------------------------------------------ Fig 1a
def fig1a(ds="device", root="init0"):
    r = rdir(ds, root)
    X = np.load(os.path.join(r, "log", "X.npy"))
    Xh = np.load(os.path.join(r, "log", "X_hat.npy"))
    kw, _ = names(ds)
    d = data.dates(ds)
    n = len(d) - 39                                         # last lf steps are never fitted
    sw = switches(r)
    Xh = Xh.copy()
    Xh[np.all(Xh == 0, axis=(1, 2))] = np.nan            # weeks the code never filled (shown as gaps)
    fig, axs = plt.subplots(2, 4, figsize=(13, 5.2), sharex=True)
    for k, ax in enumerate(axs.ravel()[:len(kw)]):
        ax.plot(d[:n], X[:n, k].mean(1), color=GRAY, lw=1.2, label="original (mean of 48 countries)")
        ax.plot(d[:n], Xh[:n, k].mean(1), color=SERIES[0], lw=1.1, label="D-Tracker fit")
        for s in sw[1:]:
            ax.axvline(d[s], color=INK2, lw=0.6, ls=":")
        ax.set_title(kw[k], loc="left")
        ax.grid(axis="y", color=GRID, lw=0.6)
        ax.tick_params(axis="x", labelrotation=30)
    axs[0, 0].legend(fontsize=7, loc="upper left")
    fig.suptitle(f"Fig. 1(a) style — {ds}: original stream (gray) vs fitted (blue); dotted = model switch "
                 f"({len(sw) - 1} switches)", x=0.01, ha="left", fontsize=12, weight="bold")
    fig.tight_layout()
    save(fig, "fig1a_device_fit")


# ------------------------------------------------------------------ Fig 3
ABL = [("nodiff", "w/o diffusion", dict(D=1)), ("noseason", "w/o seasonal", dict(S=1)),
       ("nooutlier", "w/o outlier", dict(O=0)), ("norank", "w/o RankUpdate", dict(R=0))]
DSN = {"device": "Device", "pythonlib": "Pythonlib", "vod": "VoD", "chatapp": "Chatapp",
       "programming": "Language", "covid": "Covid-19"}


def mae_at(r, h):
    f = os.path.join(r, "log")
    try:
        X, Xh = np.load(f"{f}/Xf{h}.npy"), np.load(f"{f}/Xf_hat{h}.npy")
    except FileNotFoundError:
        return None
    return float(np.mean(np.abs(X - Xh))) * 100


def fig3():
    rows, res = [], {}
    for ds in DSN:
        h = 14 if ds == "covid" else 26
        root = "D-Tracker-covid-sp52/result" if ds == "covid" else "init0"
        full = mae_at(rdir(ds, root), h)
        res[ds] = {"full": full}
        for key, lab, kw in ABL:
            if ds == "covid" and key == "norank":
                pass
            v = mae_at(rdir(ds, root, **{**dict(R=1, S=0, D=0, O=1), **kw}), h)
            res[ds][key] = v
    json.dump(res, open(os.path.join(OUT, "fig3_ablation.json"), "w"), indent=1)
    fig, ax = plt.subplots(figsize=(11, 4.2))
    dss = list(DSN)
    w = 0.2
    for a, (key, lab, _) in enumerate(ABL):
        xs, ys = [], []
        for x, ds in enumerate(dss):
            f, v = res[ds]["full"], res[ds][key]
            if f is None or v is None:
                continue
            xs.append(x + (a - 1.5) * w)
            ys.append(100 * (v - f) / v)          # improvement rate of the full model over the ablation
        CAP = 25
        bars = ax.bar(xs, [min(y, CAP) for y in ys], width=w - 0.02, color=SERIES[a], label=lab)
        for b, y in zip(bars, ys):
            yy = min(y, CAP)
            ax.text(b.get_x() + b.get_width() / 2, yy + (0.4 if y >= 0 else -0.4),
                    f"{y:.1f}" + (" (bar cut)" if y > CAP else ""),
                    ha="center", va="bottom" if y >= 0 else "top", fontsize=7, color=INK)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_ylim(top=28)
    ax.set_xticks(range(len(dss)), [DSN[d] for d in dss])
    ax.set_ylabel("improvement of full model (%)")
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.legend(ncol=4, fontsize=8, loc="upper left")
    ax.set_title("Fig. 3 style — ablation: (MAE_without − MAE_full) / MAE_without, lf = 26 weeks "
                 "(Covid: 14 days). > 0 means the component helps.", loc="left")
    save(fig, "fig3_ablation")
    return res


# ------------------------------------------------------------------ Table 3 chart
def fig_table3():
    sys.path.insert(0, W)
    from parse_results import PAPER
    csv = pd.read_csv(os.path.join(W, "logs", "table3.csv"))
    naive = json.load(open(os.path.join(W, "logs", "naive.json")))
    fig, axs = plt.subplots(2, 3, figsize=(13, 7))
    order = ["Paper: D-Tracker", "D-Tracker (init=0)", "D-Tracker (init=1)", "DISMO", "PatchTST",
             "Autoformer", "CoST", "Naive: last value"]
    for ax, ds in zip(axs.ravel(), DSN):
        h = 14 if ds == "covid" else 26
        sub = csv[(csv.dataset == ds) & (csv.horizon == h) & (csv.metric == "MAE")]
        vals = {"Paper: D-Tracker": PAPER[ds][1][PAPER[ds][0].index(h)],
                "Naive: last value": naive[ds]["last value"][str(h)][0]}
        for _, rw in sub[sub.source == "ours"].iterrows():
            vals[rw["method"]] = rw["value"]
        labs = [o for o in order if o in vals]
        ys = [vals[o] for o in labs]
        col = [SERIES[0] if o.startswith(("D-Tracker", "Paper")) else (SERIES[1] if o.startswith("Naive") else GRAY)
               for o in labs]
        y = np.arange(len(labs))[::-1]
        cap = 2.0 * max(vals["Paper: D-Tracker"], vals["Naive: last value"], 0.5)
        for yi, v, o in zip(y, ys, labs):
            clip = v > cap
            ax.text(min(v, cap) + 0.01 * cap, yi, f"{v:.2f}" + (" ▸ bar cut" if clip else ""),
                    va="center", fontsize=7, color=INK)
        ax.set_xlim(0, cap * 1.25)
        ax.barh(y, [min(v, cap) for v in ys], color=col, height=0.7)
        ax.set_yticks(y, labs, fontsize=8)
        ax.set_title(f"{DSN[ds]} — MAE ×10⁻², lf={h}", loc="left")
        ax.grid(axis="x", color=GRID, lw=0.6)
    fig.suptitle("Table 3 at a glance: blue = D-Tracker (paper / ours), orange = naive 'repeat last value', "
                 "gray = baselines (ours)", x=0.01, ha="left", fontsize=12, weight="bold")
    fig.tight_layout()
    save(fig, "table3_mae")


if __name__ == "__main__":
    what = sys.argv[1:] or ["fig1", "fig5", "fig3", "table3"]
    meta = {}
    if "fig1" in what:
        fig1a()
        r = rdir("device")
        a, b = pick(r, "2010-01-01", "device"), pick(r, "2019-07-01", "device")
        meta["fig1b_a"] = period_panel("device", a, "Fig. 1(b) style — Device, first model (2010–2011)",
                                       "fig1b_device_2010")
        meta["fig1b_b"] = period_panel("device", b, "Fig. 1(b) style — Device, 2019–2021", "fig1b_device_2019")
    if "fig5" in what:
        r = rdir("pythonlib")
        a, b = pick(r, "2013-06-01", "pythonlib"), pick(r, "2020-03-01", "pythonlib")
        meta["fig5a"] = period_panel("pythonlib", a, "Fig. 5(a) style — Pythonlib, Jun 2013 – May 2015",
                                     "fig5a_pythonlib_2013")
        meta["fig5b"] = period_panel("pythonlib", b, "Fig. 5(b) style — Pythonlib, Mar 2020 – Feb 2022",
                                     "fig5b_pythonlib_2020")
    if "fig3" in what:
        meta["fig3"] = fig3()
    if "table3" in what:
        fig_table3()
    old = {}
    mf = os.path.join(OUT, "figures_meta.json")
    if os.path.exists(mf):
        old = json.load(open(mf))
    old.update(meta)
    json.dump(old, open(mf, "w"), indent=1)
