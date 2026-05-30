@.cursor/prompts/feature-agent.md

## Context

Add PostGIS and GiST index: Install PostGIS on PostgreSQL and install GiST.

## Logic flow

- Add PostGIS on PostgreSQL
- Install GiST
- Updates the Docker Compose, CI files, test dependencies, and others

I'll run (or approve) manually commands for installing the dependencies and build containers, as defined at project boundaries, just tell me what to run. Remember to use Alembic Migrations to uses GiST index or any other PostgreSQL dependency.

## Acceptance criteria

- PostGIS must be enabled at RaFood API project and environment
- GiST must be enabled at RaFood API project and environment
- Existing environment and tests must be running ok (as is actually)

## Extra

Do not work on the new endpoints, the main goal here is to have all these dependencies installed and project is running correctly! At other Feature Prompt i'll ask to implement the feature ;)

## References

`008-add-postgis-and-gist-index.md`
