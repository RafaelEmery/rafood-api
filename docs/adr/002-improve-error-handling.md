# Improve error handling

## Context

Currently the only exceptions on application are `HTTPException` from FastAPI with only status_code `404` or `500` with only a `detail` on payload.

There are the FastAPI/Pydantic exceptions for `400` and/or `422` but it won't be changed.

The routers/APIs have the exception handling logic:

```python
@router.patch(
	'/{id}/schedules/{schedule_id}',
	name='Update restaurant schedule',
	status_code=status.HTTP_200_OK,
	response_model=RestaurantScheduleSchema,
)
async def update_restaurant_schedule(
	id: UUID,
	schedule_id: UUID,
	body: UpdateRestaurantScheduleSchema,
	service: RestaurantScheduleServiceDeps,
):
	try:
		return await service.update(id, schedule_id, body)
	except RestaurantNotFoundError as e:
		raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e
	except RestaurantScheduleNotFoundError as e:
		raise HTTPException(status.HTTP_404_NOT_FOUND, str(e)) from e
	except Exception as e:
		raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)) from e
```

## Decision

Add custom error handling to provide better messages, context and extra information. Will be used a custom `@app.exception_handler` to get all API/Service/Repository layers.

Payload for `JSONResponse` errors will be like:

```json
{
    "title": "Not Found Error",
    "error": "category_not_found",
    "message": "Category a9a4fe0f-3c53-4830-beac-7dcdc6b057e7 not found",
    "path": "/api/v1/categories/a9a4fe0f-3c53-4830-beac-7dcdc6b057e7",
    "params": "{'category_id': 'a9a4fe0f-3c53-4830-beac-7dcdc6b057e7'}",
    "query": null,
    "timestamp": "2025-12-08T22:45:03.059612+00:00"
}
```

Basic logging will be improved as well!

- Handling all application exceptions :white_check_mark:
- Handling specific layers exceptions correctly :white_check_mark:
- Handling dependency injection exceptions :white_check_mark:
- Logging exceptions contexts in each case :white_check_mark:

## Consequences

- Better error payloads
- Better separation of layers when raising exceptions
- Generic error handling for all cases
- Better logging on exceptions

## References

- [FastAPI Docs - Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [FastAPI Error Handling Patterns](https://betterstack.com/community/guides/scaling-python/error-handling-fastapi/) - `JSONResponse` payloads ideas.
- [Exception Handling Best Practices in Python: A FastAPI Perspective](https://medium.com/delivus/exception-handling-best-practices-in-python-a-fastapi-perspective-98ede2256870)
- [Building Robust Error Handling in FastAPI – and avoiding rookie mistakes](https://dev.to/buffolander/building-robust-error-handling-in-fastapi-and-avoiding-rookie-mistakes-ifg) - Multiple `exception_handler` added and generic handler.
