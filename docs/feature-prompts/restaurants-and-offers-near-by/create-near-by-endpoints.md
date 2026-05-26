@.cursor/prompts/feature-agent.md

## Context

Create the "near by" feature: search for open restaurants and active offers nearby the user's location.

Follow the existing domain structure (api, service, repository, models, schemas, deps, exceptions). Create or update unit and feature tests as needed; add a migration if needed. Explain where each part lives and why.

## Logic flow

The endpoints must be:

```text
GET /api/v1/restaurants/open?latitude=12.345678&longitude=98.765432&radius=1000
GET /api/v1/offers/active?latitude=12.345678&longitude=98.765432&radius=1000
```

The logic flow must be:

1. Get the latitude and longitude from the request
1. Get the radius from the request (meters)
1. Get the open restaurants nearby the location
1. Get the active offers nearby the location
1. Return the open restaurants and active offers nearby the location (separate, on their own APIs)

Near by: restaurant location is inside the radius defined. If radius isn't provided on request, consider 10 kilometer.

GiST can be used to index the query and search the near by point faster ;)

### Dependencies

- Must be created two columns on the restaurants table: `latitude` and `longitude`
- Offers must not have latitude and longitude columns, but the restaurant's latitude and longitude must be used to find the offers nearby the location.

### Near by restaurant query rules

- Consider the restaurant schedule
- The restaurant must be open for the current day and start/end time
- The restaurant must be active (if there's any boolean field for it)
- Must be inside the radius of the request

### Near by offer rules

- Consider the offer schedule
- The offer must be active for the current day and start/end time
- The location logic must be applied to restaurant related to offer (restaurant - product - offer)

### Responses

Must return all the restaurant or offers schema (for each domain endpoint the domain schema)

## Acceptance criteria

- I want to create restaurant with lat/long
- I want to have all the near by open restaurants
- I want to have all the near by active offers
- Must be tested
- Must use PostGIS and GiST

## Extra

- Restaurant creation must be updated to have lat/long
- Of course, follow the project rules
- Think about tests according to rules
- If there's anything wrong about de ADR or any requirement, you can change!
- Use comments ONLY on PostGIS and GiST related code
- Swagger/Open API docs for this endpoints either

## References

`008-add-postgis-and-gist-index.md`
