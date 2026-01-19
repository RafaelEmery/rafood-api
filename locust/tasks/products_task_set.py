from faker import Faker
from tasks.utils import log_failure

from locust import TaskSet, task

faker = Faker()


class ProductTasks(TaskSet):
	def create_user_for_product(self):
		"""Create a user to be the restaurant owner"""
		user_data = {
			'first_name': faker.first_name(),
			'last_name': faker.last_name(),
			'email': faker.email(),
			'password': faker.password(length=12),
		}

		response = self.client.post('/api/v1/users', name='/api/v1/users [CREATE]', json=user_data)

		if response.status_code != 201:
			log_failure('Create User for Product', response, user_data)
			return None

		return response.json().get('id')

	def create_category_for_product(self):
		"""Create a category for the product"""
		category_data = {
			'name': faker.word().capitalize(),
			'description': faker.sentence(),
		}

		response = self.client.post(
			'/api/v1/categories', name='/api/v1/categories [CREATE]', json=category_data
		)

		if response.status_code != 201:
			log_failure('Create Category for Product', response, category_data)
			return None

		return response.json().get('id')

	def create_restaurant_for_product(self, owner_id: str):
		"""Create a restaurant for the product"""
		restaurant_data = {
			'name': faker.company(),
			'image_url': faker.image_url(),
			'owner_id': owner_id,
			'street': faker.street_name(),
			'number': faker.random_int(min=1, max=9999),
			'neighborhood': faker.city_suffix(),
			'city': faker.city(),
			'state_abbr': faker.state_abbr(),
		}

		response = self.client.post(
			'/api/v1/restaurants', name='/api/v1/restaurants [CREATE]', json=restaurant_data
		)

		if response.status_code != 201:
			log_failure('Create Restaurant for Product', response, restaurant_data)
			return None

		return response.json().get('id')

	def create_product(self, restaurant_id: str, category_id: str):
		product_data = {
			'restaurant_id': restaurant_id,
			'name': faker.word().capitalize(),
			'price': faker.pyfloat(min_value=10.0, max_value=100.0, right_digits=2),
			'category_id': category_id,
			'image_url': faker.image_url(),
		}

		response = self.client.post(
			'/api/v1/products', json=product_data, name='/api/v1/products [CREATE]'
		)

		if response.status_code != 201:
			log_failure('Create Product', response, product_data)
			return None

		return response.json().get('id')

	def get_products(self):
		response = self.client.get('/api/v1/products', name='/api/v1/products [LIST]')

		if response.status_code != 200:
			log_failure('Get Products', response)
			return []

		products = response.json()
		return [product.get('id') for product in products if product.get('id')]

	def get_product_details(self, product_id: str):
		response = self.client.get(
			f'/api/v1/products/{product_id}', name='/api/v1/products/{id} [GET]'
		)

		if response.status_code != 200:
			log_failure('Get Product Details', response, {'product_id': product_id})
			return None

		return response.json().get('id')

	def update_product(self, product_id: str, restaurant_id: str, category_id: str):
		update_data = {
			'restaurant_id': restaurant_id,
			'name': faker.word().capitalize(),
			'price': faker.pyfloat(min_value=10.0, max_value=100.0, right_digits=2),
			'category_id': category_id,
			'image_url': faker.image_url(),
		}

		response = self.client.patch(
			f'/api/v1/products/{product_id}',
			json=update_data,
			name='/api/v1/products/{id} [UPDATE]',
		)

		if response.status_code != 200:
			log_failure('Update Product', response, {'product_id': product_id, 'data': update_data})
			return None

		return response.json().get('id')

	def delete_product(self, product_id: str):
		response = self.client.delete(
			f'/api/v1/products/{product_id}', name='/api/v1/products/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete Product', response, {'product_id': product_id})

	def delete_restaurant(self, restaurant_id: str):
		response = self.client.delete(f'/api/v1/restaurants/{restaurant_id}')

		if response.status_code != 204:
			log_failure('Delete Restaurant', response, {'restaurant_id': restaurant_id})

	def delete_category(self, category_id: str):
		response = self.client.delete(
			f'/api/v1/categories/{category_id}', name='/api/v1/categories/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete Category', response, {'category_id': category_id})

	@task
	def product_full_lifecycle(self):
		"""Full lifecycle: create all dependencies, product, update, delete everything"""
		owner_id = self.create_user_for_product()
		if not owner_id:
			return

		category_id = self.create_category_for_product()
		if not category_id:
			return

		restaurant_id = self.create_restaurant_for_product(owner_id)
		if not restaurant_id:
			return

		product_id = self.create_product(restaurant_id, category_id)
		if not product_id:
			return

		products = self.get_products()
		if not products:
			return

		product_id = self.get_product_details(product_id)
		if not product_id:
			return

		product_id = self.update_product(product_id, restaurant_id, category_id)
		if not product_id:
			return

		self.delete_product(product_id)
		self.delete_restaurant(restaurant_id)
		self.delete_category(category_id)
