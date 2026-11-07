# Makefile for ALGEBRA-
#
# Every target runs the SAME command as .github/workflows/ci.yml, so a green
# `make check` locally means a green CI run. Run `make` or `make help` to list
# targets. Requires GNU make (on Windows, use WSL or Git Bash).

PYTHON ?= python
PIP    := $(PYTHON) -m pip

.DEFAULT_GOAL := help

.PHONY: help install lint format format-check typecheck test test-ci cov links check hooks build clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "} {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

# --- Setup -----------------------------------------------------------------

install: ## Install the package in editable mode with dev tools
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev]"

hooks: ## Install pre-commit git hooks
	$(PYTHON) -m pre_commit install

# --- Quality checks (mirror CI) -------------------------------------------

lint: ## Ruff lint
	ruff check .

format: ## Auto-format code with Ruff (and apply safe lint fixes)
	ruff check --fix .
	ruff format .

format-check: ## Check formatting without changing files (what CI runs)
	ruff format --check .

typecheck: ## Mypy strict on tools/algebra_tools
	mypy

test: ## Run tests quickly (default Hypothesis profile)
	pytest

test-ci: ## Run tests the way CI does (more Hypothesis examples)
	pytest --hypothesis-profile=ci

cov: ## Tests with coverage report (fails under the floor in pyproject.toml)
	pytest --cov --cov-report=term-missing --hypothesis-profile=ci

links: ## Check internal markdown links (skips if the script is missing)
	@if [ -f scripts/check_links.py ]; then \
		$(PYTHON) scripts/check_links.py; \
	else \
		echo "scripts/check_links.py not found yet; skipping link check."; \
	fi

check: lint format-check typecheck cov links ## Run everything CI runs

# --- Packaging and cleanup -------------------------------------------------

build: ## Build sdist and wheel into dist/
	$(PIP) install --upgrade build
	$(PYTHON) -m build

clean: ## Remove caches and build artifacts
	rm -rf build dist *.egg-info tools/*.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache .hypothesis .coverage htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
