# Based on https://wazaari.dev/blog/fastapi-structlog-integration#logging-middleware
import time
from typing import TypedDict

import structlog
from asgi_correlation_id import correlation_id
from starlette.types import ASGIApp, Receive, Scope, Send
from uvicorn.protocols.utils import get_path_with_query_string

from src.core.config import settings

app_logger = structlog.stdlib.get_logger(settings.LOG_NAME)
access_logger = structlog.stdlib.get_logger(settings.LOG_ACCESS_NAME)


class AccessInfo(TypedDict, total=False):
	status_code: int
	start_time: float


class StructLogMiddleware:
	def __init__(self, app: ASGIApp):
		self.app = app

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		# If the request is not an HTTP request, we don't need to do anything special
		if scope['type'] != 'http':
			await self.app(scope, receive, send)
			return

		structlog.contextvars.clear_contextvars()
		# The correlation_id value is defined by X-Request-ID header on request
		# but the name of the header can be customized when adding the middleware
		# and currently is using the environment variable LOGS_CORRELATION_HEADER_NAME
		# If no X-Request-ID header is provided, a new UUIDv4 is generated automatically
		# by asgi-correlation-id middleware
		# This function binds the correlation_id to structlog contextvars so every log
		# made during this request will have the request_id field set
		structlog.contextvars.bind_contextvars(request_id=correlation_id.get())

		info = AccessInfo()

		# Inner send function
		async def inner_send(message):
			if message['type'] == 'http.response.start':
				info['status_code'] = message['status']
			await send(message)

		try:
			info['start_time'] = time.perf_counter_ns()

			await self.app(scope, receive, inner_send)
		except Exception:
			# Raising exception to be handled at exception_handlers.catch_all_handler.
			# Will be correctly logged and returned to caller
			raise
		finally:
			process_time = time.perf_counter_ns() - info['start_time']
			client_host, client_port = scope.get('client') or ('unknown', 0)
			http_method = scope['method']
			http_version = scope['http_version']
			url = get_path_with_query_string(scope)
			headers = {k.decode().lower(): v.decode() for k, v in scope.get('headers', [])}
			user_agent = headers.get('user-agent')
			http_host = headers.get('host')
			function_name = scope['endpoint'].__name__
			route_name = scope['route'].name
			path_params = scope['path_params'] if scope['path_params'] else None

			# Recreate the Uvicorn access log format, but add all parameters as structured information
			# Returning 420 (https://http.cat/status/420) if status_code is missing
			access_logger.info(
				f'Called - {http_method} {scope["path"]} | HTTP/{http_version} | {info.get("status_code", 420)} ',
				http={
					'url': str(url),
					'status_code': info.get('status_code', 420),
					'method': http_method,
					'version': http_version,
					'host': http_host,
				},
				network={'client': {'ip': client_host, 'port': client_port}},
				details={
					'function': function_name,
					'name': route_name,
					'path_params': path_params,
				},
				request_id=correlation_id.get(),
				user_agent=user_agent,
				duration=process_time,
			)
