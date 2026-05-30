# Postman collections

| File                                 | Purpose                                                            |
| ------------------------------------ | ------------------------------------------------------------------ |
| `rafood-api.postman_collection.json` | Full manual collection for local exploration (Postman UI).         |
| `smoke.postman_collection.json`      | CI smoke tests — self-contained Newman flow against an empty DB.   |
| `ci.environment.json`                | Environment for CI/local Newman runs (`baseUrl`, geo coordinates). |

## Smoke tests (Newman)

The smoke collection runs a **33-step** flow under the `Smoke` folder:

1. Health check (`GET /ping`)
1. Create user → category → restaurant (+ weekday/weekend schedules) → product → offer (+ schedule for today)
1. Read/update endpoints across all domains (GET list/find, PUT/PATCH)
1. Near-by endpoints (`/restaurants/open`, `/offers/active`)
1. Cleanup in FK-safe order: offer schedule → offer → product → restaurant schedules → restaurant → category → user

Variables are chained via collection variables (`userId`, `weekdayScheduleId`, `offerScheduleId`, etc.) and Postman test scripts assert status codes.

**Note:** `GET /api/v1/restaurants` (list all) is not in the smoke flow; it is covered by feature tests. The smoke run still exercises restaurant reads via `GET /restaurants/{id}` and `GET /restaurants/open`.

### Local run (Docker and Docker Compose — recommended)

With the API and database up:

```bash
make list-containers # check if containers are running
make start           # if containers are not running
make migrate         # apply migrations once (or after schema changes)
```

Newman runs on the **host** and hits the published API port (`APP_PORT` from `.env`, default `8000`):

```bash
make newman-smoke-tests
```

To run using `npx` (without Docker):

```bash
npx --yes newman@6.2.1 run postman/smoke.postman_collection.json \
  -e postman/ci.environment.json \
  --folder "Smoke" \
  --timeout-request 15000
```

Ensure `baseUrl` in `ci.environment.json` matches your published port (default `http://localhost:8000`).

**Tip:** use a fresh database or accept leftover smoke data from previous runs. The flow creates unique emails/names each run, but repeated runs against the same DB accumulate rows until cleanup (steps 26–33) succeeds.

### CI

See [docs/workflows.md](../docs/workflows.md) — workflow `.github/workflows/smoke-tests.yml` (PR and push to `main`).
