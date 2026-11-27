# D-Tracker Final-Project Slides Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Verify the source D-Tracker paper and build a Vietnamese 30–35 minute Beamer deck that teaches the problem and method through concrete examples, reports the paper's experiments accurately, and reserves reproduction results and Demo for the team.

**Architecture:** Keep the existing academic-clean Beamer theme and structural checker. Establish a canonical source PDF and an evidence map first, then rewrite the outline and slide content together, extract only required paper figures, and regenerate and inspect all distributable artifacts.

**Tech Stack:** LaTeX Beamer, XeLaTeX/Tectonic, TikZ, Python 3 structural tests, PyMuPDF/pdf tooling, curl, Make, Overleaf ZIP.

**Spec:** `docs/superpowers/specs/2026-11-27-dtracker-final-project-slides-design.md`

## Global Constraints

- This iteration delivers only the PDF source, outline and slide artifacts; no implementation, reproduction measurements or four-page report.
- Use `slides/paper_explore/sources/paper.pdf` as the canonical in-repo paper unless verification shows it differs from arXiv; do not duplicate an identical PDF elsewhere.
- Read and validate the complete paper before rewriting experimental or methodological claims.
- Anchor paper claims to page/section/equation/figure/table locations and distinguish them from illustrative examples and future team results.
- Teach with one recurring keyword-by-location-by-time example and use visual → plain language → minimal formula → numeric check.
- Do not fabricate reproduction results or implementation claims; Demo remains intentionally blank except for common navigation and its title.
- Keep roughly 26–29 main slides plus 3–4 backup slides and a 30–35 minute budget.
- Do not push commits.
- Do not send more than 4 images in one prompt; the native executor must not perform visual image review. Delegate visual review to the available `bioturing/deepseek-v4.1-flash` model in batches of at most 4 images.

## Review Focus

- **Wrong or stale source PDF:** Task 1 compares the arXiv download with the tracked PDF by SHA-256 and validates page count/readability before analysis.
- **Existing slide claims not supported by the current paper:** Tasks 1 and 2 use the evidence map, then Task 4 audits every numeric experimental claim against that map.
- **Placeholders confused with measured reproduction results:** Task 2 uses explicit “Nhóm sẽ bổ sung sau khi chạy thực nghiệm” labels and Task 4 checks that no result cells contain invented values.
- **Demo accidentally filled or counted as completed work:** Task 2 keeps its content area empty and Task 4 inspects the rendered Demo page text/blocks.
- **Readable source but unusable projected slides:** Task 4 checks clean logs, text bounds, rendered pages and packaged rebuild in addition to `make check`.

---

### Task 1: Verify the Canonical Paper and Build the Evidence Map

**Files:**
- Verify/download: `slides/paper_explore/sources/paper.pdf`
- Read/update if needed: `slides/paper_explore/sources/source_map.md`
- Create: `slides/dtracker_talk/sources/source_map.md`
- Create: `slides/dtracker_talk/sources/figure_manifest.tsv`

**Interfaces:**
- Consumes: arXiv `https://arxiv.org/pdf/2505.00242` and the existing tracked paper.
- Produces: a validated canonical PDF and an evidence map keyed by problem, model, algorithm, experiments, findings and limitations for use in Task 2.

- [ ] **Step 1: Establish source-validation tooling**

Run `command -v curl pdfinfo pdftotext` and check the project PyMuPDF environment used by previous builds. If a PDF utility is unavailable, use the existing local Python/PyMuPDF environment rather than installing globally.

- [ ] **Step 2: Download and compare the original source**

Download to `/tmp/opencode/dtracker-2505.00242.pdf` with `curl --fail --location`. Validate that both source PDFs have matching, readable page counts. Compare SHA-256 hashes. If identical, retain the tracked file; if different, inspect metadata/text to establish the requested version before replacing it. Do not add a second copy of an identical PDF.

- [ ] **Step 3: Read the complete paper and record evidence**

Extract text page by page with verified PDF tooling and identify relevant figure/table anchors without native visual review. Record every slide-relevant statement in `slides/dtracker_talk/sources/source_map.md`: exact venue/title, task input/output, assumptions, each model component, estimation/model-selection/streaming procedure, all experimental research questions, dataset/baseline/metric setups, quantitative results, interpretation and limitations. Include precise page and section/equation/figure/table anchors and verbatim anchors for numeric claims. Correct any old source-map item that conflicts with the canonical PDF.

