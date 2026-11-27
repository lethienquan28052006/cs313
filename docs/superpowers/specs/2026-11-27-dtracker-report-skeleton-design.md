# D-Tracker report skeleton — design

Date: 2026-11-27

## Intent

Create an Overleaf-ready, at-most-four-page English LaTeX skeleton for the D-Tracker KDD 2025 final project, based on the user's supplied `CS114_Report.zip` template. The user wants only an editable framework now, not a completed report.

## Layout decision

Use `IEEEtran` conference (the supplied template), not `acmart`. Do not keep its separate `titlepage`. Page 1 is a concise one-column title/information area plus table of contents. Following content uses the template's normal two-column layout and the required report sections, with a maximum total length of four pages. Section word/space budgets guide later editing without forcing artificial whitespace or changing template font/margins.

## Structure and content

Use a thin `main.tex`, `references.bib`, `sections/01_introduction.tex`, `02_problem_setup.tex`, `03_method.tex`, `04_experiments.tex`, `05_conclusion.tex`, `06_tasks.tex`, `images/` for the supplied optional university logo, `Makefile`, build/readme documents, generated `dtracker_report.pdf` and `dtracker_report_overleaf.zip`.

Write English section headings, short content guides and visibly styled placeholders for the title/team information, abstract, paragraph text, formulas/figures if needed, paper-vs-reproduction results and the tasks assigned to each member. Separate “Results from the original paper” from “Our reproduction,” and include no fabricated measurements or implementation claims. Include a real verified D-Tracker bibliographic entry and basic citation anchors without inventing completed report prose.

## Verification

Build locally with Tectonic/pdfLaTeX-compatible setup and compile the extracted Overleaf ZIP. Assert no LaTeX error, all required sections are present, PDF count is between one and four pages, reproduction/Demo outcomes remain unfilled, and sources in the ZIP match the worktree. Update `report/README.md` with the new layout, editing workflow and exact commands. No native visual inspection; check text/page count/log/bounds. Do not commit or push unless explicitly requested.
