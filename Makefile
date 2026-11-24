APP := demo-reviews-api
IMAGE ?= $(APP):0.1.0
VENV ?= .venv
PY := $(VENV)/bin

.PHONY: install lint format format-write test test-integration coverage build run docker-build docker-scan k8s-validate clean

install: ## Create venv and install dev+runtime deps
	python3 -m venv $(VENV)
	$(PY)/pip install -r requirements-dev.txt

lint: ## ruff + bandit + mypy
	$(PY)/ruff check app tests
	$(PY)/bandit -q -r app
	$(PY)/mypy app

format: ## Check ruff format
	$(PY)/ruff format --check app tests

format-write:
	$(PY)/ruff format app tests

test: ## pytest suite (unit + API tests)
	$(PY)/pytest -q

test-integration: test

coverage:
	$(PY)/pytest --cov=app --cov-report=term-missing --cov-report=xml:coverage.xml

build: ## Byte-compile sources
	$(PY)/python -m compileall -q app

run:
	$(PY)/uvicorn app.main:app --host 0.0.0.0 --port 8000

docker-build:
	docker build -t $(IMAGE) .

docker-scan:
	trivy image $(IMAGE)

k8s-validate:
	kubectl kustomize deploy/kubernetes | kubectl apply --dry-run=client -f -

clean:
	rm -rf $(VENV) .pytest_cache .ruff_cache .mypy_cache htmlcov coverage.xml test-results