- [ ] **Step 4: Run the source-evidence gate**

Confirm the evidence map covers the full methodology and experiment sections rather than only selected highlights, that all quantitative claims have page/element anchors, and that no reproduction claims have entered the map. Record the PDF hash, URL, validation date and page count.

- [ ] **Step 5: Commit source verification**

If the PDF changed, commit it with the evidence files; otherwise commit only the new/updated evidence and reference the already tracked PDF.

```bash
git add slides/paper_explore/sources/paper.pdf slides/paper_explore/sources/source_map.md slides/dtracker_talk/sources/source_map.md slides/dtracker_talk/sources/figure_manifest.tsv
git commit -m "docs: verify D-Tracker paper evidence for slides"
```

### Task 2: Rewrite the Outline and Example-Led Slide Deck

**Files:**
- Modify: `slides/dtracker_talk/outline.md`
- Modify: `slides/dtracker_talk/main.tex`
- Modify only if required by layouts: `slides/dtracker_talk/theme.tex`
- Add/replace only required visuals: `slides/dtracker_talk/figures/`
- Modify: `slides/dtracker_talk/sources/figure_manifest.tsv`

**Interfaces:**
- Consumes: Task 1 `sources/source_map.md` and canonical paper.
- Produces: outline slide IDs exactly matching `% SLIDE` markers, all methodological/experimental content, reproduction placeholders and the blank Demo slide.

- [ ] **Step 1: Replace the outline with the final-project narrative**

Allocate 30–35 minutes across Opening/Problem → D-Tracker big picture → Method → Paper experiments → Team reproduction → Demo → Takeaways/Q&A. Remove the standalone applications-heavy section. For every slide specify purpose, seconds/minutes, visual, plain-language message, formula (if needed), numeric check, paper source and speaker cue. Use one keyword/location/week example throughout and send proof-like details to backup.

- [ ] **Step 2: Validate or extract required paper figures**

Reuse existing extracted figures only after checking their text anchors and coordinates against the canonical PDF. Extract any additional decisive experimental figure/table image with verified PDF tooling and save under `slides/dtracker_talk/figures/`; native visual inspection is deferred to DeepSeek in the final review. Record source page/element, crop or extraction command, output file and license/credit in `figure_manifest.tsv`. Prefer native plots/tables for recreated comparisons; do not create result graphics from unverified numbers.

- [ ] **Step 3: Implement the opening, problem and big-picture slides**

Start with a concrete decision problem, then introduce data shape, forecasting/diffusion questions and challenges. Show D-Tracker's complete input-to-output pipeline before individual mechanisms. Clearly label all story numbers as illustrative.

- [ ] **Step 4: Implement the methodology slides**

Explain tensor data, signal decomposition, latent patterns/Tucker, diffusion, full model, ALS estimation, MDL/model selection, regime changes and streaming using the recurring example. Each formula must have annotated symbols and either a small numerical substitution or a concrete interpretation. Keep complete derivations and extra equations in backup slides; use TikZ for architecture/mechanism concepts rather than plots.

- [ ] **Step 5: Implement paper experiments and key findings**

Cover experimental questions, real dataset setup, baselines, metrics and the exact runs behind every reported result. Use native tables/plots where they aid comparison and validated paper crops where source details matter. Separate quantitative results, interpretation and limitations; include the paper's scalability/additional analyses when supported by Task 1 evidence.

- [ ] **Step 6: Add reproduction placeholders and blank Demo**

Create reproduction slides for environment/data/configuration, Paper-vs-team result table, runtime/behavior comparison and lessons/differences. Label empty fields “Nhóm sẽ bổ sung sau khi chạy thực nghiệm” rather than inserting zeroes or paper values as team measurements. Add a titled Demo frame whose content area is intentionally empty. End with concise takeaways and Q&A.

- [ ] **Step 7: Run structural checks and build**

Run:

```bash
cd slides/dtracker_talk
make check
make pdf
```

Expected: all checker unit tests pass, outline/deck IDs match, every `\begin{frame}` has an `\end{frame}`, referenced figures exist, Tectonic writes the PDF, and no LaTeX error/overflow/shrink/missing-glyph warning remains.

- [ ] **Step 8: Commit the reworked source**

