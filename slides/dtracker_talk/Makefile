PYTHON ?= python3
BUILD := build
LOCAL_TECTONIC := $(CURDIR)/.tools/tectonic
SIBLING_TECTONIC := $(abspath ../paper_explore/.tools/tectonic)
SYSTEM_TECTONIC := $(shell command -v tectonic 2>/dev/null)
LATEXMK := $(shell command -v latexmk 2>/dev/null)
XELATEX := $(shell command -v xelatex 2>/dev/null)

ifeq ($(SYSTEM_TECTONIC),)
  ifneq ($(wildcard $(SIBLING_TECTONIC)),)
    ENGINE := $(SIBLING_TECTONIC)
    TOOL_PREREQ :=
  else
    ENGINE := $(LOCAL_TECTONIC)
    TOOL_PREREQ := $(LOCAL_TECTONIC)
  endif
else
  ENGINE := $(SYSTEM_TECTONIC)
  TOOL_PREREQ :=
endif

OVERLEAF_ZIP := dtracker_talk_overleaf.zip
OVERLEAF_FILES := main.tex theme.tex latexmkrc OVERLEAF.md figures fonts parts

.PHONY: all pdf overleaf-zip check test clean

all: pdf overleaf-zip

ifneq ($(and $(LATEXMK),$(XELATEX)),)
pdf: check
	mkdir -p $(BUILD)
	$(LATEXMK) -xelatex -interaction=nonstopmode -halt-on-error -outdir=$(BUILD) main.tex
	cp $(BUILD)/main.pdf dtracker_talk.pdf
else
pdf: check $(TOOL_PREREQ)
	mkdir -p $(BUILD)
	$(ENGINE) --keep-logs --outdir $(BUILD) main.tex
	cp $(BUILD)/main.pdf dtracker_talk.pdf
endif

overleaf-zip:
	rm -f $(OVERLEAF_ZIP)
	zip -r -X $(OVERLEAF_ZIP) $(OVERLEAF_FILES)

check:
	$(PYTHON) scripts/test_check_deck.py
	$(PYTHON) scripts/check_deck.py

test: check

$(LOCAL_TECTONIC):
	./scripts/install_tectonic.sh

clean:
	rm -rf $(BUILD)
	rm -f dtracker_talk.pdf $(OVERLEAF_ZIP)
