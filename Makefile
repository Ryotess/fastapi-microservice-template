.PHONY: help init new-feature install sync-dev sync-prod run test lint format clean tidy host up down rebuild

help: ## Show available make targets
	@awk 'BEGIN {FS = ":.*## "}; /^[a-zA-Z0-9_.-]+:.*## / {printf "%-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

init: ## Install baseline runtime and development dependencies
	uv add fastapi uvicorn sqlalchemy pydantic-settings loguru alembic psycopg
	uv add --dev ruff pytest pytest-asyncio httpx

new-feature: ## Scaffold a new feature module with name=<feature_name>
	@if [ -z "$(name)" ]; then echo "Usage: make new-feature name=<feature_name>"; exit 1; fi
	bash scripts/new_feature.sh "$(name)"

install: ## Sync dependencies from lockfile
	uv sync --frozen --no-cache

sync-dev: ## Sync development dependencies
	uv sync --frozen --no-cache

sync-prod: ## Sync production-only dependencies
	uv sync --frozen --no-cache --no-dev

run: ## Run the FastAPI app with reload enabled
	PYTHONPATH=src uv run  uvicorn src.main:app --reload

test: ## Run the test suite
	PYTHONPATH=src uv run pytest

lint: ## Run Ruff lint checks
	uv run ruff check .

format: ## Format code with Ruff
	uv run ruff format .

clean: ## Remove caches and the virtual environment
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv

tidy: ## Remove Python and pytest caches
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

host: ## Run the FastAPI app without reload
	PYTHONPATH=src uv run  uvicorn src.main:app

up: ## Start Docker services with rebuild
	docker-compose up --build

down: ## Stop Docker services
	docker-compose down

rebuild: ## Recreate Docker services and volumes
	docker-compose down -v
	docker-compose up --build
