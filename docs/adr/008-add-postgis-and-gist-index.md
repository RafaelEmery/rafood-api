# Add PostGIS and GiST Index for Restaurant/Offer Search

## Context

We\`ll build a new endpoint to search for open restaurants and active offers considering now date and time, current day of the week the location of the user and the restaurant:

```
GET /api/v1/restaurants/open?latitude=12.345678&longitude=98.765432&radius=1000
GET /api/v1/offers/active?latitude=12.345678&longitude=98.765432&radius=1000
```

This endpoint would be the first search for any app of RaFood. The `radius` is the radius in meters to search for open restaurants and active offers around the user's location.

## Decision

We'll add PostGIS to the project and create a GiST index on the latitude and longitude columns of the restaurants table, the "near by" offers search would use the offer's restaurant's latitude and longitude to find the offers around the user's location.

For that, we'll need to add:

- The `latitude` and `longitude` columns to the restaurants table and models.
- Use PostgreSQL's PostGIS extension to create the GiST index on the latitude and longitude columns.
- Add a new endpoint to search for open restaurants nearby the user's location.
- Add a new endpoint to search for active offers nearby the user's location.

PostgreSQL's PostGIS extension is a geospatial extension for PostgreSQL that allows you to store and query spatial data, and GiST is a Generalized Search Tree index access method commonly used to accelerate spatial queries and predicates.

The idea here is to use functions like `geography(Point)`, `ST_Distance` and `ST_DWithin` together with a GiST index on location data.

## Consequences

It becomes easier to search for open restaurants and active offers considering now date and time, current day of the week and the location of the user.

On the other hand, it becomes more complex to search for open restaurants and active offers considering now date and time, current day of the week and the location of the user.

## References

This ADR and feature is being implemented as a PoC of `explain-agent.md` and `feature-agent.md` defined at [AGENTS.md](../../AGENTS.md), [.cursor/prompts](../../.cursor/prompts) and [cursor-as-my-intern.md](../cursor-as-my-intern.md).

So, there references are based on AI generated content by Cursor.
