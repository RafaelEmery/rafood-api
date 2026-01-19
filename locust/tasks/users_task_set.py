from faker import Faker
from tasks.utils import log_failure

from locust import TaskSet, task

faker = Faker()


class UserTasks(TaskSet):
	def create_user(self):
		user_data = {
			'first_name': faker.first_name(),
			'last_name': faker.last_name(),
			'email': faker.email(),
			'password': faker.password(length=12),
		}

		response = self.client.post('/api/v1/users', json=user_data, name='/api/v1/users [CREATE]')

		if response.status_code != 201:
			log_failure('Create User', response, user_data)
			return None

		return response.json().get('id')

	def get_users(self):
		response = self.client.get('/api/v1/users', name='/api/v1/users [LIST]')

		if response.status_code != 200:
			log_failure('Get Users', response)
			return []

		users = response.json()
		return [user.get('id') for user in users if user.get('id')]

	def get_user_details(self, user_id: str):
		response = self.client.get(f'/api/v1/users/{user_id}', name='/api/v1/users/{id} [GET]')

		if response.status_code != 200:
			log_failure('Get User Details', response, {'user_id': user_id})
			return None

		return response.json().get('id')

	def update_user(self, user_id: str):
		update_data = {
			'first_name': faker.first_name(),
			'last_name': faker.last_name(),
		}

		response = self.client.put(
			f'/api/v1/users/{user_id}', json=update_data, name='/api/v1/users/{id} [UPDATE]'
		)

		if response.status_code != 200:
			log_failure('Update User', response, {'user_id': user_id, 'data': update_data})
			return None

		return response.json().get('id')

	def delete_user(self, user_id: str):
		response = self.client.delete(
			f'/api/v1/users/{user_id}', name='/api/v1/users/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete User', response, {'user_id': user_id})

	@task
	def user_lifecycle(self):
		"""Full lifecycle: create, list, get details, update, delete"""
		user_id = self.create_user()
		if not user_id:
			return

		users = self.get_users()
		if not users:
			return

		user_id = self.get_user_details(user_id)
		if not user_id:
			return

		user_id = self.update_user(user_id)
		if not user_id:
			return

		self.delete_user(user_id)
