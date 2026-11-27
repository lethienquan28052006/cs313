PYTHON ?= python3
PY_LIBS := ../slides/paper_explore/.tools/pylibs
BUILD := build
ifneq ($(wildcard .tools/tectonic),)
  TECTONIC := .tools/tectonic
else
  TECTONIC := $(shell command -v tectonic 2>/dev/null)
  ifeq ($(TECTONIC),)
    TECTONIC := ../slides/paper_explore/.tools/tectonic
  endif
endif

PDF := dtracker_report.pdf
ZIP := dtracker_report_overleaf.zip
OVERLEAF_FILES := main.tex references.bib sections images OVERLEAF.md README.md latexmkrc

.PHONY: all pdf check test overleaf-zip clean

all: pdf overleaf-zip

pdf: check
	mkdir -p $(BUILD)
	$(TECTONIC) --keep-logs --outdir $(BUILD) main.tex
	cp $(BUILD)/main.pdf $(PDF)

check:
	PYTHONPATH=$(PY_LIBS) $(PYTHON) scripts/test_check_report.py
	PYTHONPATH=$(PY_LIBS) $(PYTHON) scripts/check_report.py

test: check

overleaf-zip:
	rm -f $(ZIP)
	zip -r -X $(ZIP) $(OVERLEAF_FILES)

clean:
	rm -rf $(BUILD)
	rm -f $(PDF) $(ZIP)
