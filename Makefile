dep-start:
	docker-compose up -d

dep-stop:
	docker-compose down

dep-logs:
	docker-compose logs -f database

# Usage: make create-migration message=<revision message>
create-migration:
	@poetry run alembic revision --autogenerate -m "$(message)"

lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

run:
	@poetry run python src/main.py
