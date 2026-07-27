# Repository root. Every topic is a self-contained folder with its own Makefile.
# Add a new topic by creating its folder and adding its name here.
TOPICS := jacobian-conjecture kakeya-conjecture

VENV := $(CURDIR)/.venv

.PHONY: help venv test figures topics

help:
	@echo "make venv      create the shared .venv and install every topic"
	@echo "make test      run the tests of every topic"
	@echo "make figures   re-render the figures of every topic"
	@echo "make topics    list the topics in this repo"
	@echo
	@echo "To work on one topic:  cd jacobian-conjecture && make test"

topics:
	@for t in $(TOPICS); do echo "$$t"; done

venv:
	python3 -m venv $(VENV)
	@set -e; for t in $(TOPICS); do $(VENV)/bin/pip install -e "./$$t[dev]"; done

test:
	@set -e; for t in $(TOPICS); do echo "== $$t"; $(MAKE) -C $$t test; done

figures:
	@set -e; for t in $(TOPICS); do echo "== $$t"; $(MAKE) -C $$t figures; done
