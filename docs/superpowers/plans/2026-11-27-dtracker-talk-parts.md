# D-Tracker Talk `parts/` Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Split the D-Tracker Beamer deck into seven narrative `parts/*.tex` files without changing any rendered content.

**Architecture:** Keep `main.tex` as the thin document entry point and move verbatim frame ranges into ordered input files. Extend the existing structural checker to expand LaTeX `\input` statements before performing its existing checks, then package and verify the same set of inputs on Overleaf.

**Tech Stack:** LaTeX Beamer, Tectonic/XeLaTeX, Python 3 `unittest`, Make, PyMuPDF, ZIP.

**Spec:** `docs/superpowers/specs/2026-11-27-dtracker-talk-parts-design.md`

## Global Constraints

- Move LaTeX content verbatim; do not address deferred editorial minors or change narrative, order, style or timing.
- Create exactly `00_cover`, `01_problem`, `02_methodology`, `03_experiments`, `04_reproduction`, `05_demo_conclusion`, `99_backup` under `parts/`.
- Preserve all `% SLIDE` markers, section/appendix placement, reproduction placeholders and the blank Demo.
- Keep figure paths and Overleaf compilation behavior working from the talk root.
- Do not perform native visual inspection; require page-text equivalence instead.
- User chose direct work on `feat/quan-slides`; no new worktree needed.
- Do not commit or push without an explicit user request.

## Review Focus

- Valid nested inputs: Task 1 tests expansion before matching slides/frames.
- Missing or cyclic inputs: Task 1 requires deterministic diagnostics instead of silent pass or recursion.
- Lost/reordered frames during mechanical split: Task 2 asserts lossless part concatenation and page-by-page text equality.
- Overleaf missing the new directory: Task 2 inspects ZIP contents and compiles the extracted package.
- Accidental rendered-content change: Task 2 performs clean log/bounds/page-count checks with no native image review.

---

### Task 1: Teach the Structural Checker to Read `parts/` Inputs

**Files:**
- Modify: `slides/dtracker_talk/scripts/check_deck.py`
- Modify: `slides/dtracker_talk/scripts/test_check_deck.py`

**Interfaces:**
- Produces: `source_with_inputs(root: Path, entry: Path, issues: list[str], seen: set[Path] | None = None) -> str`, used by `check(root)` to obtain expanded Beamer source before slide/frame/figure validation.

- [ ] **Step 1: Add three failing unit tests**

In `test_check_deck.py` add:
1. `test_nested_inputs_expand_and_pass`: `main.tex` inputs `parts/body`, which inputs `parts/frames`; the final file contains the valid slide 1 and A1 frames. Run `run_check()` and assert return code 0.
2. `test_missing_input_fails`: main inputs nonexistent `parts/missing`; assert the same `assert_fails_with(..., "input not found: parts/missing.tex")` behavior used for other diagnostics.
3. `test_input_cycle_fails`: `parts/a.tex` and `parts/b.tex` input each other around valid frame content; assert failure contains `input cycle:` and completes deterministically.

Input names without `.tex` must resolve to that suffix. Expansion must preserve the existing root-relative figure behavior and slide-marker ordering.

- [ ] **Step 2: Verify RED**

Run `python3 scripts/test_check_deck.py` from `slides/dtracker_talk`. Expected: the three new tests fail because `\input` is currently not expanded; the original six tests remain passing.

- [ ] **Step 3: Implement minimal recursive input expansion**

Add a compiled `\input{...}` matcher and `source_with_inputs(...)` with the interface above. Resolve relative names from talk root and append `.tex` only when no suffix exists. Return file contents with each input recursively expanded. Append `input not found: <relative-path>` or `input cycle: <relative-path>` to existing `issues`; track visited paths with the optional `seen` set. Call it in `check()` instead of bare `main.read_text()` before `OUTLINE_RE`, `SLIDE_RE`, frame or figure checks.

- [ ] **Step 4: Verify GREEN and the full checker suite**

Run `python3 scripts/test_check_deck.py && python3 scripts/check_deck.py` from `slides/dtracker_talk`. Expected: 9/9 tests PASS; existing deck stays valid.

