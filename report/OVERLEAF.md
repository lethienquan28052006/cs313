# Upload D-Tracker report skeleton to Overleaf

## Import

1. Upload `dtracker_report_overleaf.zip` as a new Overleaf project.
2. Set **Main document** to `main.tex`.
3. Set **Compiler** to **pdfLaTeX** (not XeLaTeX; the template uses `inputenc` and T5 font encoding).
4. Click **Recompile**.

Expected current output: **3 pages**. The editable report may grow to at most 4 pages. Do not reduce font size or margins to hide overflow.

## Included files

```text
main.tex          # Thin IEEEtran entry point
references.bib    # Verified D-Tracker citation and future references
sections/        # Six required report sections
images/          # Optional logo copied from supplied user template
README.md        # Editing/build notes
OVERLEAF.md      # This quick guide
latexmkrc        # pdfLaTeX selection
```

No paper PDF, experiment outputs, raw template archive, test scripts, local compiler or unrelated template figure is included.

## Editing

- Work in `sections/`, not in generated PDF or ZIP.
- Replace every `\pending{...}` with real report content.
- Complete course/team/member metadata on page 1 and actual Task Assignment entries.
- Keep `Results from the Original Paper` and `Our Reproduction` separate. Do not relabel paper values as team results.
- Add BibTeX entries to `references.bib` and cite them in the corresponding paragraphs.

When replacing placeholders with longer paragraphs or figures, run `make check` locally if possible and verify the final report stays within four pages.
