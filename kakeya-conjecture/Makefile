# Run these from inside this topic folder: `cd kakeya-conjecture && make test`.
# The virtualenv is shared by every topic and lives at the repository root.
PY ?= $(CURDIR)/../.venv/bin/python
VENV := $(CURDIR)/../.venv

CHAPTER_SCRIPTS := $(wildcard src/viz/ch*.py)

# chapter targets are deliberately not .PHONY: make only applies the ch% rule
# below to targets it has not been told are phony
.PHONY: help venv test figures docs

help:
	@echo "make venv      create the shared ../.venv and install the package + dev deps"
	@echo "make test      re-verify every mathematical claim in the guide"
	@echo "make figures   re-render every figure in guide/"
	@echo "make docs      rebuild ../docs/kakeya-conjecture/index.html from ARTICLE.md"
	@echo "make ch05_the_perron_tree   re-render a single chapter's figures"

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

# `make ch05_the_perron_tree` etc.
ch%:
	cd src/viz && $(PY) ch$*.py
