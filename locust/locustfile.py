from faker import Faker
from tasks.categories_task_set import CategoryTasks

from locust import HttpUser, between

faker = Faker()


class RafoodAPILoadTest(HttpUser):
	tasks = [CategoryTasks]
	host = 'http://localhost:8000'
	wait_time = between(1, 3)
