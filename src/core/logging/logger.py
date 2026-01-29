# Based on https://wazaari.dev/blog/fastapi-structlog-integration#configure-the-logger
import logging
import re
from typing import Any

import structlog
from sqlmodel import SQLModel
from structlog.types import EventDict, Processor

from src.core.config import settings


def drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
	"""
	Uvicorn logs the message a second time in the extra `color_message`, but we don't
	need it. This processor drops the key from the event dict if it exists.
	"""
	event_dict.pop('color_message', None)
	return event_dict


def setup_logging(json_logs: bool = False, log_level: str = 'INFO'):
	"""
	Configure structlog with shared processors and formatters for Rafood API.
	Uses JSON renderer for production (json_logs=True) or console renderer for development.
	Reconfigures root logger to emit logs through structlog and handles uvicorn log propagation.
	"""
	timestamper = structlog.processors.TimeStamper(fmt='iso')

	shared_processors: list[Processor] = [
		structlog.contextvars.merge_contextvars,
		structlog.stdlib.add_logger_name,
		structlog.stdlib.add_log_level,
		structlog.stdlib.PositionalArgumentsFormatter(),
		structlog.stdlib.ExtraAdder(),
		drop_color_message_key,
		timestamper,
		structlog.processors.StackInfoRenderer(),
	]

	if json_logs:
		# Format the exception only for JSON logs, as we want to pretty-print them when
		# using the ConsoleRenderer
		shared_processors.append(structlog.processors.format_exc_info)

	structlog.configure(
		processors=shared_processors
		+ [
			structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
		],
		logger_factory=structlog.stdlib.LoggerFactory(),
		cache_logger_on_first_use=True,
	)

	log_renderer: structlog.types.Processor
	if json_logs:
		# JSONRenderer is used at production for better parsing by log management systems
		log_renderer = structlog.processors.JSONRenderer()
	else:
		# ConsoleRenderer is used during development for better readability
		log_renderer = structlog.dev.ConsoleRenderer()

	formatter = structlog.stdlib.ProcessorFormatter(
		# These run ONLY on `logging` entries that do NOT originate within
		# structlog.
		foreign_pre_chain=shared_processors,
		# These run on ALL entries after the pre_chain is done.
		processors=[
			# Remove _record & _from_structlog.
			structlog.stdlib.ProcessorFormatter.remove_processors_meta,
			log_renderer,
		],
	)

	# Reconfigure the root logger to use our structlog formatter, effectively emitting
	# the logs via structlog
	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	root_logger = logging.getLogger()
	root_logger.addHandler(handler)
	root_logger.setLevel(log_level.upper())

	for _log in ['uvicorn', 'uvicorn.error']:
		# Make sure the logs are handled by the root logger
		logging.getLogger(_log).handlers.clear()
		logging.getLogger(_log).propagate = True

	# Uvicorn logs are re-emitted with more context. We effectively silence them here
	logging.getLogger('uvicorn.access').handlers.clear()
	logging.getLogger('uvicorn.access').propagate = False


class StructLogger:
	"""
	A thin wrapper, which translates the easy to use bind and unbind syntax to the _contextvars
	methods and handles SQLModel instances for us. Models will be translated to snake case.
	"""

	def __init__(self, log_name=settings.LOG_NAME):
		self.logger = structlog.stdlib.get_logger(log_name)

	@staticmethod
	def _to_snake_case(name):
		return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

	def bind(self, *args, **new_values: Any):
		"""
		Binds the given arguments to the logger context.
		Any value added here will be added to all subsequent logs made with this logger.
		Args can be either unnamed SQLModel subclasses, which will bind the model name in snake_case
		to the model's ID, or named arguments, which will be bound as-is.
		"""
		for arg in args:
			if not issubclass(type(arg), SQLModel):
				self.logger.error(
					'Unsupported argument when trying to log.'
					f'Unnamed argument must be a subclass of SQLModel. Invalid argument: {type(arg).__name__}'
				)
				continue

			# If a Model is bound, we convert its class name to snake_case and bind its ID
			key = self._to_snake_case(type(arg).__name__)

			structlog.contextvars.bind_contextvars(**{key: arg.id})

		structlog.contextvars.bind_contextvars(**new_values)

	@staticmethod
	def unbind(*keys: str):
		structlog.contextvars.unbind_contextvars(*keys)

	def debug(self, event: str | None = None, *args: Any, **kw: Any):
		self.logger.debug(event, *args, **kw)

	def info(self, event: str | None = None, *args: Any, **kw: Any):
		self.logger.info(event, *args, **kw)

	def warning(self, event: str | None = None, *args: Any, **kw: Any):
		self.logger.warning(event, *args, **kw)

	warn = warning

	def error(self, event: str | None = None, *args: Any, **kw: Any):
		self.logger.error(event, *args, **kw)

	def critical(self, event: str | None = None, *args: Any, **kw: Any):
		self.logger.critical(event, *args, **kw)

	def exception(self, event: str | None = None, *args: Any, **kw: Any):
		self.logger.exception(event, *args, **kw)
