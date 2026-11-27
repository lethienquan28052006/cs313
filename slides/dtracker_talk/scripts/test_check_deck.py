#!/usr/bin/env python3
"""Tests for the Beamer deck structural checker."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).with_name("check_deck.py")


class CheckDeckTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "figures").mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def outline(self, slides: list[str]) -> str:
        return "\n".join(f"### Slide {name}\nNội dung." for name in slides)

    def deck(self, slides: list[str], body: str = "") -> str:
        frames = "\n".join(
            f"% SLIDE {name}\n\\begin{{frame}}\n{body}\n\\end{{frame}}"
            for name in slides
        )
        return "\\documentclass{beamer}\n\\begin{document}\n" + frames + "\n\\end{document}\n"

    def run_check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(self.root)],
            text=True,
            capture_output=True,
            check=False,
        )

    def assert_fails_with(self, result: subprocess.CompletedProcess[str], text: str) -> None:
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(text, result.stdout + result.stderr)

    def test_missing_outline_fails(self) -> None:
        self.assert_fails_with(self.run_check(), "missing outline")

    def test_outline_deck_mismatch_fails(self) -> None:
        self.write("outline.md", self.outline(["1", "2"]))
        self.write("main.tex", self.deck(["1"]))
        self.assert_fails_with(self.run_check(), "slide mismatch")

    def test_placeholder_fails(self) -> None:
        slides = ["1"]
        self.write("outline.md", self.outline(slides))
        self.write("main.tex", self.deck(slides, "TODO"))
        self.assert_fails_with(self.run_check(), "placeholder")

    def test_missing_figure_fails(self) -> None:
        slides = ["1"]
        self.write("outline.md", self.outline(slides))
        self.write(
            "main.tex",
            self.deck(slides, "\\includegraphics{figures/missing.png}"),
        )
        self.assert_fails_with(self.run_check(), "figure not found")

    def test_unbalanced_frame_fails(self) -> None:
        slides = ["1", "2"]
        self.write("outline.md", self.outline(slides))
        self.write(
            "main.tex",
            "% SLIDE 1\n\\begin{frame}\na\n\\end{frame}\n% SLIDE 2\n\\begin{frame}\nb\n",
        )
        self.assert_fails_with(self.run_check(), "frame mismatch")

    def test_valid_deck_passes(self) -> None:
        slides = ["1", "A1"]
        self.write("outline.md", self.outline(slides))
        self.write("main.tex", self.deck(slides, "Nội dung có toán \\(x=1\\)."))
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_nested_inputs_expand_and_pass(self) -> None:
        slides = ["1", "A1"]
        self.write("outline.md", self.outline(slides))
        self.write("parts/frames.tex", self.deck(slides))
        self.write("parts/body.tex", "\\input{parts/frames}\n")
        self.write(
            "main.tex",
            "\\documentclass{beamer}\n\\begin{document}\n\\input{parts/body}\n\\end{document}\n",
        )
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_input_fails(self) -> None:
        self.write("outline.md", self.outline(["1"]))
        self.write(
            "main.tex",
            "\\documentclass{beamer}\n\\begin{document}\n\\input{parts/missing}\n\\end{document}\n",
        )
        self.assert_fails_with(self.run_check(), "input not found: parts/missing.tex")

    def test_input_cycle_fails(self) -> None:
        self.write("outline.md", self.outline(["1"]))
        body = "% SLIDE 1\n\\begin{frame}\nNội dung.\n\\end{frame}\n"
        self.write("parts/a.tex", body + "\\input{parts/b}\n")
        self.write("parts/b.tex", "\\input{parts/a}\n")
        self.write(
            "main.tex",
            "\\documentclass{beamer}\n\\begin{document}\n\\input{parts/a}\n\\end{document}\n",
        )
        self.assert_fails_with(self.run_check(), "input cycle:")


if __name__ == "__main__":
    unittest.main()
