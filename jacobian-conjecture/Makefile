# Run these from inside this topic folder: `cd jacobian-conjecture && make test`.
# The virtualenv is shared by every topic and lives at the repository root.
PY ?= $(CURDIR)/../.venv/bin/python
VENV := $(CURDIR)/../.venv

CHAPTER_SCRIPTS := $(wildcard src/viz/ch*.py)

.PHONY: help venv test figures $(CHAPTER_SCRIPTS:src/viz/%.py=%)

help:
	@echo "make venv      create the shared ../.venv and install the package + dev deps"
	@echo "make test      re-verify every mathematical claim in the guide"
	@echo "make figures   re-render every figure and GIF in guide/"
	@echo "make ch07_jacobian   re-render a single chapter's figures"

venv:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e ".[dev]"

test:
	$(PY) -m pytest tests/ -q

figures:
	@set -e; for f in $(CHAPTER_SCRIPTS); do \
		echo "== $$f"; (cd src/viz && $(PY) $$(basename $$f)); done

# `make ch05_linear_determinant` etc.
ch%:
	cd src/viz && $(PY) ch$*.py
