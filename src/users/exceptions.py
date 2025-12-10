from src.exceptions import AppInternalServerError, AppNotFoundError


class UsersInternalError(AppInternalServerError):
	def __init__(self, message: str):
		super().__init__(
			message=message,
			error_code='users_internal_error',
		)


class UserNotFoundError(AppNotFoundError):
	def __init__(self, user_id: str):
		super().__init__(
			message=f'User {user_id} not found',
			error_code='user_not_found',
		)
