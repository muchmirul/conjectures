# Run these from inside this topic folder: `cd zeta-critical-line && make test`.
# The virtualenv is shared by every topic and lives at the repository root.
PY ?= $(CURDIR)/../.venv/bin/python
VENV := $(CURDIR)/../.venv

CHAPTER_SCRIPTS := $(wildcard src/viz/ch*.py)

# chapter targets are deliberately not .PHONY: make only applies the ch% rule
# below to targets it has not been told are phony
.PHONY: help venv test figures docs guide play

help:
	@echo "make venv      create the shared ../.venv and install the package + dev deps"
	@echo "make test      re-verify every number the guide quotes"
	@echo "make figures   re-render every figure in guide/"
	@echo "make docs      rebuild ../docs/zeta-critical-line/index.html from ARTICLE.md"
	@echo "make guide     rebuild every guide/NN-.../README.md from ARTICLE.md"
	@echo "make play      rebuild the playable pages in ../docs/zeta-critical-line/play/"
	@echo "make ch03_the_music   re-render a single chapter's figures"

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e ".[dev]"

test:
	$(PY) -m pytest tests/ -q

figures:
	@set -e; for f in $(CHAPTER_SCRIPTS); do \
		echo "== $$f"; (cd src/viz && $(PY) $$(basename $$f)); done

docs:
	$(PY) build_docs.py

guide:
	$(PY) build_guide.py

play:
	$(PY) build_interactive.py

# `make ch03_the_music` etc.
ch%:
	cd src/viz && $(PY) ch$*.py
