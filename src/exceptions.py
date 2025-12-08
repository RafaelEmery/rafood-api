NOT_FOUND_ERROR = 'Not Found Error'
INTERNAL_SERVER_ERROR = 'Internal Server Error'


class AppError(Exception):
	"""Base class for all exceptions in the application."""

	def __init__(self, title: str, message: str, error_code: str, status_code: str):
		self.title = title
		self.message = message
		self.error_code = error_code
		self.status_code = status_code

		super().__init__(message)


class AppNotFoundError(AppError):
	"""Base class for all not found exceptions."""

	def __init__(self, message: str, error_code: str):
		super().__init__(
			title=NOT_FOUND_ERROR, message=message, error_code=error_code, status_code='404'
		)


class AppInternalServerError(AppError):
	"""Base class for all internal server error exceptions."""

	def __init__(self, message: str, error_code: str):
		super().__init__(
			title=INTERNAL_SERVER_ERROR, message=message, error_code=error_code, status_code='500'
		)


class UserNotFoundError(AppError):
	def __init__(self, user_id: str):
		super().__init__(
			message=f'User {user_id} not found', error_code='user_not_found', status_code='404'
		)


class ProductNotFoundError(AppError):
	def __init__(self, product_id: str):
		super().__init__(
			message=f'Product {product_id} not found',
			error_code='product_not_found',
			status_code='404',
		)


class OfferNotFoundError(AppError):
	def __init__(self, offer_id: str):
		super().__init__(
			message=f'Offer {offer_id} not found', error_code='offer_not_found', status_code='404'
		)


class OfferScheduleNotFoundError(AppError):
	def __init__(self, schedule_id: str):
		super().__init__(
			message=f'Offer schedule {schedule_id} not found',
			error_code='offer_schedule_not_found',
			status_code='404',
		)


class RestaurantNotFoundError(AppError):
	def __init__(self, restaurant_id: str):
		super().__init__(
			message=f'Restaurant {restaurant_id} not found',
			error_code='restaurant_not_found',
			status_code='404',
		)


class RestaurantScheduleNotFoundError(AppError):
	def __init__(self, schedule_id: str):
		super().__init__(
			message=f'Restaurant schedule {schedule_id} not found',
			error_code='restaurant_schedule_not_found',
			status_code='404',
		)
