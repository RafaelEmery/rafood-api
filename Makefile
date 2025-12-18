.PHONY: all clean test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

dep-start: ## Start dependencies (Docker)
	@docker compose up -d

dep-stop: ## Stop dependencies
	@docker compose stop

dep-down: ## Remove dependencies
	@docker compose down

dep-restart: ## Restart dependencies
	@docker compose down && docker compose up -d


dep-logs: ## Show database logs
	@docker compose logs -f database

create-migration: ## Create a new migration (name='message')
	@echo "Usage: make create-migration name='<revision message>'"
	@poetry run alembic revision -m "$(name)"

migrate: ## Run migrations
	@poetry run alembic upgrade head

rollback: ## Rollback last migration
	@poetry run alembic downgrade -1

pre-commit: ## Install and run pre-commit hooks
	@poetry run pre-commit install && poetry run pre-commit run -a -v

lint: ## Run linter
	@poetry run ruff check .

lint-fix: ## Run linter with auto-fix
	@poetry run ruff check --fix .

format: ## Format code
	@poetry run ruff format .

run: ## Run the application
	@poetry run python -m src.main

test: ## Run tests (t=path for specific test)
	@PYTHONPATH=src poetry run pytest -vv --cov=src --cov-report=term-missing $(t)

clean-test: ## Clean test cache files
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache/ .ruff_cache/ .coverage htmlcov/
