.PHONY: all clean test

dep-start:
	@docker compose up -d

dep-stop:
	@docker compose stop

dep-down:
	@docker compose down

dep-logs:
	@docker compose logs -f database

create-migration:
	@echo "Usage: make create-migration name='<revision message>'"
	@poetry run alembic revision -m "$(name)"

migrate:
	@poetry run alembic upgrade head

rollback:
	@poetry run alembic downgrade -1

pre-commit:
	@poetry run pre-commit install && poetry run pre-commit run -a -v

lint:
	@poetry run ruff check .

lint-fix:
	@poetry run ruff check --fix .

format:
	@poetry run ruff format .

run:
	@poetry run python -m src.main

test:
	@PYTHONPATH=src poetry run pytest -vv --cov=src --cov-report=term-missing $(t)
