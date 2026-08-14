# Run these from inside this topic folder: `cd condensed-math && make test`.
# The virtualenv is shared by every topic and lives at the repository root.
PY ?= $(CURDIR)/../.venv/bin/python
VENV := $(CURDIR)/../.venv

PART_SCRIPTS := $(wildcard src/viz/part*_figures.py)

.PHONY: help venv test figures docs guide play all part1 part2 part3

help:
	@echo "make venv      create the shared ../.venv and install the package + dev deps"
	@echo "make test      recompute every number the three articles quote"
	@echo "make figures   re-render every figure of every part"
	@echo "make guide     rebuild every parts/*/guide/NN-.../README.md from the articles"
	@echo "make docs      rebuild ../docs/condensed-math/ from the articles"
	@echo "make play      rebuild the 27 playable pages"
	@echo "make all       guide, docs and play in one go"
	@echo "make part2     re-render one part's figures"

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e ".[dev]"

test:
	$(PY) -m pytest tests/ -q

figures:
	@set -e; for f in $(PART_SCRIPTS); do \
		echo "== $$f"; (cd src/viz && $(PY) $$(basename $$f)); done

guide:
	$(PY) build_guide.py

docs:
	$(PY) build_docs.py

play:
	$(PY) build_interactive.py

all: guide play docs

# `make part1` etc: re-render a single part's figures
part1 part2 part3:
	cd src/viz && $(PY) $@_figures.py
