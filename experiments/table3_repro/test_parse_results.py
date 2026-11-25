import tempfile
import unittest
from pathlib import Path

from parse_results import parse_log, table, verdict, best_baseline, still_first, compare_table

FULL = """dataset: pythonlib
RMSE: 0.5 MAE: 0.4
lf=13
MAE: 0.0027
RMSE: 0.0142
lf=26
MAE: 0.0032
RMSE: 0.0154
lf=39
MAE: 0.0037
RMSE: 0.0178
END 2026 rc=0 elapsed_s=12
"""


class T(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())

    def w(self, s):
        p = self.d / "x.txt"
        p.write_text(s)
        return p

    def test_full_log(self):
        r = parse_log(self.w(FULL))
        self.assertEqual({k: (round(a, 4), round(b, 4)) for k, (a, b) in r.items()},
                         {13: (0.27, 1.42), 26: (0.32, 1.54), 39: (0.37, 1.78)})

    def test_per_window_line_ignored_and_truncated(self):
        r = parse_log(self.w("RMSE: 0.5 MAE: 0.4\nlf=13\nMAE: 0.01\nRMSE: 0.02\nlf=26\nMAE: 0.03\n"))
        self.assertEqual(set(r), {13})

    def test_missing_file(self):
        self.assertEqual(parse_log(self.d / "none.txt"), {})
        self.assertIn("missing", table({"pythonlib": {}}))

    def test_verdict(self):
        self.assertEqual(verdict(0.285, 0.27), "PASS")   # abs 0.015 <= 0.02
        self.assertEqual(verdict(1.86, 1.82), "PASS")    # abs 0.04, rel 2.2%
        self.assertEqual(verdict(0.33, 0.27), "FAIL")

    def test_table_has_verdict(self):
        md = table({"pythonlib": parse_log(self.w(FULL))})
        self.assertIn("PASS", md)
        self.assertNotIn("FAIL", md)

    def test_best_baseline_vod13_tie(self):
        name, v = best_baseline("vod", 13)
        self.assertEqual(v, 0.56)
        self.assertEqual(set(name.split("/")), {"DISMO", "Autoformer"})

    def test_best_baseline_device13(self):
        self.assertEqual(best_baseline("device", 13), ("DISMO", 1.08))

    def test_still_first(self):
        self.assertEqual(still_first(0.547, "vod", 13), "yes")
        self.assertEqual(still_first(0.56, "vod", 13), "tie")
        self.assertEqual(still_first(0.60, "vod", 13), "no")

    def test_compare_table_columns(self):
        md = compare_table({"pythonlib": {13: (0.25, 1.2)}}, {"pythonlib": {}})
        self.assertIn("init=1", md)
        self.assertIn("missing", md)
        self.assertIn("CoST", md)   # best pythonlib lf13 baseline MAE 0.40


if __name__ == "__main__":
    unittest.main()
