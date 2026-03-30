.PHONY: init new-feature install sync-dev sync-prod run test lint format clean tidy host up down rebuild

init:
	uv add fastapi uvicorn sqlalchemy pydantic-settings loguru alembic psycopg
	uv add --dev ruff pytest pytest-asyncio httpx

new-feature:
	@if [ -z "$(name)" ]; then echo "Usage: make new-feature name=<feature_name>"; exit 1; fi
	bash scripts/new_feature.sh "$(name)"

install:
	uv sync --frozen --no-cache

sync-dev:
	uv sync --frozen --no-cache

sync-prod:
	uv sync --frozen --no-cache --no-dev

run:
	PYTHONPATH=src uv run  uvicorn src.main:app --reload

test:
	PYTHONPATH=src uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .venv

tidy:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

host:
	PYTHONPATH=src uv run  uvicorn src.main:app

up:
	docker-compose up --build

down:
	docker-compose down

rebuild:
	docker-compose down -v
	docker-compose up --build
