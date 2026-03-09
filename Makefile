.PHONY: all clean test

.DEFAULT_GOAL := help

# Cores
GREEN = \033[32m
RED = \033[31m
YELLOW = \033[33m
BLUE = \033[34m
PURPLE = \033[35m
CYAN = \033[36m
BOLD = \033[1m
RESET = \033[0m

# Banner
define BANNER
$(PURPLE)$(BOLD)
██████╗  █████╗ ███████╗ ██████╗  ██████╗ ██████╗
██╔══██╗██╔══██╗██╔════╝██╔═══██╗██╔═══██╗██╔══██╗
██████╔╝███████║█████╗  ██║   ██║██║   ██║██║  ██║
██╔══██╗██╔══██║██╔══╝  ██║   ██║██║   ██║██║  ██║
██║  ██║██║  ██║██║     ╚██████╔╝╚██████╔╝██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝  ╚═════╝ ╚═════╝
                    $(CYAN)API$(RESET)
endef
export BANNER

# Docker compose command aliases
DOCKER_PS_FORMAT = "table {{.Service}}\t{{.Image}}\t{{.State}}\t{{.Status}}\t{{.Size}}\t{{.Ports}}"
DOCKER_PS_AWK = 'BEGIN{OFS="\t"} { \
    gsub(/0\.0\.0\.0:/, ""); \
    gsub(/->/, " → "); \
    gsub(/\/tcp.*/, ""); \
    gsub(/running/, "\033[32mrunning\033[0m"); \
    gsub(/exited/, "\033[31mexited\033[0m"); \
    gsub(/paused/, "\033[33mpaused\033[0m"); \
    gsub(/^api/, "\033[35mapi\033[0m"); \
    gsub(/rafood-api:latest/, "\033[35mrafood-api:latest\033[0m"); \
    gsub(/8000/, "\033[35m8000\033[0m"); \
    print \
}'

help: ## Show this help message
	@echo "$$BANNER"
	@echo "\nShowing all available make targets... 🤔\n"
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

banner: ## Show the banner
	@echo "$$BANNER"

start: ## Start the Docker containers (also run the API)
	@echo "$$BANNER"
	@echo "Starting containers... 🚀\n"
	@docker compose up -d
	@echo "\nContainers started! 🎉\n"
	@docker compose ps --format $(DOCKER_PS_FORMAT) | awk $(DOCKER_PS_AWK)

build: ## Build the Docker images. Tip: use 'make build' after changing dependencies in pyproject.toml
	@echo "Building Docker images... 🏗️"
	@docker compose down && docker compose build
	@echo "\nDocker images built! 🎉\n"
	@make start && make list-containers

stop: ## Stop the Docker containers
	@echo "Stopping containers... 🛑\n"
	@docker compose stop

down: ## Remove the Docker containers
	@echo "Removing containers... 🗑️\n"
	@docker compose down

restart: ## Restart the Docker containers
	@echo "Restarting containers... 🔄\n"
	@docker compose stop
	@docker compose up -d
	@echo "\nContainers restarted! 🎉\n"
	@docker compose ps --format $(DOCKER_PS_FORMAT) | awk $(DOCKER_PS_AWK)

start-monitoring: ## Start the monitoring Docker containers
	@echo "$$BANNER"
	@echo "Starting monitoring containers... 🚀\n"
	@docker compose --profile monitoring up -d
	@echo "\nMonitoring containers started! 🎉\n"
	@docker compose ps --format $(DOCKER_PS_FORMAT) | awk $(DOCKER_PS_AWK)

down-monitoring: ## Remove the monitoring Docker containers
	@echo "Removing monitoring containers... 🗑️\n"
	@docker compose --profile monitoring down

restart-monitoring: ## Restart the monitoring Docker containers (from down state)
	@echo "Stopping and restarting monitoring Docker containers (full down/up cycle) ... 🔄\n"
	@docker compose --profile monitoring down
	@docker compose --profile monitoring up -d
	@echo "\nContainers restarted! 🎉\n"
	@docker compose ps --format $(DOCKER_PS_FORMAT) | awk $(DOCKER_PS_AWK)

list-containers: ## List running Docker containers
	@echo "Listing running containers... 📋\n"
	@docker compose ps --format $(DOCKER_PS_FORMAT) | awk $(DOCKER_PS_AWK)

logs: ## Show logs for a container. Usage: make logs container=<container_name> (default: api)
	@echo "Showing logs... 📜\n"
	@docker compose logs -f $(or $(container),api)

bash: ## Access bash in a container. Usage: make bash container=<container_name> (default: api)
	@echo "Accessing bash in container... 💻\n"
	@docker compose exec $(or $(container),api) bash

create-migration: ## Create a new database migration. Usage: make create-migration name='<revision message>'
	@echo "Creating new migration... 🆕"
	@echo "Usage: make create-migration name='<revision message>'"
	@if [ -z "$(name)" ]; then \
		echo "Error: Please provide a migration name using name='<revision message>'"; \
		exit 1; \
	fi
	@poetry run alembic revision -m "$(name)"

migrate: ## Apply database migrations
	@echo "Applying migrations... 🚧\n"
	@poetry run alembic upgrade head

rollback: ## Rollback the last database migration
	@echo "Rolling back last migration... ⏪\n"
	@poetry run alembic downgrade -1

pre-commit: ## Install and run pre-commit hooks
	@echo "Installing and running pre-commit hooks... 🪝\n"
	@poetry run pre-commit install && poetry run pre-commit run -a -v

lint: ## Run the linter
	@echo "Running linter... 🧹\n"
	@poetry run ruff check .

lint-fix: ## Run the linter with auto-fix
	@echo "Running linter with auto-fix... 🧽\n"
	@poetry run ruff check --fix .

format: ## Format the codebase
	@echo "Formatting code... 🎨\n"
	@poetry run ruff format .

lint-type: ## Run the type checker
	@echo "Running type checker... 🔍\n"
	@poetry run mypy src

lint-complete: ## Run the linter, type checker, formatter and pre-commit hooks
	@echo "Running linter, type checker, formatter and pre-commit hooks... 🧹🔍🎨🪝\n"
	@make lint-fix && make lint-type && make format && make pre-commit

run: ## Run the application (not recommended for use with Docker)
	@echo "⚠️ Possibly deprecated. Can't be used with API running on Docker ⚠️\n"
	@poetry run python -m src.main

test: ## Run the test suite. Usage: make test t='<test_path_or_marker>'
	@echo "Running tests... 🧪\n"
	@echo "Usage: make test or make test t='<test_path_or_marker>'"
	@PYTHONPATH=src poetry run pytest -vv --cov=src --cov-report=term-missing $(t)

clean-test: ## Clean test cache files
	@echo "Cleaning test cache files... 🧹\n"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@rm -rf .pytest_cache/ .ruff_cache/ .coverage htmlcov/

tree: ## Show project file tree
	@echo "Project file tree... 🌲\n"
	@tree src -I "__pycache__|*.pyc|.pytest_cache|.ruff_cache|.venv|venv|.mypy_cache|.git|.idea|__pypackages__|.venv|venv|node_modules"

create-adr: ## Create a new Architecture Decision Record. Usage: make create-adr name='<descriptive-name>'
	@echo "Creating new Architecture Decision Record... 🆕"
	@echo "Usage: make create-adr name='<descriptive-name>'"
	@if [ -z "$(name)" ]; then \
		echo "Error: Please provide a descriptive name using name='<descriptive-name>'"; \
		exit 1; \
	fi
	@NUM=$$(ls docs/adr/ | grep -E '^[0-9]{3}-' | grep -v '^000-' | wc -l | awk '{printf "%03d", $$1 + 1}'); \
	cp docs/adr/000-base-adr-template.md docs/adr/$$NUM-$(name).md; \
	echo "Created docs/adr/$$NUM-$(name).md"

load-test: ## Run load tests with Locust
	@echo "Running load tests with Locust... 🔥\n"
	@echo "Warning: Make sure the API is running before executing load tests! ⚠️\n"
	@poetry run locust -f locust/locustfile.py

build-container: ## Build the Docker image for Kubernetes deployment using Docker only (not for use with Docker Compose)
	@echo "Building Docker image for Kubernetes deployment using Docker... 🏗️\n"
	@docker build -t rafood-api:latest .
	@echo "\nDocker image built! 🎉\n"
	@echo "Showing Docker image... 📋\n"
	@docker images | grep rafood-api

run-container: ## Run the Docker container locally for testing (not for use with Docker Compose)
	@echo "Running Docker container locally... 🚀\n"
	@docker run --env-file .env -p 8000:8000 rafood-api:latest
	@echo "\nDocker container started! 🎉\n"

stop-container: ## Stop the Docker container locally for testing (not for use with Docker Compose)
	@echo "Stopping Docker container locally... 🛑\n"
	@docker stop rafood-api:latest
	@echo "\nDocker container stopped! 🎉\n"
