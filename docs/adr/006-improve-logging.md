# Improve Logging

## Context

Currently, the logging setup for Rafood API has a basic configuration that does not provide sufficient detail for effective monitoring and debugging. Example:

```bash
rafood_api  | INFO:     10.100.4.1:55236 - "GET /api/v1/categories HTTP/1.1" 200 OK
rafood_api  | INFO:     10.100.4.1:49344 - "POST /api/v1/categories HTTP/1.1" 201 Created
```

In exceptions scenarios, the logs return an unstructured stack trace and a `exception_handlers.py` logger stacktrace:

```bash
rafood_api  | Handled AppError on /api/v1/categories
rafood_api  | Traceback (most recent call last):
    # Some stack trace lines here
rafood_api  | INFO:     10.100.4.1:56104 - "POST /api/v1/categories HTTP/1.1" 500 Internal Server Error
```

There's no loggers on endpoints, services on repository layers, and other critical parts of the application, making it hard to trace issues or understand application flow.

## Decision

Improve logging by implementing a more complete logging configuration, validate if can logs requests and responses. The exception logging may not be changed in this case, but we can improve it in the future.

The log message should be organized, JSON formatted, and include relevant metadata such as timestamps, log levels, request IDs, user IDs, and other contextual information.

## Consequences

- Better visibility into application behavior and issues.
- Easier debugging and monitoring.
- Potentially increased log volume, which may require log management solutions.

## References

Docs, links or any other references to this change.

- [XI. Logs](https://12factor.net/logs) - The Twelve-Factor App: Logs
- [Logging with FastAPI](https://betterstack.com/community/guides/logging/logging-with-fastapi/) - A guide on setting up logging in FastAPI applications with different configurations (dict, JSON, file, console).
- [How to log every request and response in FastAPI](https://medium.com/@joerosborne/how-to-log-every-request-and-response-in-fastapi-dcf8d2be2055) - How to log every request and response in FastAPI (saving on database).
- [Backend logging in Python and applied to FastAPI](https://medium.com/@v0220225/backend-logging-in-python-and-applied-to-fastapi-7b47118d1d92) - Defining logging best practices and logging requests and responses with a middleware.
- [Creating a middleware in FastAPI for logging request and responses](https://dev.to/rajathkumarks/creating-a-middleware-in-fastapi-for-logging-request-and-responses-379o) - Simpler middleware example for logging requests and responses in FastAPI.
- [Sharpen Your Code: Using the right tools](https://pythonbynight.com/blog/sharpen-your-code) - Rich Logging lib for Python applications.
- [FastAPI Structlog Integration](https://wazaari.dev/blog/fastapi-structlog-integration) - Guide on integrating Structlog with FastAPI for structured logging (*that's a good one*). Has `correlation_id` implementation, request and simple `log.info()`. That's the main reference for this ADR.
