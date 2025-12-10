from src.exceptions import AppInternalServerError, AppNotFoundError


class OffersInternalError(AppInternalServerError):
	def __init__(self, message: str):
		super().__init__(
			message=message,
			error_code='offers_internal_error',
		)


class OfferNotFoundError(AppNotFoundError):
	def __init__(self, offer_id: str):
		super().__init__(
			message=f'Offer {offer_id} not found',
			error_code='offer_not_found',
		)


class OfferSchedulesInternalError(AppInternalServerError):
	def __init__(self, message: str):
		super().__init__(
			message=message,
			error_code='offer_schedules_internal_error',
		)


class OfferScheduleNotFoundError(AppNotFoundError):
	def __init__(self, schedule_id: str):
		super().__init__(
			message=f'Offer schedule {schedule_id} not found',
			error_code='offer_schedule_not_found',
		)
