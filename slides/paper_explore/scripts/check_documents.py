#!/usr/bin/env python3
"""Structural checks shared by the Vietnamese and English explainers."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LANGUAGES = ("vi", "en")
INPUT_RE = re.compile(r"\\input\{([^}]+)\}")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
FIGURE_RE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD)\b|chưa điền", re.IGNORECASE)
SELFCHECK = r"\begin{selfcheck}"


def included_inputs(main: Path) -> list[str]:
    return [name.removesuffix(".tex") for name in INPUT_RE.findall(main.read_text())]


def resolve_input(root: Path, name: str) -> Path:
    path = root / name
    return path if path.suffix else path.with_suffix(".tex")


def check(root: Path) -> list[str]:
    issues: list[str] = []
    mains = {language: root / f"dtracker_explained_{language}.tex" for language in LANGUAGES}
    for language, main in mains.items():
        if not main.is_file():
            issues.append(f"missing main document ({language}): {main.name}")
    if issues:
        return issues

    chapters: dict[str, list[str]] = {}
    files: dict[str, list[Path]] = {}
    for language, main in mains.items():
        chapters[language] = included_inputs(main)
        files[language] = [main]
        for name in chapters[language]:
            path = resolve_input(root, name)
            if not path.is_file():
                issues.append(f"input not found ({language}): {name}")
            else:
                files[language].append(path)

    if len(chapters["vi"]) != len(chapters["en"]):
        issues.append(
            f"chapter mismatch: vi has {len(chapters['vi'])}, "
            f"en has {len(chapters['en'])}"
        )
    else:
        vi_names = [Path(name).name for name in chapters["vi"]]
        en_names = [Path(name).name for name in chapters["en"]]
        if vi_names != en_names:
            issues.append(f"chapter mismatch: vi={vi_names}, en={en_names}")

    selfchecks: dict[str, int] = {}
    label_sets: dict[str, set[str]] = {}
    for language in LANGUAGES:
        labels: dict[str, int] = {}
        selfchecks[language] = 0
        for path in files[language]:
            text = path.read_text()
            for match in LABEL_RE.finditer(text):
                labels[match.group(1)] = labels.get(match.group(1), 0) + 1
            selfchecks[language] += text.count(SELFCHECK)
            if PLACEHOLDER_RE.search(text):
                issues.append(f"placeholder ({language}): {path.relative_to(root)}")
            for raw in FIGURE_RE.findall(text):
                if "#" in raw:
                    # A shared macro parameter, not a literal asset reference.
                    continue
                figure = root / raw
                candidates = [figure] if figure.suffix else [
                    figure.with_suffix(ext) for ext in (".png", ".pdf", ".jpg", ".jpeg")
                ]
                if not any(candidate.is_file() for candidate in candidates):
                    issues.append(
                        f"figure not found ({language}): {raw} in {path.relative_to(root)}"
                    )
        label_sets[language] = set(labels)
        duplicates = sorted(label for label, count in labels.items() if count > 1)
        if duplicates:
            issues.append(f"duplicate label ({language}): {', '.join(duplicates)}")

    if label_sets["vi"] != label_sets["en"]:
        only_vi = sorted(label_sets["vi"] - label_sets["en"])
        only_en = sorted(label_sets["en"] - label_sets["vi"])
        issues.append(f"label mismatch: only vi={only_vi}, only en={only_en}")

    if selfchecks["vi"] != selfchecks["en"]:
        issues.append(
            f"selfcheck mismatch: vi has {selfchecks['vi']}, "
            f"en has {selfchecks['en']}"
        )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="document root (default: parent of scripts/)",
    )
    args = parser.parse_args()
    issues = check(args.root.resolve())
    if issues:
        print("FAIL: document structure check")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print("PASS: main documents, chapters, labels, placeholders, figures, and parity are valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
