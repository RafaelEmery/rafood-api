from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.api import api_router
from src.core.config import settings
from src.core.exception_handlers import register_exception_handlers
from src.core.logger import setup_logging
from src.core.middlewares.struct_log import StructLogMiddleware

app = FastAPI(
	title=settings.APP_NAME,
	description=settings.APP_DESCRIPTION,
	version=settings.APP_VERSION,
)

Instrumentator(
	should_group_status_codes=True,
	should_ignore_untemplated=True,
	excluded_handlers=['/metrics', '/ping'],
).instrument(app).expose(
	app,
	endpoint='/metrics',
	include_in_schema=False,
)

setup_logging(json_logs=settings.LOG_JSON_FORMAT, log_level=settings.LOG_LEVEL)
register_exception_handlers(app)

app.include_router(api_router, prefix=settings.APP_V1_PREFIX)

app.add_middleware(CorrelationIdMiddleware, header_name=settings.LOGS_CORRELATION_HEADER_NAME)
app.add_middleware(StructLogMiddleware)


@app.get(
	'/ping',
	tags=['Standard'],
	status_code=200,
	name='Health Check Endpoint',
	description='Check if the API is running.',
)
async def ok():
	return {'message': 'pong'}


if __name__ == '__main__':
	# Main entry point for running the FastAPI application using Uvicorn.
	# Possibly deprecated in favor of using Docker and `make start` command.
	import uvicorn

	uvicorn.run(
		'src.main:app',
		host=settings.APP_HOST,
		port=settings.APP_PORT,
		reload=True,
		log_level='info',
	)
