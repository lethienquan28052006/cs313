#!/usr/bin/env python3
"""Check that outline and Beamer deck stay in sync."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

OUTLINE_RE = re.compile(r"^### Slide (S?[0-9]+|A[0-9]+)\b", re.MULTILINE)
SLIDE_RE = re.compile(r"^% SLIDE (S?[0-9]+|A[0-9]+)\s*$", re.MULTILINE)
FIGURE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD)\b|chưa điền", re.IGNORECASE)


def check(root: Path) -> list[str]:
    outline = root / "outline.md"
    main = root / "main.tex"
    issues: list[str] = []
    if not outline.is_file():
        issues.append(f"missing outline: {outline.name}")
    if not main.is_file():
        issues.append(f"missing deck: {main.name}")
    if issues:
        return issues

    expected = OUTLINE_RE.findall(outline.read_text())
    source = main.read_text()
    actual = SLIDE_RE.findall(source)
    if expected != actual:
        issues.append(f"slide mismatch: outline={expected}, deck={actual}")

    begin = len(re.findall(r"\\begin\{frame\}", source))
    end = len(re.findall(r"\\end\{frame\}", source))
    if begin != end or begin != len(expected):
        issues.append(f"frame mismatch: begin={begin}, end={end}, expected={len(expected)}")

    if PLACEHOLDER_RE.search(source) or PLACEHOLDER_RE.search(outline.read_text()):
        issues.append("placeholder TODO/TBD remains")

    for raw in FIGURE_RE.findall(source):
        if "#" in raw:
            continue
        candidate = root / raw
        if not candidate.is_file():
            issues.append(f"figure not found: {raw}")

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    issues = check(args.root.resolve())
    if issues:
        print("FAIL: deck structure check")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("PASS: outline, slide markers, frame balance, placeholders, and figures are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
