"""Thin adapters around UNMODIFIED official model code in baselines/<repo>.
One method per process (repos share module names like `models`, `layers`, `utils`).
CPU shims are applied at runtime only (no file edits): see cpu_shims()."""
import os
import sys
import types

import numpy as np
import torch
import torch.nn as nn

from . import protocol

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "baselines")
torch.set_num_threads(1)


def _path(p):
    p = os.path.join(BASE, p)
    if p not in sys.path:
        sys.path.insert(0, p)


def cpu_shims():
    """Repos hard-code .cuda()/'cuda:0'. Make them no-ops on CPU (runtime only)."""
    torch.Tensor.cuda = lambda self, *a, **k: self
    nn.Module.cuda = lambda self, *a, **k: self


# ---------------------------------------------------------------- generic trainer
class Neural:
    """Supervised direct multi-step forecaster: (B, lc, C) -> (B, lf, C)."""
    max_epochs = 100
    patience = 10
    batch = 32
    dtype = torch.float32

    def __init__(self, hp, lc, lf, C, dates=None):
        self.hp, self.lc, self.lf, self.C, self.dates = hp, lc, lf, C, dates
        torch.manual_seed(0)
        self.net = self.build()

    def build(self):
        raise NotImplementedError

    def forward(self, x, taus):
        return self.net(x)

    def loss(self, x, y, taus):
        return nn.functional.mse_loss(self.forward(x, taus), y)

    def fit(self, Y, val_start, max_epochs=None):
        """Y: (T, C) history. Train targets end before val_start; val targets in [val_start, T)."""
        xt, yt = protocol.windows(Y, self.lc, self.lf, 0, val_start)
        xv, yv = protocol.windows(Y, self.lc, self.lf, val_start, len(Y))
        tt = np.arange(max(0, self.lc), val_start - self.lf + 1)
        tv = np.arange(max(val_start, self.lc), len(Y) - self.lf + 1)
        T = lambda a: torch.as_tensor(a, dtype=self.dtype)
        xt, yt, xv, yv = T(xt), T(yt), T(xv), T(yv)
        opt = torch.optim.Adam([p for p in self.net.parameters() if p.requires_grad], lr=self.hp["lr"])
        best, bad, state = np.inf, 0, None
        g = torch.Generator().manual_seed(0)
        for ep in range(max_epochs or self.max_epochs):
            self.net.train()
            for idx in torch.randperm(len(xt), generator=g).split(self.batch):
                self.train_step(opt, xt[idx], yt[idx], tt[idx.numpy()])
            v = self.val_mae(xv, yv, tv)
            if v < best - 1e-7:
                best, bad, state = v, 0, {k: t.clone() for k, t in self.net.state_dict().items()}
            else:
                bad += 1
                if bad >= self.patience:
                    break
        if state is not None:
            self.net.load_state_dict(state)
        self.epochs_run, self.best_val = ep + 1, best
        return best

    def train_step(self, opt, x, y, taus):
        opt.zero_grad()
        l = self.loss(x, y, taus)
        l.backward()
        opt.step()

    @torch.no_grad()
    def val_mae(self, xv, yv, tv):
        self.net.eval()
        if len(xv) == 0:
            return np.inf
        return float(torch.mean(torch.abs(self.forward(xv, tv) - yv)))

    @torch.no_grad()
    def predict(self, Y, tau):
        """Forecast Y[tau:tau+lf] from Y[tau-lc:tau]."""
        self.net.eval()
        x = torch.as_tensor(Y[tau - self.lc:tau][None], dtype=self.dtype)
        return self.forward(x, np.array([tau]))[0].numpy().astype(float)


# ---------------------------------------------------------------- PatchTST
class PatchTST(Neural):
    def build(self):
        _path("PatchTST/PatchTST_supervised")
        from models.PatchTST import Model
        h = self.hp
        cfg = types.SimpleNamespace(
            enc_in=self.C, seq_len=self.lc, pred_len=self.lf,
            e_layers=3, n_heads=h["n_heads"], d_model=16, d_ff=128,   # repo's small-data (ILI) setting
            dropout=h["dropout"], fc_dropout=h["dropout"], head_dropout=0,
            patch_len=h["patch"], stride=h["patch"], padding_patch="end",
            revin=1, affine=0, subtract_last=0, decomposition=0, kernel_size=25, individual=0)
        return Model(cfg)


