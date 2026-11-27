# D-Tracker talk `parts/` refactor — design

Date: 2026-11-27

## Intent

Make the 1,256-line Beamer deck easier to edit by splitting it into narrative source files, with no content, ordering, styling, timing or visual changes.

## Selected approach

Use `parts/00_cover.tex` (slide 1), `01_problem.tex` (2–6), `02_methodology.tex` (7–18), `03_experiments.tex` (19–24), `04_reproduction.tex` (25–27), `05_demo_conclusion.tex` (28–29) and `99_backup.tex` (A1–A4). Reduce `main.tex` to preamble, metadata and ordered `\input` calls. The alternative of 33 one-slide files was rejected because it creates unnecessary file-management overhead for section-level edits.

## Goals and constraints

- Move LaTeX content verbatim and preserve section/appendix placement.
- Keep all `% SLIDE` markers paired with their frames and matching `outline.md`.
- Support `\input{parts/...}` in the durable structural checker, including missing-input diagnostics and input chains without modifying figure resolution semantics.
- Add `parts/` to Overleaf ZIP and update README/OVERLEAF editing instructions.
- Preserve the canonical paper, claim ledger, reproduction placeholders, blank Demo and every previously identified deferred minor.
- Refactor only: no narrative changes, no implementation/reproduction/report work and no native visual inspection.
- Do not commit or push without an explicit user request.

## Verification

Before refactoring, capture the current PDF page count and normalized page text. Add failing checker tests for valid input files and missing inputs, then implement input expansion. Run all checker tests, clean-build main PDF and ZIP, compile the packaged source, compare normalized text per page with the baseline, inspect the final source differences, and confirm working-tree/remote state. No image-review prompt is needed because this refactor must not alter rendered content.
