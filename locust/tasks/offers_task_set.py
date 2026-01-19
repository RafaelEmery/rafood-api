import json

from faker import Faker

from locust import TaskSet, task

faker = Faker()


def log_failure(action: str, response, extra_info=None):
	print(f'[{action}] - Status: {response.status_code}')
	print(f'Response: {response.text}')
	if extra_info:
		print(f'Info: {json.dumps(extra_info, indent=2, default=str)}')


class OfferTasks(TaskSet):
	def create_user_for_offer(self):
		"""Create a user to be the restaurant owner"""
		user_data = {
			'first_name': faker.first_name(),
			'last_name': faker.last_name(),
			'email': faker.email(),
			'password': faker.password(length=12),
		}

		response = self.client.post('/api/v1/users', name='/api/v1/users [CREATE]', json=user_data)

		if response.status_code != 201:
			log_failure('Create User for Offer', response, user_data)
			return None

		return response.json().get('id')

	def create_category_for_offer(self):
		"""Create a category for the product"""
		category_data = {
			'name': faker.word().capitalize(),
			'description': faker.sentence(),
		}

		response = self.client.post(
			'/api/v1/categories', name='/api/v1/categories [CREATE]', json=category_data
		)

		if response.status_code != 201:
			log_failure('Create Category for Offer', response, category_data)
			return None

		return response.json().get('id')

	def create_restaurant_for_offer(self, owner_id: str):
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
			log_failure('Create Restaurant for Offer', response, restaurant_data)
			return None

		return response.json().get('id')

	def create_product_for_offer(self, restaurant_id: str, category_id: str):
		"""Create a product for the offer"""
		product_data = {
			'restaurant_id': restaurant_id,
			'name': faker.word().capitalize(),
			'price': faker.pyfloat(min_value=10.0, max_value=100.0, right_digits=2),
			'category_id': category_id,
			'image_url': faker.image_url(),
		}

		response = self.client.post(
			'/api/v1/products', name='/api/v1/products [CREATE]', json=product_data
		)

		if response.status_code != 201:
			log_failure('Create Product for Offer', response, product_data)
			return None

		return response.json().get('id')

	def create_offer(self, product_id: str):
		offer_data = {
			'product_id': product_id,
			'price': faker.pyfloat(min_value=5.0, max_value=50.0, right_digits=2),
		}

		response = self.client.post(
			'/api/v1/offers', json=offer_data, name='/api/v1/offers [CREATE]'
		)

		if response.status_code != 201:
			log_failure('Create Offer', response, offer_data)
			return None

		return response.json().get('id')

	def get_offers(self):
		response = self.client.get('/api/v1/offers', name='/api/v1/offers [LIST]')

		if response.status_code != 200:
			log_failure('Get Offers', response)
			return []

		offers = response.json()
		return [offer.get('id') for offer in offers if offer.get('id')]

	def get_offer_details(self, offer_id: str):
		response = self.client.get(f'/api/v1/offers/{offer_id}', name='/api/v1/offers/{id} [GET]')

		if response.status_code != 200:
			log_failure('Get Offer Details', response, {'offer_id': offer_id})
			return None

		return response.json().get('id')

	def update_offer(self, offer_id: str):
		update_data = {
			'price': faker.pyfloat(min_value=5.0, max_value=50.0, right_digits=2),
			'active': faker.pybool(),
		}

		response = self.client.patch(
			f'/api/v1/offers/{offer_id}', json=update_data, name='/api/v1/offers/{id} [UPDATE]'
		)

		if response.status_code != 200:
			log_failure('Update Offer', response, {'offer_id': offer_id, 'data': update_data})
			return None

		return response.json().get('id')

	def create_offer_schedule(self, offer_id: str):
		days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

		schedule_data = {
			'day': faker.random_element(days),
			'start_time': f'{faker.random_int(min=8, max=12):02d}:00:00',
			'end_time': f'{faker.random_int(min=18, max=23):02d}:00:00',
			'repeats': faker.pybool(),
		}

		response = self.client.post(
			f'/api/v1/offers/{offer_id}/schedules',
			json=schedule_data,
			name='/api/v1/offers/{id}/schedules [CREATE]',
		)

		if response.status_code != 201:
			log_failure('Create Offer Schedule', response, schedule_data)
			return None

		return response.json().get('id')

	def update_offer_schedule(self, offer_id: str, schedule_id: str):
		days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

		update_data = {
			'day': faker.random_element(days),
			'start_time': f'{faker.random_int(min=8, max=12):02d}:00:00',
			'end_time': f'{faker.random_int(min=18, max=23):02d}:00:00',
			'repeats': faker.pybool(),
		}

		response = self.client.patch(
			f'/api/v1/offers/{offer_id}/schedules/{schedule_id}',
			json=update_data,
			name='/api/v1/offers/{id}/schedules/{schedule_id} [UPDATE]',
		)

		if response.status_code != 200:
			log_failure(
				'Update Offer Schedule',
				response,
				{'offer_id': offer_id, 'schedule_id': schedule_id, 'data': update_data},
			)
			return None

		return response.json().get('id')

	def delete_offer_schedule(self, offer_id: str, schedule_id: str):
		response = self.client.delete(
			f'/api/v1/offers/{offer_id}/schedules/{schedule_id}',
			name='/api/v1/offers/{id}/schedules/{schedule_id} [DELETE]',
		)

		if response.status_code != 204:
			log_failure(
				'Delete Offer Schedule',
				response,
				{'offer_id': offer_id, 'schedule_id': schedule_id},
			)

	def delete_offer(self, offer_id: str):
		response = self.client.delete(
			f'/api/v1/offers/{offer_id}', name='/api/v1/offers/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete Offer', response, {'offer_id': offer_id})

	def delete_product(self, product_id: str):
		response = self.client.delete(
			f'/api/v1/products/{product_id}', name='/api/v1/products/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete Product', response, {'product_id': product_id})

	def delete_restaurant(self, restaurant_id: str):
		response = self.client.delete(
			f'/api/v1/restaurants/{restaurant_id}', name='/api/v1/restaurants/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete Restaurant', response, {'restaurant_id': restaurant_id})

	def delete_category(self, category_id: str):
		response = self.client.delete(
			f'/api/v1/categories/{category_id}', name='/api/v1/categories/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete Category', response, {'category_id': category_id})

	@task
	def offer_full_lifecycle(self):
		"""Full lifecycle: create all dependencies, offer, schedules, update, delete everything"""
		owner_id = self.create_user_for_offer()
		if not owner_id:
			return

		category_id = self.create_category_for_offer()
		if not category_id:
			return

		restaurant_id = self.create_restaurant_for_offer(owner_id)
		if not restaurant_id:
			return

		product_id = self.create_product_for_offer(restaurant_id, category_id)
		if not product_id:
			return

		offer_id = self.create_offer(product_id)
		if not offer_id:
			return

		offers = self.get_offers()
		if not offers:
			return

		offer_id = self.get_offer_details(offer_id)
		if not offer_id:
			return

		schedule_id = self.create_offer_schedule(offer_id)
		if not schedule_id:
			return

		schedule_id = self.update_offer_schedule(offer_id, schedule_id)
		if not schedule_id:
			return

		self.delete_offer_schedule(offer_id, schedule_id)

		offer_id = self.update_offer(offer_id)
		if not offer_id:
			return

		self.delete_offer(offer_id)
		self.delete_product(product_id)
		self.delete_restaurant(restaurant_id)
		self.delete_category(category_id)
