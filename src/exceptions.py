NOT_FOUND_ERROR = 'Not Found Error'
INTERNAL_SERVER_ERROR = 'Internal Server Error'


class AppError(Exception):
	"""Base class for all exceptions in the application."""

	def __init__(self, title: str, message: str, error_code: str, status_code: int):
		self.title = title
		self.message = message
		self.error_code = error_code
		self.status_code = status_code

		super().__init__(message)


class AppNotFoundError(AppError):
	"""Base class for all not found exceptions."""

	def __init__(self, message: str, error_code: str):
		super().__init__(
			title=NOT_FOUND_ERROR, message=message, error_code=error_code, status_code=404
		)


class AppInternalServerError(AppError):
	"""Base class for all internal server error exceptions."""

	def __init__(self, message: str, error_code: str):
		super().__init__(
			title=INTERNAL_SERVER_ERROR, message=message, error_code=error_code, status_code=500
		)
