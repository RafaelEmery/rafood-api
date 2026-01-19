import json

from faker import Faker

from locust import TaskSet, task

faker = Faker()


def log_failure(action: str, response, extra_info=None):
	print(f'[{action}] - Status: {response.status_code}')
	print(f'Response: {response.text}')
	if extra_info:
		print(f'Info: {json.dumps(extra_info, indent=2, default=str)}')


class RestaurantTasks(TaskSet):
	def create_user_for_restaurant(self):
		"""Create a user to be the restaurant owner"""
		user_data = {
			'first_name': faker.first_name(),
			'last_name': faker.last_name(),
			'email': faker.email(),
			'password': faker.password(length=12),
		}

		response = self.client.post('/api/v1/users', name='/api/v1/users [CREATE]', json=user_data)

		if response.status_code != 201:
			log_failure('Create User for Restaurant', response, user_data)
			return None

		return response.json().get('id')

	def create_restaurant(self, owner_id: str):
		restaurant_data = {
			'name': faker.company(),
			'image_url': faker.image_url(),
			'owner_id': owner_id,
			'street': faker.street_name(),
			'number': faker.random_int(min=1, max=9999),  # noqa: S311
			'neighborhood': faker.city_suffix(),
			'city': faker.city(),
			'state_abbr': faker.state_abbr(),
		}

		response = self.client.post(
			'/api/v1/restaurants', name='/api/v1/restaurants [CREATE]', json=restaurant_data
		)

		if response.status_code != 201:
			log_failure('Create Restaurant', response, restaurant_data)
			return None

		return response.json().get('id')

	def get_restaurants(self):
		response = self.client.get('/api/v1/restaurants', name='/api/v1/restaurants [LIST]')

		if response.status_code != 200:
			log_failure('Get Restaurants', response)
			return []

		restaurants = response.json()
		return [restaurant.get('id') for restaurant in restaurants if restaurant.get('id')]

	def get_restaurant_details(self, restaurant_id: str):
		response = self.client.get(
			f'/api/v1/restaurants/{restaurant_id}', name='/api/v1/restaurants/{id} [GET]'
		)

		if response.status_code != 200:
			log_failure('Get Restaurant Details', response, {'restaurant_id': restaurant_id})
			return None

		return response.json().get('id')

	def update_restaurant(self, restaurant_id: str, owner_id: str):
		update_data = {
			'name': faker.company(),
			'owner_id': owner_id,
			'street': faker.street_name(),
			'number': faker.random_int(min=1, max=9999),
			'neighborhood': faker.city_suffix(),
			'city': faker.city(),
			'state_abbr': faker.state_abbr(),
		}

		response = self.client.patch(
			f'/api/v1/restaurants/{restaurant_id}',
			json=update_data,
			name='/api/v1/restaurants/{id} [UPDATE]',
		)

		if response.status_code != 200:
			log_failure(
				'Update Restaurant', response, {'restaurant_id': restaurant_id, 'data': update_data}
			)
			return None

		return response.json().get('id')

	def create_restaurant_schedule(self, restaurant_id: str):
		days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
		day_types = ['weekday', 'weekend', 'holiday']

		schedule_data = {
			'day_type': faker.random_element(day_types),
			'start_day': faker.random_element(days),
			'end_day': faker.random_element(days),
			'start_time': f'{faker.random_int(min=8, max=12):02d}:00:00',
			'end_time': f'{faker.random_int(min=18, max=23):02d}:00:00',
		}

		response = self.client.post(
			f'/api/v1/restaurants/{restaurant_id}/schedules',
			json=schedule_data,
			name='/api/v1/restaurants/{id}/schedules [CREATE]',
		)

		if response.status_code != 201:
			log_failure('Create Restaurant Schedule', response, schedule_data)
			return None

		return response.json().get('id')

	def update_restaurant_schedule(self, restaurant_id: str, schedule_id: str):
		days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
		day_types = ['weekday', 'weekend', 'holiday']

		update_data = {
			'day_type': faker.random_element(day_types),
			'start_day': faker.random_element(days),
			'end_day': faker.random_element(days),
			'start_time': f'{faker.random_int(min=8, max=12):02d}:00:00',
			'end_time': f'{faker.random_int(min=18, max=23):02d}:00:00',
		}

		response = self.client.patch(
			f'/api/v1/restaurants/{restaurant_id}/schedules/{schedule_id}',
			json=update_data,
			name='/api/v1/restaurants/{id}/schedules/{schedule_id} [UPDATE]',
		)

		if response.status_code != 200:
			log_failure(
				'Update Restaurant Schedule',
				response,
				{'restaurant_id': restaurant_id, 'schedule_id': schedule_id, 'data': update_data},
			)
			return None

		return response.json().get('id')

	def delete_restaurant_schedule(self, restaurant_id: str, schedule_id: str):
		response = self.client.delete(
			f'/api/v1/restaurants/{restaurant_id}/schedules/{schedule_id}',
			name='/api/v1/restaurants/{id}/schedules/{schedule_id} [DELETE]',
		)

		if response.status_code != 204:
			log_failure(
				'Delete Restaurant Schedule',
				response,
				{'restaurant_id': restaurant_id, 'schedule_id': schedule_id},
			)

	def delete_restaurant(self, restaurant_id: str):
		response = self.client.delete(
			f'/api/v1/restaurants/{restaurant_id}', name='/api/v1/restaurants/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete Restaurant', response, {'restaurant_id': restaurant_id})

	@task
	def restaurant_full_lifecycle(self):
		"""Full lifecycle: create owner, create restaurant, schedules, update, delete"""
		owner_id = self.create_user_for_restaurant()
		if not owner_id:
			return

		restaurant_id = self.create_restaurant(owner_id)
		if not restaurant_id:
			return

		restaurants = self.get_restaurants()
		if not restaurants:
			return

		restaurant_id = self.get_restaurant_details(restaurant_id)
		if not restaurant_id:
			return

		schedule_id = self.create_restaurant_schedule(restaurant_id)
		if not schedule_id:
			return

		schedule_id = self.update_restaurant_schedule(restaurant_id, schedule_id)
		if not schedule_id:
			return

		self.delete_restaurant_schedule(restaurant_id, schedule_id)

		restaurant_id = self.update_restaurant(restaurant_id, owner_id)
		if not restaurant_id:
			return

		self.delete_restaurant(restaurant_id)
