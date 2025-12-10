from src.exceptions import AppInternalServerError, AppNotFoundError


class CategoriesInternalError(AppInternalServerError):
	def __init__(self, message: str):
		super().__init__(
			message=message,
			error_code='categories_internal_error',
		)


class CategoryNotFoundError(AppNotFoundError):
	def __init__(self, category_id: str):
		super().__init__(
			message=f'Category {category_id} not found',
			error_code='category_not_found',
		)
