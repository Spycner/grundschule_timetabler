.PHONY: help install dev test lint format run migrate clean

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

dev: ## Run development server
	uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov=src --cov-report=term --cov-report=html

lint: ## Run linter
	uv run ruff check .

format: ## Format code
	uv run ruff format .

typecheck: ## Run type checker
	uvx --native-tls ty check

check: ## Run all checks (lint, format check, and type check)
	uv run ruff check .
	uv run ruff format --check .
	uvx --native-tls ty check

fix: ## Fix linting issues and format code
	uv run ruff check --fix .
	uv run ruff format .

migrate-init: ## Initialize alembic migrations
	uv run alembic init alembic

migrate-create: ## Create a new migration (usage: make migrate-create name="migration_name")
	uv run alembic revision --autogenerate -m "$(name)"

migrate-up: ## Apply migrations
	uv run alembic upgrade head

migrate-down: ## Rollback one migration
	uv run alembic downgrade -1

migrate-history: ## Show migration history
	uv run alembic history

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov/
	rm -rf .coverage
	rm -f timetabler.db

shell: ## Open Python shell with app context
	uv run python -i -c "from src.main import app; from src.models.database import *; from src.config import get_settings; settings = get_settings()"

db-shell: ## Open database shell
	sqlite3 timetabler.db

update: ## Update all dependencies
	uv lock --upgrade
	uv sync

update-package: ## Update specific package (usage: make update-package pkg=fastapi)
	uv lock --upgrade-package $(pkg)
	uv sync