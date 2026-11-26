PYTHON ?= python3
BUILD := build
LOCAL_TECTONIC := $(CURDIR)/.tools/tectonic
SIBLING_TECTONIC := $(abspath ../paper_explore/.tools/tectonic)
SYSTEM_TECTONIC := $(shell command -v tectonic 2>/dev/null)

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

.PHONY: all check test clean

all: check
	mkdir -p $(BUILD)
	$(ENGINE) --keep-logs --outdir $(BUILD) main.tex
	cp $(BUILD)/main.pdf dtracker_talk.pdf

check:
	$(PYTHON) scripts/test_check_deck.py
	$(PYTHON) scripts/check_deck.py

test: check

$(LOCAL_TECTONIC):
	./scripts/install_tectonic.sh

clean:
	rm -rf $(BUILD)
	rm -f dtracker_talk.pdf
