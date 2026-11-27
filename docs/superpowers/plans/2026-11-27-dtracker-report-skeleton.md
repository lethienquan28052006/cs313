# D-Tracker Report Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a four-page-maximum English IEEEtran report skeleton with an editable one-column information/ToC first page, required two-column report sections and an Overleaf-ready package.

**Architecture:** Reuse the supplied template's IEEEtran conventions, stripped to a small reproducible preamble. Keep metadata and ordered inputs in `report/main.tex`; isolate each required report section under `report/sections/`; use a small source/PDF checker to prevent missing sections and page-limit regressions.

**Tech Stack:** `IEEEtran`, pdfLaTeX-compatible LaTeX, Tectonic, BibTeX, Python `unittest`, PyMuPDF, Make and ZIP.

**Spec:** `docs/superpowers/specs/2026-11-27-dtracker-report-skeleton-design.md`

## Global Constraints

- English skeleton only; do not fabricate completed report paragraphs, implementation status, reproduction results or team assignments.
- No separate `titlepage`; one-column information + ToC first page, then two-column body; total PDF length must be at most four pages.
- Required sections: Introduction, Problem Setup, Method, Experiments (Original Paper vs. Our Reproduction), Conclusion and Task Assignment.
- Keep supplied `IEEEtran` template style rather than changing to `acmart`; do not shrink template font/margins to force the cap.
- User chose direct work on `feat/quan-slides`; no new worktree needed. Do not commit or push without an explicit request.
- No native visual inspection; use source checks, PDF text/dimensions/bounds and logs.

## Review Focus

- Missing section or accidental loss of separate reproduction: Task 1 assert-fails when a required file/subsection is absent.
- Unexpected separate cover environment: Task 1 rejects literal `\begin{titlepage}` in main.tex.
- More than four pages: Task 1 creates real five-page/four-page PyMuPDF fixtures and verifies failure/pass behavior.
- Package missing inputs: Task 2 verifies required source/logo/BibTeX identity and compiles the ZIP extraction.
- Fabricated status/results: Task 2 audits the visible placeholder convention and checks that original-paper and team sections stay distinct.

---

### Task 1: Add a Failing-First Source/Page Checker and Build the Skeleton

**Files:**
- Create: `report/scripts/check_report.py`
- Create: `report/scripts/test_check_report.py`
- Create: `report/main.tex`, `report/references.bib`, `report/latexmkrc`
- Create: `report/sections/01_introduction.tex`, `02_problem_setup.tex`, `03_method.tex`, `04_experiments.tex`, `05_conclusion.tex`, `06_tasks.tex`
- Create: `report/images/Logo_UIT.svg.png` from the user-supplied ZIP
- Create: `report/Makefile`
- Produce: `report/dtracker_report.pdf`

**Interfaces:**
- Produces `check(root: Path) -> list[str]`: validates required main/sections/anti-titlepage constraints and validates `dtracker_report.pdf` ≤4 pages when that file exists.
- Produces a one-column first-page block followed by `\tableofcontents`, `\clearpage` and `\twocolumn`; `main.tex` sequences all six section inputs before references.

- [ ] **Step 1: Write failing checker tests**

Use a temporary fixture root with real files. Test four behaviors:
1. A fixture containing the six required input sections and title-page-free main passes when no PDF exists, then passes again with a real four-page PDF.
2. Deleting a required section produces `missing or incomplete section:` rather than a silent pass.
3. A literal `\begin{titlepage}` in main produces `unexpected titlepage environment`.
4. A real five-page PDF produces `PDF exceeds 4 pages`; deleting the required `Results from the Original Paper` or `Our Reproduction` subsection produces a separate reproduction error.

Define expected section headings as Introduction, Problem Setup, Method, Experiments, Conclusion, Task Assignment. Derive every fixture expectation independently with PyMuPDF `new_page()` page objects, not PDF image inspection.

- [ ] **Step 2: Verify RED before implementation/scaffolding**

Run the tests using `PYTHONPATH=../slides/paper_explore/.tools/pylibs` from `report/`. Expected: failures because `check_report.py`/scaffold do not exist, not because fixtures are wrong.

- [ ] **Step 3: Implement checker and minimal LaTeX scaffold**

Implement source error collection and optional PDF page-count validation. Reuse the supplied template's IEEEtran/T5/inputenc/babel graphics/booktabs/hyperref style without its long report content. Add a clear `\pending{...}` placeholder convention and a real D-Tracker BibTeX entry (`10.1145/3690624.3709192`, arXiv:2505.00242v1). Use placeholders for title/course/instructor/member names and for all report prose/results. Experiments must explicitly keep Original Paper and Our Reproduction separate. Copy only the optional university logo from the supplied ZIP; unrelated template figures stay excluded.

- [ ] **Step 4: Add reproducible build/check commands and verify GREEN**

Provide Makefile targets `all`, `pdf`, `check`, `overleaf-zip`, `clean`, using system Tectonic or `../slides/paper_explore/.tools/tectonic` and local PyMuPDF path. Run checker unit tests, `make check && make pdf`; expected checker PASS and a build with no fatal LaTeX/font/layout errors and at most four pages.

### Task 2: Document, Package and Verify the Overleaf Workflow

**Files:**
- Modify: `report/README.md`
- Create: `report/OVERLEAF.md`
- Regenerate: `report/dtracker_report.pdf`, `report/dtracker_report_overleaf.zip`

**Interfaces:**
- Consumes: Task 1 local checker/PDF/layout.
- Produces: ZIP containing main.tex, references.bib, latexmkrc, six inputs, optional logo and instructions, with no verdict about unwritten content.

- [ ] **Step 1: Document editing and page budget**

Describe page-one information/ToC followed by the two-column body; file ownership and section ranges; how to replace `\pending{}`; required member-task content; Original Paper vs. Our Reproduction separation; `make all/check/overleaf-zip/clean`; XeLaTeX is not required—use pdfLaTeX on Overleaf. State that the short skeleton can occupy fewer than four pages and later content must not exceed four without changing template typography/margins.

- [ ] **Step 2: Generate and audit ZIP**

Run `make all && make check`. Verify archive integrity and exact worktree hashes for all required LaTeX/BibTeX/image entries. Confirm no test artifacts, original unrelated report images or simulated result files are in the archive.

- [ ] **Step 3: Prove packaged compilation and output constraints**

Extract in this plan's ignored workspace, compile `main.tex` with Tectonic, and compare package/worktree page text and page count. Run checker against both roots; assert total PDF ≤4 pages and no missing sections or titlepage. Inspect logs for fatal errors, missing glyphs and overfull content. Check via text blocks that content stays within page bounds; no native image review.

- [ ] **Step 4: Leave a reviewed, uncommitted checkpoint**

Run `git diff --check`, `git status --short` and a final fresh whole-checkpoint review. Record all completed verification, then report the PDF/ZIP/source locations and wait for an explicit user decision about commit/push.

## Self-Review

- Spec coverage: template fidelity, one-column first page/ToC, two-column required sections, English placeholders, real D-Tracker citation, page cap, docs and packaging are assigned.
- Step scan: tests assert behavior on real temporary files/PDFs and give exact reproduction conditions.
- Interfaces: Task 1's `check(root)` is reused for local and packaged roots; required title/subsection strings agree across tests and scaffold.
- Review focus: five stated failure modes have executable checks or explicit audit steps rather than visual guessing.
- Proportion: detailed paper/report prose remains outside scope; the plan describes only structure and validation.
