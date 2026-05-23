# Add PostGIS and GiST Index for Restaurant/Offer Search

## Context

Currently, there's no index on search at restaurant or offer for values like schedule start and end time.

In case of a large number of restaurants or offers, the search will be slow.

We'll create two new endpoints to search for open restaurants and active offers considering now date and time, current day of the week and current city or product:

```
GET /api/v1/restaurants/open?city="some_city"
GET /api/v1/offers/active?product_id="some_product_id"
```

This endpoints would be the first search for any app of RaFood.

## Decision

We'll add a GiST index on the schedule start and end time columns to speed up the search.

The GiST index would be created on the schedule start and end time columns. GiST index is commonly used for range queries and spatial data including date and time ranges.

## Consequences

It becomes easier to search for open restaurants and active offers considering now date and time, current day of the week and current city or product.

## References

> Docs, links or any other references to this change.
