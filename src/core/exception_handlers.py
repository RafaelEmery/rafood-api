import logging, traceback

from datetime import datetime, timezone

from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions import AppError, AppNotFoundError


logger = logging.getLogger(__name__)


def register_exception_handlers(app):
	@app.exception_handler(AppError)
	async def app_exception_handler(
		request: Request,
		exc: AppError,
	):
		logger.exception(f'{exc.message}')

		return JSONResponse(
			status_code=int(exc.status_code),
			content={
				'title': exc.title,
				'error': exc.error_code,
				'message': exc.message,
				'path': request.url.path,
				'params': str(request.path_params) if request.path_params else None,
				'query': str(request.query_params.items()) if request.query_params else None,
				'timestamp': datetime.now(timezone.utc).isoformat(),
			},
		)

	@app.exception_handler(AppNotFoundError)
	async def app_not_found_exception_handler(
		request: Request,
		exc: AppNotFoundError,
	):
		return JSONResponse(
			status_code=int(exc.status_code),
			content={
				'title': exc.title,
				'error': exc.error_code,
				'message': exc.message,
				'timestamp': datetime.now(timezone.utc).isoformat(),
			},
		)

	@app.exception_handler(Exception)
	async def catch_all_handler(request: Request, exc: Exception):
		logger.error(
			'UnhandledException:\n%s',
			''.join(
				traceback.format_exception(
					type(exc),
					exc,
					exc.__traceback__,
				)
			),
		)
		return JSONResponse(
			status_code=500,
			content={
				'title': 'Unexpected Error',
				'type': str(exc.__class__.__name__),
				'message': str(exc),
			},
		)
