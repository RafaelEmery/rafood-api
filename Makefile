lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

run:
	@poetry run python src/main.py
