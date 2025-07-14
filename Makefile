.PHONY: help install install-dev test test-cov benchmark clean build publish lint format check

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the package
	pip install -e .

install-dev: ## Install development dependencies
	pip install -e ".[test]"

test: ## Run tests
	pytest -v

test-cov: ## Run tests with coverage
	pytest --cov=jsonport --cov-report=html --cov-report=term-missing

benchmark: ## Run performance benchmarks
	pytest --benchmark-only -v

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build package
	python -m build

publish: ## Publish to PyPI (requires twine)
	twine upload dist/*

lint: ## Run linting
	flake8 jsonport/ tests/
	mypy jsonport/

format: ## Format code with black
	black jsonport/ tests/

check: ## Run all checks (lint, format, test)
	make lint
	make format
	make test

docs: ## Build documentation
	cd docs && make html

docs-serve: ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8000 