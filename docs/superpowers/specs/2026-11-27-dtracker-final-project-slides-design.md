# D-Tracker final-project slides — design

Date: 2026-11-27

## Intent and audience

Prepare a Vietnamese 30–35 minute undergraduate Data Mining presentation on the KDD 2025 D-Tracker paper. The audience has limited mathematical background. The presentation must explain the problem, the proposed technique, the paper's experiments and key findings, then reserve space for the team's reproduction results and a future demo.

## Scope

In scope:

- Download the original arXiv paper PDF from `https://arxiv.org/pdf/2505.00242` into the repository.
- Read the complete paper and maintain page/figure/table/equation evidence for claims used in the deck.
- Rewrite `slides/dtracker_talk/outline.md` with slide-by-slide purpose, timing, visuals, mathematical content and speaker cues.
- Restructure `slides/dtracker_talk/main.tex`, retaining the existing academic-clean Beamer theme unless a layout requires a small theme adjustment.
- Build the presentation PDF and Overleaf ZIP, run structural checks, and verify the packaged source compiles.
- Create clearly marked, structured placeholders for reproduction setup/results because the team has not supplied results.
- Leave a Demo slide blank apart from the common navigation elements and its Demo heading.

Out of scope for this iteration:

- Implementing or reproducing D-Tracker.
- Producing reproduction measurements or claims.
- Writing the four-page English report.
- Filling in the Demo.
- Pushing commits.

## Goals

- Lead with a concrete real-world problem before naming mathematical machinery.
- Explain the complete D-Tracker pipeline through one recurring social-interest example.
- Cover all methodological components in a way non-specialists can follow.
- Separate paper-reported experiments from the team's future reproduction.
- Fit the main talk into 30–35 minutes, with technical material moved to backup slides when useful.
- Preserve the current readable light-background, navy/gold visual system.

## Non-goals and anti-goals

- No abstract-only or heading-by-heading substitute for reading the paper.
- No proofs or symbol-heavy slide sequence.
- No fabrication of results, reproduction success, runtime, figures or implementation status.
- No ambiguous mixing of illustrative numbers with paper-reported numbers.
- No attempt to reproduce the reference seminar deck's 73-slide density.

## Approaches considered

1. **Restructure the deck around the final-project narrative (selected).** Keep the theme and useful diagrams but rewrite the flow as Problem → D-Tracker idea → example-led method → paper experiments → reproduction → blank Demo → conclusion. This directly matches the assignment and the audience.
2. **Minimally patch the existing deck.** Faster, but its applications emphasis and missing reproduction/demo narrative make it less suitable for the final project.

## Presentation design

Use approximately 26 main slides plus 3–4 backup slides. Timing budget:

- Opening and problem: 3–4 minutes.
- D-Tracker big picture: about 4 minutes.
- Example-led methodology: 11–13 minutes.
- Paper experiments and key findings: 5–6 minutes.
- Team reproduction placeholders: 3–4 minutes.
- Blank Demo placeholder: 2–3 minutes when eventually presented.
- Conclusion and Q&A: 1–2 minutes.

Use one recurring example: keyword/search-interest values observed for several keywords and locations over weekly time steps. Introduce tensor data as a stack of keyword-by-location tables, signal decomposition through visually distinct temporal behaviors, latent patterns/Tucker as shared patterns mixed with weights, diffusion as cross-channel influence, ALS as updating parameter blocks in turn, MDL/regime selection as balancing fit and complexity, and streaming as incorporating newly arriving observations. Each concept follows visual → plain-language explanation → minimal formula → small numeric check where a formula is shown.

Use plots for comparisons and trends; use diagrams for architecture, mechanics and conceptual structure; use tables for compact experimental configurations or quantitative comparisons. Label illustrative examples explicitly. Credit paper figures and anchor experimental claims to their paper locations.

## Deliverables and verification

Commit the downloaded source paper separately from the slide revision. Update all generated PDF/ZIP artifacts and current documentation affected by the new slide count or narrative. Verify page count, clean LaTeX build, structural checker tests, no overflow/missing glyphs/placeholders outside intentionally reserved reproduction/Demo areas, content within slide bounds, and a fresh compilation from the Overleaf ZIP. The native executor must not perform visual image review; delegate that review to DeepSeek with at most 4 images per prompt.

## Remaining builder decisions

The builder may adjust the exact slide count, visual layouts and concise Vietnamese wording after reading the paper, while preserving the approved narrative, audience level, scope and timing. Unsupported technical claims must be removed or corrected rather than carried over from the existing deck.
