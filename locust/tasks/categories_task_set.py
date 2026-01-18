import json

from faker import Faker

from locust import TaskSet, task

faker = Faker()


def log_failure(action: str, response, extra_info=None):
	print(f'[{action}] - Status: {response.status_code}')
	print(f'Response: {response.text}')
	if extra_info:
		print(f'Info: {json.dumps(extra_info, indent=2, default=str)}')


class CategoryTasks(TaskSet):
	def create_category(self):
		category_data = {
			'name': faker.word().capitalize(),
			'description': faker.sentence(),
		}

		response = self.client.post(
			'/api/v1/categories', json=category_data, name='/api/v1/categories [CREATE]'
		)

		if response.status_code != 201:
			log_failure('Create Category', response, category_data)
			return None

		return response.json().get('id')

	def get_categories(self):
		response = self.client.get('/api/v1/categories', name='/api/v1/categories [LIST]')

		if response.status_code != 200:
			log_failure('Get Categories', response)
			return []

		categories = response.json()
		return [cat.get('id') for cat in categories if cat.get('id')]

	def delete_category(self, category_id: str):
		response = self.client.delete(
			f'/api/v1/categories/{category_id}', name='/api/v1/categories/{id} [DELETE]'
		)

		if response.status_code != 204:
			log_failure('Delete Category', response, {'category_id': category_id})

	@task
	def category_lifecycle(self):
		"""Full lifecycle: create, list, delete"""
		category_id = self.create_category()
		if not category_id:
			return

		categories = self.get_categories()
		if not categories:
			return

		self.delete_category(category_id)
