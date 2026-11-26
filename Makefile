# Makefile for KTU Activity Points Checker
# Operating contract as defined in agent.md §8.2

SHELL := /bin/bash
VENV := .venv
PYTHON := $(VENV)/bin/python
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
MYPY := $(VENV)/bin/mypy
LINT_IMPORTS := $(VENV)/bin/lint-imports

.PHONY: help setup lint test test-golden test-e2e mutation rules-check gen-docs gate

help:
	@echo "KTU Activity Points Checker - Development Commands"
	@echo "  make setup        Install dependencies"
	@echo "  make lint         Run linters (ruff, mypy)"
	@echo "  make test         Run unit + property tests"
	@echo "  make test-golden  Run golden + adversarial tests"
	@echo "  make test-e2e     Run Playwright e2e tests"
	@echo "  make mutation     Run mutmut mutation tests"
	@echo "  make rules-check  Validate schema, checksum, rule coverage & tier boundaries"
	@echo "  make gen-docs     Regenerate DOUBT_CODES.md"
	@echo "  make gate         Execute complete pre-merge CI gate"

setup:
	@echo "==> Setting up environment..."
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(PYTHON) -m pip install -q --upgrade pip
	@echo "==> Setup complete."

lint:
	@echo "==> Running ruff lint and format check..."
	@$(RUFF) check .
	@echo "==> Running mypy strict type check on scripts & backend..."
	@MYPYPATH=backend $(MYPY) --strict scripts/rules_check.py scripts/test_accuracy.py
	@if find backend/app -name "*.py" 2>/dev/null | grep -q .; then $(MYPY) --strict backend/app; fi

test:
	@echo "==> Running pytest test suite (unit + property)..."
	@PYTHONPATH=backend $(PYTEST) -v backend/tests/unit backend/tests/property

test-golden:
	@echo "==> Running golden & adversarial test suite..."
	@if [ -d backend/tests/golden ] && [ "$$(ls -A backend/tests/golden)" ]; then \
		PYTHONPATH=backend $(PYTEST) -v backend/tests/golden backend/tests/adversarial && $(PYTHON) scripts/test_accuracy.py; \
	else \
		echo "    [Phase 0 Stub] Golden tests will activate in Phase 2/3."; \
	fi

test-e2e:
	@echo "==> Running E2E test suite..."
	@echo "    [Phase 0 Stub] Playwright tests will activate with UI in Phase 1."

mutation:
	@echo "==> Running mutation tests on engine and doubt modules..."
	@echo "    [Phase 0 Stub] mutmut testing will run on engine in Phase 1."

rules-check:
	@echo "==> Running KTU 2024 ruleset checks..."
	@$(PYTHON) scripts/rules_check.py

gen-docs:
	@echo "==> Regenerating DOUBT_CODES.md from code enum..."
	@if [ -f backend/app/doubt/codes.py ]; then \
		$(PYTHON) scripts/gen_doubt_codes.py; \
	else \
		echo "    [Phase 0 Stub] Doubt codes documentation generator will activate in Phase 1."; \
	fi

gate: lint test test-golden rules-check
	@echo "==> Checking architectural boundaries with import-linter..."
	@if [ -f .importlinter ]; then PYTHONPATH=backend $(LINT_IMPORTS); fi
	@echo ""
	@echo "============================================================"
	@echo "                 ALL CI GATE CHECKS PASSED                  "
	@echo "============================================================"