# ---------------------------------------------------------------- Autoformer
class Autoformer(Neural):
    def build(self):
        _path("Autoformer")
        from models.Autoformer import Model
        from utils.timefeatures import time_features
        h = self.hp
        self.freq = self.hp.get("freq", "w")
        self.marks = torch.as_tensor(time_features(self.dates, freq=self.freq).T, dtype=self.dtype)
        self.label_len = self.lc // 2
        cfg = types.SimpleNamespace(
            seq_len=self.lc, label_len=self.label_len, pred_len=self.lf, output_attention=False,
            moving_avg=25, enc_in=self.C, dec_in=self.C, c_out=self.C, d_model=64, d_ff=128,
            embed="timeF", freq=self.freq, dropout=0.05, factor=h["factor"], n_heads=h["n_heads"],
            e_layers=h["e_layers"], d_layers=h["d_layers"], activation="gelu")
        return Model(cfg)

    def forward(self, x, taus):
        idx_e = np.stack([np.arange(t - self.lc, t) for t in taus])
        idx_d = np.stack([np.arange(t - self.label_len, t + self.lf) for t in taus])
        n = len(self.marks)
        me = self.marks[idx_e]
        md = self.marks[np.minimum(idx_d, n - 1)]   # future calendar marks (known); clip at series end
        dec = torch.cat([x[:, -self.label_len:], torch.zeros(x.shape[0], self.lf, x.shape[2])], dim=1)
        return self.net(x, me, dec, md)


# ---------------------------------------------------------------- LaST
class LaST(Neural):
    max_epochs = 1000
    dtype = torch.float64

    def build(self):
        cpu_shims()
        _path("LaST")
        import models.units as units

        def topk_mask(input, k, dim, return_mask=False):        # repo version hard-codes cuda:0
            topk, indices = torch.topk(input, k, dim=dim)
            fill = 1 if return_mask else topk
            return torch.zeros_like(input).scatter_(dim, indices, fill)
        units.topk_mask = topk_mask
        import models.LaST as M
        M.topk_mask = topk_mask
        net = M.LaST(input_len=self.lc, output_len=self.lf, input_dim=1, out_dim=1, var_num=self.C,
                     latent_dim=self.hp["latent"], dropout=self.hp["dropout"], device="cpu").double()
        return net

    def forward(self, x, taus):
        return self.net(x)[0]

    def train_step(self, opt, x, y, taus):
        # exp_LaST.py: two passes per batch with alternating trainable groups
        L = self.net.LaSTLayer
        crit = [L.MuboNet, L.SNet.VarUnit_s.critic_xz, L.TNet.VarUnit_t.critic_xz]
        for mode in range(2):
            opt.zero_grad()
            for p in self.net.parameters():
                p.requires_grad = (mode == 0)
            for m in crit:
                for p in m.parameters():
                    p.requires_grad = (mode == 1)
            pred, elbo, mlbo, mubo = self.net(x)
            loss = (nn.functional.mse_loss(pred, y) - elbo - mlbo + mubo) if mode == 0 else (mubo - mlbo)
            loss.backward()
            opt.step()
        for p in self.net.parameters():
            p.requires_grad = True


# ---------------------------------------------------------------- CoST
class CoST:
    """Repo protocol (tasks/forecasting.py): self-supervised encoder + ridge on last-step repr.
    max_train_length = lc and sliding_padding = lc-1 (repo: padding = max_train_length-1)."""
    def __init__(self, hp, lc, lf, C, dates=None):
        cpu_shims()
        _path("CoST")
        from cost import CoST as M
        self.hp, self.lc, self.lf, self.C = hp, lc, lf, C
        torch.manual_seed(0)
        self.m = M(input_dims=C, kernels=[1, 2, 4, 8, 16, 32, 64, 128], alpha=hp["alpha"],
                   max_train_length=lc, device="cpu", output_dims=hp["repr"], lr=1e-3, batch_size=8)
        self.epochs = 600

    def _repr(self, Y):
        return self.m.encode(Y[None], mode="forecasting", casual=True, sliding_length=1,
                             sliding_padding=self.lc - 1, batch_size=256)[0]   # (T, repr)

    def fit(self, Y, val_start, max_epochs=None):
        from sklearn.linear_model import Ridge
        self.m.fit(Y[None, :val_start], n_epochs=max_epochs or self.epochs)
        R = self._repr(Y)
        tr = np.arange(self.lc, val_start - self.lf + 1)
        va = np.arange(max(val_start, self.lc), len(Y) - self.lf + 1)
        tgt = lambda ix: np.stack([Y[t:t + self.lf].ravel() for t in ix])
        best = (np.inf, None)
        for a in [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]:   # repo fit_ridge grid
            r = Ridge(alpha=a).fit(R[tr - 1], tgt(tr))
            v = np.mean(np.abs(r.predict(R[va - 1]) - tgt(va))) if len(va) else np.inf
            if v < best[0]:
                best = (v, r)
        self.ridge, self.best_val, self.R, self.Y = best[1], best[0], R, Y
        return best[0]

    def predict(self, Y, tau):
        # casual=True + sliding_length=1: R[tau-1] depends only on Y[:tau] (repo encodes full series too)
        if getattr(self, "_cache_id", None) != id(Y):
            self._cache_R, self._cache_id = self._repr(Y), id(Y)
        return self.ridge.predict(self._cache_R[tau - 1][None])[0].reshape(self.lf, self.C)


METHODS = {"patchtst": PatchTST, "autoformer": Autoformer, "last": LaST, "cost": CoST}
