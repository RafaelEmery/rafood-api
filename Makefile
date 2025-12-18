.PHONY: all clean test

help: ## Show this help message
	@echo 'Showing all available make targets... 🤔'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

start: ## Start the Docker containers (also run the API)
	@echo "Starting containers... 🚀"
	@docker compose up -d

build: ## Build the Docker images
	@echo "Building Docker images... 🏗️"
	@echo "Tip: use 'make build' after changing dependencies in pyproject.toml 😎"
	@docker compose down
	@docker compose build

stop: ## Stop the Docker containers
	@echo "Stopping containers... 🛑"
	@docker compose stop

down: ## Remove the Docker containers
	@echo "Removing containers... 🗑️"
	@docker compose down

restart: ## Restart the Docker containers
	@echo "Restarting containers... 🔄"
	@docker compose stop
	@docker compose up -d

logs: ## Show logs for all services
	@echo "Showing API logs... 📜"
	@docker compose logs -f api

database-logs: ## Show logs for the database service
	@echo "Showing database logs... 📜"
	@docker compose logs -f database

create-migration: ## Create a new database migration. Usage: make create-migration name='<revision message>'
	@echo "Usage: make create-migration name='<revision message>'"
	@if [ -z "$(name)" ]; then \
		echo "Error: Please provide a migration name using name='<revision message>'"; \
		exit 1; \
	fi
	@poetry run alembic revision -m "$(name)"

migrate: ## Apply database migrations
	@echo "Applying migrations... 🚧"
	@poetry run alembic upgrade head

rollback: ## Rollback the last database migration
	@echo "Rolling back last migration... ⏪"
	@poetry run alembic downgrade -1

pre-commit: ## Install and run pre-commit hooks
	@echo "Installing and running pre-commit hooks... 🪝"
	@poetry run pre-commit install && poetry run pre-commit run -a -v

lint: ## Run the linter
	@echo "Running linter... 🧹"
	@poetry run ruff check .

lint-fix: ## Run the linter with auto-fix
	@echo "Running linter with auto-fix... 🧽"
	@poetry run ruff check --fix .

format: ## Format the codebase
	@echo "Formatting code... 🎨"
	@poetry run ruff format .

run: ## Run the application (not recommended for use with Docker)
	@echo "⚠️ Possibly deprecated. Can't be used with API running on Docker ⚠️"
	@poetry run python -m src.main

test: ## Run the test suite. Usage: make test t='<test_path_or_marker>'
	@echo "Running tests... 🧪"
	@echo "Usage: make test or make test t='<test_path_or_marker>'"
	@PYTHONPATH=src poetry run pytest -vv --cov=src --cov-report=term-missing $(t)

clean-test: ## Clean test cache files
	@echo "Cleaning test cache files... 🧹"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache/ .ruff_cache/ .coverage htmlcov/
