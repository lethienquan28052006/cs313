#!/usr/bin/env python3
"""Validate the D-Tracker report skeleton and its four-page limit."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pymupdf

REQUIRED_SECTIONS = (
    ("01_introduction", "Introduction"),
    ("02_problem_setup", "Problem Setup"),
    ("03_method", "Method"),
    ("04_experiments", "Experiments"),
    ("05_conclusion", "Conclusion"),
    ("06_tasks", "Task Assignment"),
)


def check(root: Path) -> list[str]:
    """Return structural and page-count issues for a report root."""
    root = root.resolve()
    issues: list[str] = []
    main = root / "main.tex"
    if not main.is_file():
        issues.append("missing main.tex")
    else:
        source = main.read_text()
        if r"\begin{titlepage}" in source:
            issues.append("unexpected titlepage environment")
        for command in (r"\tableofcontents", r"\twocolumn"):
            if command not in source:
                issues.append(f"missing layout command: {command}")
        if r"\bibliography{references}" not in source:
            issues.append("missing references bibliography")

        for name, title in REQUIRED_SECTIONS:
            relative = f"sections/{name}.tex"
            if rf"\input{{sections/{name}}}" not in source:
                issues.append(f"missing or incomplete section input: {relative}")
            section = root / relative
            if not section.is_file() or rf"\section{{{title}}}" not in section.read_text():
                issues.append(f"missing or incomplete section: {relative}")

        experiments = root / "sections/04_experiments.tex"
        if experiments.is_file():
            body = experiments.read_text()
            for heading in ("Results from the Original Paper", "Our Reproduction"):
                if rf"\subsection{{{heading}}}" not in body:
                    issues.append(f"missing reproduction subsection: {heading}")

    pdf = root / "dtracker_report.pdf"
    if pdf.is_file():
        with pymupdf.open(pdf) as document:
            if document.page_count > 4:
                issues.append(f"PDF exceeds 4 pages: {document.page_count}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    issues = check(args.root)
    if issues:
        print("FAIL: report structure check")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("PASS: report sections, layout, reproduction separation and four-page limit are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
