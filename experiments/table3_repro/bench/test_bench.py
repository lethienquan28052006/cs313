import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bench import data, protocol  # noqa: E402

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(W, "D-Tracker/result/pythonlib/lc=104/stl=26/rankupdate=1/ablation_s=0/"
                      "ablation_d=0/outlier=1/stl=0/forecast")
# accuracy.py output for pythonlib init=0 (logs/pythonlib.txt), x100
LOGGED = {13: (0.2566716443848815, 1.1919368726267116),
          26: (0.28316693652850325, 1.3276848994315738),
          39: (0.3244206604516827, 1.5600599749858883)}


class Bench(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.X = data.load("pythonlib")

    def test_shape(self):
        self.assertEqual(self.X.shape, (678, 7, 48))

    def test_dtracker_alignment_and_score(self):
        preds = {}
        for t in data.origins("pythonlib"):
            xf = np.load(f"{RES}/t={t}/Xf.npy")
            np.testing.assert_array_equal(xf, self.X[t:t + 39])   # forecast step i == time t+i
            preds[t] = np.load(f"{RES}/t={t}/Xf_hat.npy")
        got = protocol.score(preds, self.X, [13, 26, 39])
        for lf, (m, r) in LOGGED.items():
            self.assertAlmostEqual(got[lf][0], m, places=9)
            self.assertAlmostEqual(got[lf][1], r, places=9)

    def test_roundtrip(self):
        k, l = self.X.shape[1:]
        np.testing.assert_array_equal(protocol.to3d(protocol.to2d(self.X), k, l), self.X)

    def test_origins(self):
        self.assertEqual(data.origins("device"), list(range(312, 636, 4)))
        self.assertEqual(data.origins("covid"), list(range(400, 968, 4)))
        self.assertEqual(data.horizons("covid"), [7, 14, 21])

    def test_split(self):
        d = data.dates("device")
        tr, va = data.split("device")
        self.assertEqual((d[tr - 1].year, d[tr].year, d[va - 1].year, d[va].year), (2014, 2015, 2015, 2016))
        c = data.dates("covid")
        tr, va = data.split("covid")
        self.assertEqual((str(c[tr].date()), str(c[va].date())), ("2021-01-01", "2021-02-01"))
        self.assertEqual(len(c), 990)

    def test_windows_no_leak(self):
        Y = np.arange(100, dtype=float)[:, None]
        xi, yi = protocol.windows(Y, lc=10, lf=5, lo=10, hi=60)   # targets start in [10, 60-5]
        self.assertEqual(yi[-1, -1, 0], 59.0)
        self.assertTrue((yi[:, 0, 0] == xi[:, -1, 0] + 1).all())
        self.assertEqual(len(xi), 46)

    def test_refit_points(self):
        o = data.origins("device")
        self.assertEqual(protocol.refit_points(o, 52), [t for t in o if (t - 312) % 52 == 0])
        self.assertEqual(protocol.refit_points(o, 52)[:2], [312, 364])


if __name__ == "__main__":
    unittest.main()