```bash
git add slides/dtracker_talk/outline.md slides/dtracker_talk/main.tex slides/dtracker_talk/theme.tex slides/dtracker_talk/figures slides/dtracker_talk/sources/figure_manifest.tsv slides/dtracker_talk/dtracker_talk.pdf
git commit -m "slides: restructure D-Tracker final project narrative"
```

### Task 3: Update Documentation and Reproducible Packages

**Files:**
- Modify: `slides/dtracker_talk/README.md`
- Modify: `slides/dtracker_talk/OVERLEAF.md`
- Regenerate: `slides/dtracker_talk/dtracker_talk_overleaf.zip`
- Add planning records: `docs/superpowers/specs/2026-11-27-dtracker-final-project-slides-design.md`, this plan

**Interfaces:**
- Consumes: Task 2 final slide count, structure, figures and build outputs.
- Produces: documentation and Overleaf package consistent with the deck.

- [ ] **Step 1: Update documentation**

Describe the approved scope, narrative, actual main/backup slide counts, intentional reproduction placeholders, blank Demo, source-paper location, evidence map, build/check commands and generated artifacts. Ensure Overleaf instructions and included-file lists match the ZIP configuration.

- [ ] **Step 2: Regenerate the Overleaf ZIP**

Run `make overleaf-zip` from `slides/dtracker_talk`; inspect its file list to ensure required source/figures are present while evidence files and unrelated large artifacts are not accidentally included.

- [ ] **Step 3: Rebuild from the packaged source**

Extract the ZIP into a temporary directory under `/tmp/opencode`, compile its `main.tex` with Tectonic, and assert that its PDF page count equals `dtracker_talk.pdf`.

- [ ] **Step 4: Commit documentation and packaging**

```bash
git add slides/dtracker_talk/README.md slides/dtracker_talk/OVERLEAF.md slides/dtracker_talk/dtracker_talk_overleaf.zip docs/superpowers/specs/2026-11-27-dtracker-final-project-slides-design.md docs/superpowers/plans/2026-11-27-dtracker-final-project-slides.md
git commit -m "docs: package D-Tracker final project slides"
```

### Task 4: Final Content, Layout and Repository Verification

**Files:**
- Verify all Task 1–3 outputs; modify only defects discovered during verification.

**Interfaces:**
- Consumes: all prior outputs.
- Produces: final verified, committed working tree with no unpushed action taken.

- [ ] **Step 1: Audit content against evidence**

Check every method statement and experimental number on slides against `sources/source_map.md`. Confirm illustrative values are labeled, paper results are not called reproduced results, reproduction fields contain no invented measurements, Demo is blank, and the talk covers problem/methodology/experiments/key findings.

- [ ] **Step 2: Run clean source and structural verification**

Run `make clean && make all && make check` in `slides/dtracker_talk`. Grep the final log for errors, overfull/underfull boxes, unexpected shrinking, undefined references and missing characters; only the already documented Vietnamese Babel hyphenation warning may remain.

- [ ] **Step 3: Inspect rendered layout**

Use PyMuPDF to assert a 16:9 page size, expected page count, no non-footer text outside safe bounds and no unresolved `??`. Render cover, recurring-example method slides, experiment plots/tables, reproduction placeholders, Demo and closing slide. The native executor must not visually inspect them; send rendered pages to DeepSeek for review in prompts containing at most 4 images each and use its findings for any required fix pass.

- [ ] **Step 4: Recheck package and timing**

Repeat the ZIP compilation after any fix, compare page counts, and sum the outline timings to ensure the main presentation fits 30–35 minutes without counting backup slides.

- [ ] **Step 5: Verify repository state**

Run `git status --short` and `git log -3 --oneline`. Any verification fix must be committed in a small corrective commit. Expected: clean working tree, new commits present locally, and no push performed.

## Self-Review

- Spec coverage: Tasks 1–4 cover source verification, full-paper evidence, outline/slides, recurring examples, paper experiments, reproduction placeholders, blank Demo, artifacts, checks and local commits. Implementation/report/push are explicitly excluded.
- Step scan: each step has a concrete artifact, command or verification result; no unresolved placeholder steps remain in the plan itself.
- Interface consistency: Task 1 evidence and figure manifest feed Task 2; Task 2 final IDs/counts/artifacts feed Tasks 3–4.
- Review focus: every listed failure mode has a corresponding source, structural, content or rendered-output check.
- Proportion: repeated LaTeX bodies and final experimental numbers are deliberately left to implementation after full-paper reading rather than guessed in the plan.
