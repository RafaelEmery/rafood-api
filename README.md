# RaFood API

FastAPI project to manage restaurants, products and offers :hamburger:

## About the project

It was based on [this](https://github.com/goomerdev/job-dev-backend-interview) backend challenge and a opportunity to learn and apply some concepts of FastAPI.

My inicial studies of FastAPI is at [fastapi-studies repository](https://github.com/RafaelEmery/fastapi-studies)

### Tools used :hammer:

- Python (3.10.7)
- Poetry
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- Pre-commit
- PostgreSQL
- Docker & Docker Compose

### ER Model

![er-model](./images/projects-and-pocs-restaurants-ER.jpg)

### Contexts

Based on the ER Model there are 5 folder to separate contexts:

- Restaurants and restaurant schedules
- Products
- Offers and offers schedules
- Categories
- Users

### Architecture Decision Records (ADRs)

The ADRs are at `adr/` [folder and documents the main decisions](./adr/README.md) of this project.

### Swagger

FastAPI generates an OpenAPI docs on `/docs` endpoint.

## Running the API :running:

To show all Makefile commands:

```bash
make help
```

To install Python and Pyenv:

```bash
pyenv install 3.10.7

pyenv virtualenv 3.10.7 rafood-api

pyenv activate rafood-api
```

To install the application:

```bash
poetry install --no-root
```

To run the API:

```bash
make run
```

### Start dependencies

To start and stop the Docker dependencies:

```bash
make dep-start

make dep-stop
```

### Alembic migrations

To create a new revision (migration file based on the models definitions):

```bash
make create-migration name=<revision-name>
```

To migrate or rollback

```bash
make migrate

make rollback
```

### Linter

The `pre-commit` is enable to run linter before each commit, but you can run any time. To run linter manually:

```bash
make lint
```

### Tests

To run tests with `pytest`:

```bash
make test
```

Be sure to have database container running with `make dep-start`

______________________________________________________________________

Made with :crystal_ball: for studies by RafaelEmery
