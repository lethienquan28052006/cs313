#!/usr/bin/env python3
"""Tests for the D-Tracker report skeleton checker."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

CHECKER = Path(__file__).with_name("check_report.py")
SECTIONS = {
    "01_introduction": "Introduction",
    "02_problem_setup": "Problem Setup",
    "03_method": "Method",
    "04_experiments": "Experiments",
    "05_conclusion": "Conclusion",
    "06_tasks": "Task Assignment",
}
MAIN = """\\documentclass[conference]{IEEEtran}
\\begin{document}
\\onecolumn
\\tableofcontents
\\clearpage
\\twocolumn
\\begin{abstract}Pending abstract.\\end{abstract}
\\input{sections/01_introduction}
\\input{sections/02_problem_setup}
\\input{sections/03_method}
\\input{sections/04_experiments}
\\input{sections/05_conclusion}
\\input{sections/06_tasks}
\\bibliography{references}
\\end{document}
"""


class CheckReportTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.write_valid_sources()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def write_valid_sources(self) -> None:
        self.write("main.tex", MAIN)
        self.write("references.bib", "@article{x, title={X}}")
        for name, title in SECTIONS.items():
            body = f"\\section{{{title}}}\nPending text.\n"
            if name == "04_experiments":
                body += "\\subsection{Results from the Original Paper}\nPending paper results.\n"
                body += "\\subsection{Our Reproduction}\nPending team results.\n"
            self.write(f"sections/{name}.tex", body)

    def write_pdf(self, pages: int) -> None:
        document = pymupdf.open()
        for _ in range(pages):
            document.new_page()
        document.save(self.root / "dtracker_report.pdf")
        document.close()

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

    def test_valid_report_accepts_source_and_four_page_pdf(self) -> None:
        self.assertEqual(self.run_check().returncode, 0)
        self.write_pdf(4)
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_missing_section_fails(self) -> None:
        (self.root / "sections/03_method.tex").unlink()
        self.assert_fails_with(self.run_check(), "missing or incomplete section:")

    def test_titlepage_fails(self) -> None:
        self.write("main.tex", MAIN.replace("\\twocolumn", "\\begin{titlepage}X\\end{titlepage}\n\\twocolumn"))
        self.assert_fails_with(self.run_check(), "unexpected titlepage environment")

    def test_pdf_over_four_pages_fails(self) -> None:
        self.write_pdf(5)
        self.assert_fails_with(self.run_check(), "PDF exceeds 4 pages")

    def test_missing_original_paper_subsection_fails(self) -> None:
        path = self.root / "sections/04_experiments.tex"
        path.write_text(path.read_text().replace("Results from the Original Paper", "Results"))
        self.assert_fails_with(self.run_check(), "Original Paper")

    def test_missing_reproduction_subsection_fails(self) -> None:
        path = self.root / "sections/04_experiments.tex"
        path.write_text(path.read_text().replace("Our Reproduction", "Our Results"))
        self.assert_fails_with(self.run_check(), "Our Reproduction")


class DTrackerBibliographyTest(unittest.TestCase):
    def test_proceedings_metadata_matches_crossref_record(self) -> None:
        report_root = Path(__file__).resolve().parent.parent
        entry = (report_root / "references.bib").read_text()
        normalized = "".join(entry.split())
        self.assertIn("doi={10.1145/3690624.3709192}", normalized)
        self.assertIn("pages={460--471}", normalized)


if __name__ == "__main__":
    unittest.main()
