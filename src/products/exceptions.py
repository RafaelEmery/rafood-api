from src.exceptions import AppInternalServerError, AppNotFoundError


class ProductsInternalError(AppInternalServerError):
	def __init__(self, message: str):
		super().__init__(
			message=message,
			error_code='products_internal_error',
		)


class ProductNotFoundError(AppNotFoundError):
	def __init__(self, product_id: str):
		super().__init__(
			message=f'Product {product_id} not found',
			error_code='product_not_found',
		)
