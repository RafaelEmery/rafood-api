from unittest.mock import Mock, call, patch

import pytest
from structlog.types import EventDict  # noqa: TCH002

from src.core.logging.logger import StructLogger, drop_color_message_key, setup_logging


def test_drop_color_message_key_removes_color_message():
	event_dict: EventDict = {
		'giorgian': 'arrascaeta',
		'color_message': 'colored',
		'bruno': 'henrique',
	}
	result = drop_color_message_key(None, None, event_dict)

	assert 'color_message' not in result
	assert result['giorgian'] == 'arrascaeta'
	assert result['bruno'] == 'henrique'


def test_drop_color_message_key_handles_missing_key():
	event_dict: EventDict = {'filipe': 'luís'}
	result = drop_color_message_key(None, None, event_dict)

	assert result == event_dict


@patch('src.core.logging.logger.structlog')
@patch('src.core.logging.logger.logging')
def test_setup_logging_with_json_renderer(mock_logging, mock_structlog):
	mock_handler = Mock()
	mock_logging.StreamHandler.return_value = mock_handler
	mock_root_logger = Mock()
	mock_logging.getLogger.return_value = mock_root_logger

	setup_logging(json_logs=True, log_level='INFO')

	mock_structlog.configure.assert_called_once()
	mock_root_logger.setLevel.assert_called_with('INFO')


def test_struct_logger_to_snake_case():
	assert StructLogger._to_snake_case('CampeonatoCarioca') == 'campeonato_carioca'
	assert StructLogger._to_snake_case('CampeonatoBrasileiro') == 'campeonato_brasileiro'
	assert StructLogger._to_snake_case('LibertadoresDaAmerica') == 'libertadores_da_america'


@patch('src.core.logging.logger.settings')
@patch('src.core.logging.logger.structlog')
def test_struct_logger_bind_with_sqlmodel(mock_structlog, mock_settings, category, user):
	mock_settings.LOG_NAME = 'alexsandro'
	logger = StructLogger()

	logger.bind(category, user)

	calls = mock_structlog.contextvars.bind_contextvars.call_args_list
	assert call(category=category.id) in calls
	assert call(user=user.id) in calls


@patch('src.core.logging.logger.settings')
@patch('src.core.logging.logger.structlog')
def test_struct_logger_bind_with_kwargs(mock_structlog, mock_settings):
	mock_settings.LOG_NAME = 'carrascal'
	logger = StructLogger()

	logger.bind(user_id=123, action='tricampeonato_da_libertadores')

	mock_structlog.contextvars.bind_contextvars.assert_called_with(
		user_id=123, action='tricampeonato_da_libertadores'
	)


@patch('src.core.logging.logger.settings')
@patch('src.core.logging.logger.structlog')
def test_struct_logger_bind_with_invalid_argument(mock_structlog, mock_settings):
	mock_settings.LOG_NAME = 'luiz_araujo'
	mock_logger = Mock()
	mock_structlog.stdlib.get_logger.return_value = mock_logger
	logger = StructLogger()

	logger.bind('allan')

	mock_logger.error.assert_called_once()


@patch('src.core.logging.logger.settings')
@patch('src.core.logging.logger.structlog')
def test_struct_logger_bind_mixed_arguments(mock_structlog, mock_settings, category):
	mock_settings.LOG_NAME = 'samuel_lino'
	logger = StructLogger()

	logger.bind(category, custom_field='Vitão')

	calls = mock_structlog.contextvars.bind_contextvars.call_args_list
	assert call(category=category.id) in calls
	assert call(custom_field='Vitão') in calls


@patch('src.core.logging.logger.structlog')
def test_struct_logger_unbind(mock_structlog):
	StructLogger.unbind('emerson_royal', 'ayrton_lucas')

	mock_structlog.contextvars.unbind_contextvars.assert_called_once_with(
		'emerson_royal', 'ayrton_lucas'
	)


@pytest.mark.parametrize(
	'log_method, message, kwargs',
	[
		('debug', 'Debug message', {'key': 'value'}),
		('info', 'Info message', {'user_id': 123}),
		('warning', 'Warning message', {}),
		('error', 'Error message', {'error_code': 500}),
		('critical', 'Critical message', {}),
		('exception', 'Exception occurred', {}),
	],
)
@patch('src.core.logging.logger.settings')
@patch('src.core.logging.logger.structlog')
def test_struct_logger_methods(mock_structlog, mock_settings, log_method, message, kwargs):
	mock_settings.LOG_NAME = 'erick_pulgar'
	mock_logger = Mock()
	mock_structlog.stdlib.get_logger.return_value = mock_logger
	logger = StructLogger()

	# Calling logger function with desired parameters
	getattr(logger, log_method)(message, **kwargs)

	getattr(mock_logger, log_method).assert_called_once_with(message, **kwargs)
