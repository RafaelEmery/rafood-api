from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

import pytest

from src.core.logging.middleware import StructLogMiddleware


@pytest.mark.asyncio
@patch('src.core.logging.middleware.access_logger')
@patch('src.core.logging.middleware.correlation_id')
async def test_structlog_middleware_logs_access(mock_correlation_id, mock_access_logger):
	mock_correlation_id.get.return_value = str(uuid4())

	async def app(scope, receive, send):
		await send({'type': 'http.response.start', 'status': 200})

	middleware = StructLogMiddleware(app)

	scope = {
		'type': 'http',
		'client': ('127.0.0.1', 12345),
		'method': 'GET',
		'http_version': '1.1',
		'path': '/test',
		'headers': [
			(b'user-agent', b'test-agent'),
			(b'host', b'testserver'),
		],
		'endpoint': lambda: None,
		'route': Mock(name='route', spec=['name']),
		'path_params': {},
		'query_string': b'',
	}
	scope['route'].name = 'test_route'
	scope['endpoint'].__name__ = 'test_endpoint'

	async def fake_send(message):
		pass

	await middleware(scope, AsyncMock(), fake_send)

	assert mock_access_logger.info.called
	args, kwargs = mock_access_logger.info.call_args
	assert 'GET' in args[0]
	assert kwargs['http']['url'] == '/test'