### Task 2: Split the Deck, Package Inputs and Prove Rendered Equivalence

**Files:**
- Modify: `slides/dtracker_talk/main.tex`
- Create: `slides/dtracker_talk/parts/00_cover.tex`
- Create: `slides/dtracker_talk/parts/01_problem.tex`
- Create: `slides/dtracker_talk/parts/02_methodology.tex`
- Create: `slides/dtracker_talk/parts/03_experiments.tex`
- Create: `slides/dtracker_talk/parts/04_reproduction.tex`
- Create: `slides/dtracker_talk/parts/05_demo_conclusion.tex`
- Create: `slides/dtracker_talk/parts/99_backup.tex`
- Modify: `slides/dtracker_talk/Makefile`
- Modify: `slides/dtracker_talk/README.md`
- Modify: `slides/dtracker_talk/OVERLEAF.md`
- Regenerate: `slides/dtracker_talk/dtracker_talk.pdf`, `dtracker_talk_overleaf.zip`

**Interfaces:**
- Consumes: Task 1 `source_with_inputs(...)`.
- Produces: ordered inputs `00_cover → 01_problem → 02_methodology → 03_experiments → 04_reproduction → 05_demo_conclusion → 99_backup`; combined source remains identical to the original body.

- [ ] **Step 1: Capture the baseline before editing content**

Save a deterministic JSON record in this plan's ignored workspace containing all 33 values of `page.get_text()` in order, page count, 16:9 dimensions and outline timing total. Assert baseline is 33 pages, 29 main + 4 backup and 1,965 seconds.

- [ ] **Step 2: Extract and write the seven verbatim parts**

Split only at the existing literal boundaries:
- cover before `\section{Problem}`;
- `\section{Problem}` to before Methodology;
- Methodology to before Experiments;
- Experiments to before Reproduction;
- Reproduction to before Demo/conclusion;
- Demo/conclusion to before `\appendix`;
- `\appendix` through original document body end.

Before replacing `main.tex`, assert that concatenating all seven part bodies recreates the original body byte-for-byte. Write the parts and a thin `main.tex` retaining the original prefix through `\begin{document}` and ordered `\input{parts/<name>}` calls before `\end{document}`.

- [ ] **Step 3: Run structural verification after the split**

Run `make check`. Expected: 9/9 unit tests PASS, outline/deck marker lists match exactly, balanced 33 frames, every referenced figure found and no forbidden placeholders.

- [ ] **Step 4: Package and document the parts workflow**

Change `OVERLEAF_FILES` to include `parts`. In README and OVERLEAF document the seven files, which slide ranges they own, that editors should work there instead of editing generated outputs, and that ZIP includes `parts/`. Update source-layout documentation without altering deck content.

- [ ] **Step 5: Verify local and packaged builds against baseline**

Run `make clean && make all && make check`; extract ZIP into this plan's ignored workspace, compile it with Tectonic and assert 33 pages. Compare `page.get_text()` page-by-page with Task 2 Step 1 baseline. Expected: exact text equality for every page, unchanged 16:9 page size, unchanged timing and no layout/font/shrink errors beyond the documented Babel warning.

- [ ] **Step 6: Audit the final refactor and leave an uncommitted review checkpoint**

Run `git diff --check`, inspect `git diff --stat` and `git status --short`. Expected: intended seven new part files, thin-main/checker/tests/docs/ZIP/PDF changes only; no scratch directory committed or pushed. Report results and wait for an explicit user decision about committing/pushing.

## Self-Review

- Spec coverage: the seven-file split, checker expansion, tests, packaging/docs and render equivalence are all assigned.
- Step scan: each action has an exact boundary, interface, command or expected assertion.
- Interfaces: `check()` and Task 2 both rely on the same expansion helper; file naming and ordering match exactly.
- Review focus: valid/missing/cyclic inputs, missing package files, mechanical content loss and build drift each have explicit checks.
- Proportion: no LaTeX frame bodies are transcribed into this plan.
