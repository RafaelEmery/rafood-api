from src.exceptions import AppInternalServerError, AppNotFoundError


class RestaurantsInternalError(AppInternalServerError):
	def __init__(self, message: str):
		super().__init__(
			message=message,
			error_code='restaurants_internal_error',
		)


class RestaurantNotFoundError(AppNotFoundError):
	def __init__(self, restaurant_id: str):
		super().__init__(
			message=f'Restaurant {restaurant_id} not found',
			error_code='restaurant_not_found',
		)


class RestaurantSchedulesInternalError(AppInternalServerError):
	def __init__(self, message: str):
		super().__init__(
			message=message,
			error_code='restaurant_schedules_internal_error',
		)


class RestaurantScheduleNotFoundError(AppNotFoundError):
	def __init__(self, schedule_id: str):
		super().__init__(
			message=f'Restaurant schedule {schedule_id} not found',
			error_code='restaurant_schedule_not_found',
		)
