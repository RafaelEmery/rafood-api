# Logging Guide

Proposed at [Improve Logging ADR](../adr/006-improve-logging.md)

## Overview

For better logging, we're using `structlog` and `asgi_correlation_id`.

### Using `structlog`

Use `structlog` to create structured logs that are easy to read and parse. The configuration is setup at `Environment variables` section below.

The `StructLogMiddleware` is defined on `main.py` to configure the logging for each request/response cycle. So any requests made to the API will be logged with structured information like method, URL, status code, and duration. The structured data are defined at `finally` block at `StructLogMiddleware`.

At `logger.py`, we define a `StructLogger` class with helper methods to create loggers with the desired configuration and the `setup_logging` function to initialize the logging system.

The key concept here is understand that the `structlog` is being used to overwrite the Uvicorn logs (API calls) and the `logger` calls on each service or repository (or any other function/class) and enrich logs message, in JSON format.

### Using `asgi_correlation_id`

Defines a `correlation_id` named as `request_id` on logs and represents a key for the current request lifecycle.

Uses the `CorrelationIdMiddleware` defined on `main.py` with the HTTP header name. **If the HTTP header is not present on request, the `asgi_correlation_id` library will auto generate the key**.

The `structlog` will bind this ID as context variable. This happends in `StructLogMiddleware`:

```python
import structlog
from asgi_correlation_id import correlation_id

structlog.contextvars.bind_contextvars(request_id=correlation_id.get())
```

### Environment variables

In `Settings` and values are defined at `.env`:

```python
LOG_LEVEL: str = 'INFO'
LOG_JSON_FORMAT: bool = True  # Use JSON format for logs (ideal for production)
LOG_NAME: str = 'rafood-api'  # Application logs name
LOG_ACCESS_NAME: str = (
	'rafood-api-access'  # Uvicorn access logs, re-emitted using structured information
)
LOG_INCLUDE_STACK: bool = True
LOGS_CORRELATION_HEADER_NAME: str = 'X-Request-ID'
```

The `LOG_JSON_FORMAT` sets application logs as JSON and `LOGS_CORRELATION_HEADER_NAME` sets the HTTP header for `correlation_id` (*if there's no header on request, will be auto generated*)

## Using loggers

### Endpoint logs

As mentioned before, the Uvicorn logs are overwritten and it's recommended to use the JSON format. Since the `StructLogMiddleware` is being used globally (defined at `main.py`) all the requests will be logged correctly.

### Logger calls

Import the `StructLogger` class and use it as your logger. Example on `CategoryService`:

```python
from src.core.logger import StructLogger

logger = StructLogger()


async def create(self, category: CreateCategorySchema) -> CreateCategoryResponseSchema:
	try:
		category_id = await self.repository.create(category)
		logger.bind(created_category_id=str(category_id))

		return CreateCategoryResponseSchema(id=category_id)
	except Exception as e:
		raise CategoriesInternalError(message=str(e)) from e
```

The `bind` functions sets the desired key/value as context variable so it'll be at every log message on this request lifecycle.

You can just use `logger.info` (`warning` or any other) to log a specific message or value either.

## Example

Uvicorn log example (formatted):

```json
{
   "http": {
      "url": "/api/v1/categories",
      "status_code": 201,
      "method": "POST",
      "version": "1.1",
      "host": "localhost:8000"
   },
   "network": {
      "client": {
         "ip": "10.100.4.1",
         "port": 56418
      }
   },
   "details": {
      "function": "create_category",
      "name": "Create category",
      "path_params": null
   },
   "request_id": "65b6ae74-7e5a-424f-9d03-8430da3bcb2a",
   "user_agent": "PostmanRuntime/7.49.1",
   "duration": 6794130,
   "event": "Called - POST /api/v1/categories | HTTP/1.1 | 201",
   "created_category_id": "0f56b03c-1fa8-4c57-a59c-6b8caa1bcaac",
   "logger": "rafood-api-access",
   "level": "info",
   "timestamp": "2026-01-26T11:55:48.004412Z"
}
```

This logger is called `rafood-api-access` (defined at `LOG_ACCESS_NAME` environment variable) and contains structured information about the request, response, duration, user agent, request ID, and any additional context variables (like `created_category_id`).

Example of log message:

```python
from src.core.logger import StructLogger

logger = StructLogger()


async def create(self, category: CreateCategorySchema) -> CreateCategoryResponseSchema:
	try:
		category_id = await self.repository.create(category)
		logger.bind(created_category_id=str(category_id))
		logger.info('Category created successfully.')  # <-- log message here

		return CreateCategoryResponseSchema(id=category_id)
	except Exception as e:
		raise CategoriesInternalError(message=str(e)) from e
```

```json
{
   "event": "Category created successfully.",
   "created_category_id": "0f56b03c-1fa8-4c57-a59c-6b8caa1bcaac",
   "request_id": "65b6ae74-7e5a-424f-9d03-8430da3bcb2a",
   "logger": "rafood-api",
   "level": "info",
   "timestamp": "2026-01-26T11:55:48.004512Z"
}
```
