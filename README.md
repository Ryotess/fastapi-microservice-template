# fastapi-microservice-template

A production-oriented, AI-coding-friendly FastAPI template for teams that want a clean microservice layout, consistent developer workflow, and minimal setup friction.

This repository is designed to be cloned, re-initialized as a new Git repository, and then adapted into a real service. It includes:

- FastAPI app bootstrap with lifespan hooks
- Async SQLAlchemy and psycopg setup
- Loguru logging
- Ruff formatting and linting
- Pytest configuration
- Docker and Docker Compose
- GitHub Actions CI for format, lint, and test checks
- Feature scaffolding with `make new-feature`

## Who This Is For

Use this template if you want:

- one deployable FastAPI service
- feature-oriented modules under `src/<feature>/`
- shared infrastructure kept in `src/`
- `uv` as the only dependency manager
- a predictable local setup and CI flow

## Quick Start

If you are creating a new project from this template, use this sequence:

```bash
git clone <your_template_repo_url> <your_new_project_name>
cd <your_new_project_name>
rm -rf .git
git init
uv python pin <python_version>
uv init
uv venv
make init
cp .env.example .env
```

Then:

1. Update `.env` for your local environment.
2. Rename the user-facing app metadata in `src/main.py` if needed.
3. Create your first feature with `make new-feature name=<feature_name>`.
4. Run checks with `make format`, `make lint`, and `make test`.
5. Add your Git remote and push the first commit.

## Daily Developer Workflow

### Start the App

```bash
make run
```

The API is served at `http://localhost:8000`.

### Create a Feature

```bash
make new-feature name=users
```

Each feature should own its API contract and business logic:

- `router.py` for endpoints
- `schemas.py` for request and response models
- `service.py` or `service/` for business logic
- optional `models.py`, `dependencies.py`, `config.py`, `exceptions.py`, and `utils.py`

### Run Quality Checks

```bash
make format
make lint
make test
```

### Run with Docker

```bash
make up
make down
```

## Project Structure

```text
fastapi-microservice-template/
├── .github/workflows/ci.yml  # GitHub Actions CI
├── .env.example              # Local environment template
├── Dockerfile
├── Makefile
├── alembic.ini
├── docker-compose.yml
├── pytest.ini
├── scripts/
│   ├── bootstrap.sh
│   └── new_feature.sh
├── src/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── models.py
│   ├── pagination.py
│   └── <feature_name>/
│       ├── __init__.py
│       ├── router.py
│       ├── schemas.py
│       ├── service.py
│       └── ...
├── templates/
│   └── feature_scaffold/
└── tests/
    └── test_main.py
```

## Architecture Rules

### Global Layer

Keep shared application concerns in `src/`:

- `main.py`: app creation, middleware, lifespan, router registration
- `config.py`: global settings
- `database.py`: engine and sessionmaker lifecycle
- `models.py`: shared model primitives
- `logging_config.py`: Loguru configuration

### Feature Layer

Keep feature-owned concerns in `src/<feature>/`:

- routers
- schemas
- business logic
- feature-specific models
- feature-specific config and dependencies

Rule of thumb:

- if multiple features need it, place it in `src/`
- if one feature owns it, place it in `src/<feature>/`

## Environment and Configuration

- Local development uses a single root `.env` file.
- Global settings use the `GLOBAL_` prefix.
- Feature settings should use feature-specific prefixes such as `USERS_` or `PAYMENTS_`.
- `GLOBAL_DATABASE_URL` is required for database-backed features.
- Non-database routes can still run without `GLOBAL_DATABASE_URL`.

Create your local environment file with:

```bash
cp .env.example .env
```

## Dependency Management

This repository uses `uv` only.

- Initialize baseline dependencies: `make init`
- Install from lockfile: `make install`
- Add a runtime dependency: `uv add <package>`
- Add a dev dependency: `uv add --dev <package>`
- Remove a dependency: `uv remove <package>`
- Sync development dependencies: `uv sync --frozen --no-cache`
- Sync production dependencies: `uv sync --frozen --no-cache --no-dev`

Do not use:

- `pip install`
- `requirements.txt`
- Poetry
- Pipenv
- Conda

## Database and Migrations

Alembic is the migration tool for this project.

Typical workflow:

```bash
uv run alembic revision --autogenerate -m "add users table"
uv run alembic upgrade head
```

If the `alembic/` directory does not exist yet:

```bash
uv run alembic init alembic
```

Keep model changes and migration files in the same change set.

## CI

GitHub Actions runs:

- formatting check
- lint
- tests

The workflow file is:

- `.github/workflows/ci.yml`

The local commands and CI commands are intentionally aligned.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

## First Customization Checklist

After cloning this template, update these areas before building real features:

1. Set the repository name and remote.
2. Update `.env` values.
3. Rename app metadata in `src/main.py` if your service should not expose the template name.
4. Create your first feature module.
5. Add project-specific models, routers, and tests.

## Author

Author: Jess Chen  
Contact: jess880831@gmail.com
