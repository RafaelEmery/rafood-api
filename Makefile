dep-start:
	docker-compose up -d

dep-stop:
	docker-compose down

dep-logs:
	docker-compose logs -f database

# Usage: make create-migration name='<revision message>'
create-migration:
	@poetry run alembic revision -m "$(name)"

# make revision name='<revision message>'
revision:
	@poetry run alembic revision --autogenerate -m "$(name)"

migrate:
	@poetry run alembic upgrade head

rollback:
	@poetry run alembic downgrade -1

lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

run:
	@poetry run python src/main.py
