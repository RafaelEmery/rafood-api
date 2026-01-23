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
		pass

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		# If the request is not an HTTP request, we don't need to do anything special
		if scope['type'] != 'http':
			await self.app(scope, receive, send)
			return

		structlog.contextvars.clear_contextvars()
		# The correlation_id value is defined by X-Request-ID header on request
		# but the name of the header can be customized when adding the middleware
		# and currently is using the environment variable LOGS_CORRELATION_HEADER_NAME
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
		except Exception as e:
			# Raising exception to be handled at exception_handlers.catch_all_handler.
			# Will be correctly logged and returned to caller
			raise e
		finally:
			process_time = time.perf_counter_ns() - info['start_time']
			client_host, client_port = scope['client']
			http_method = scope['method']
			http_version = scope['http_version']
			url = get_path_with_query_string(scope)

			# Recreate the Uvicorn access log format, but add all parameters as structured information
			access_logger.info(
				f"""{client_host}:{client_port} - "{http_method} {scope['path']} HTTP/{http_version}" {info['status_code']}""",
				http={
					'url': str(url),
					'status_code': info['status_code'],
					'method': http_method,
					'request_id': correlation_id.get(),
					'version': http_version,
				},
				network={'client': {'ip': client_host, 'port': client_port}},
				duration=process_time,
			)
