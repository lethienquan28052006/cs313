#!/usr/bin/env python3
"""Boundary tests for check_documents.py using disposable document trees."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).with_name("check_documents.py")


class CheckDocumentsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "sections_vi").mkdir()
        (self.root / "sections_en").mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def main(self, language: str, chapters: list[str]) -> str:
        inputs = "\n".join(f"\\input{{sections_{language}/{name}}}" for name in chapters)
        return f"\\documentclass{{article}}\n{inputs}\n\\begin{{document}}x\\end{{document}}\n"

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

    def test_missing_main_document_fails(self) -> None:
        self.assert_fails_with(self.run_check(), "missing main document")

    def test_missing_input_chapter_fails(self) -> None:
        self.write("dtracker_explained_vi.tex", self.main("vi", ["one"]))
        self.write("dtracker_explained_en.tex", self.main("en", ["one"]))
        self.write("sections_en/one.tex", "\\section{One}\\label{sec:one}\n")
        self.assert_fails_with(self.run_check(), "input not found")

    def test_duplicate_label_fails(self) -> None:
        for language in ("vi", "en"):
            self.write(f"dtracker_explained_{language}.tex", self.main(language, ["one"]))
            self.write(
                f"sections_{language}/one.tex",
                "\\section{One}\\label{sec:one}\\label{sec:one}\n",
            )
        self.assert_fails_with(self.run_check(), "duplicate label")

    def test_placeholder_fails(self) -> None:
        for language in ("vi", "en"):
            self.write(f"dtracker_explained_{language}.tex", self.main(language, ["one"]))
            self.write(f"sections_{language}/one.tex", "\\section{One} TODO\n")
        self.assert_fails_with(self.run_check(), "placeholder")

    def test_different_chapter_lists_fail(self) -> None:
        self.write("dtracker_explained_vi.tex", self.main("vi", ["one"]))
        self.write("dtracker_explained_en.tex", self.main("en", ["one", "two"]))
        self.write("sections_vi/one.tex", "\\section{One}\n")
        self.write("sections_en/one.tex", "\\section{One}\n")
        self.write("sections_en/two.tex", "\\section{Two}\n")
        self.assert_fails_with(self.run_check(), "chapter mismatch")

    def test_label_sets_must_match_between_languages(self) -> None:
        for language, label in (("vi", "sec:one"), ("en", "sec:different")):
            self.write(f"dtracker_explained_{language}.tex", self.main(language, ["one"]))
            self.write(f"sections_{language}/one.tex", f"\\label{{{label}}}\n")
        self.assert_fails_with(self.run_check(), "label mismatch")

    def test_different_selfcheck_counts_fail(self) -> None:
        for language in ("vi", "en"):
            self.write(f"dtracker_explained_{language}.tex", self.main(language, ["one"]))
        self.write(
            "sections_vi/one.tex",
            "\\section{One}\\begin{selfcheck}q\\end{selfcheck}\n",
        )
        self.write("sections_en/one.tex", "\\section{One}\n")
        self.assert_fails_with(self.run_check(), "selfcheck mismatch")

    def test_missing_figure_fails(self) -> None:
        for language in ("vi", "en"):
            self.write(f"dtracker_explained_{language}.tex", self.main(language, ["one"]))
            self.write(
                f"sections_{language}/one.tex",
                "\\begin{figure}\\includegraphics{figures/missing.png}\\end{figure}\n",
            )
        self.assert_fails_with(self.run_check(), "figure not found")

    def test_shared_style_macro_does_not_fail(self) -> None:
        for language in ("vi", "en"):
            self.write(
                f"dtracker_explained_{language}.tex",
                "\\input{dtracker_style.tex}\n" + self.main(language, ["one"]),
            )
            self.write(f"sections_{language}/one.tex", "\\section{One}\n")
        self.write(
            "dtracker_style.tex",
            "\\newcommand{\\sourcefig}[1]{\\includegraphics{figures/#1}}\n",
        )
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_complete_tree_passes(self) -> None:
        for language in ("vi", "en"):
            self.write(f"dtracker_explained_{language}.tex", self.main(language, ["one"]))
            self.write(
                f"sections_{language}/one.tex",
                "\\section{One}\\label{sec:one}\n"
                "\\begin{selfcheck}q\\end{selfcheck}\n",
            )
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
