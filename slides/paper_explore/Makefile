PYTHON ?= python3
BUILD := build
LOCAL_TECTONIC := $(CURDIR)/.tools/tectonic
SYSTEM_TECTONIC := $(shell command -v tectonic 2>/dev/null)

ifeq ($(SYSTEM_TECTONIC),)
ENGINE := $(LOCAL_TECTONIC)
TOOL_PREREQ := $(LOCAL_TECTONIC)
else
ENGINE := $(SYSTEM_TECTONIC)
TOOL_PREREQ :=
endif

.PHONY: all vi en check test clean

all: vi en

vi: $(TOOL_PREREQ) check
	mkdir -p $(BUILD)
	$(ENGINE) --keep-logs --outdir $(BUILD) dtracker_explained_vi.tex
	cp $(BUILD)/dtracker_explained_vi.pdf dtracker_explained_vi.pdf

en: $(TOOL_PREREQ) check
	mkdir -p $(BUILD)
	$(ENGINE) --keep-logs --outdir $(BUILD) dtracker_explained_en.tex
	cp $(BUILD)/dtracker_explained_en.pdf dtracker_explained_en.pdf

check:
	$(PYTHON) scripts/test_check_documents.py
	$(PYTHON) scripts/check_documents.py

test: check

$(LOCAL_TECTONIC):
	./scripts/install_tectonic.sh

clean:
	rm -rf $(BUILD)
	rm -f dtracker_explained_vi.pdf dtracker_explained_en.pdf
