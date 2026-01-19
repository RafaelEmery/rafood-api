from faker import Faker
from tasks.categories_task_set import CategoryTasks
from tasks.offers_task_set import OfferTasks
from tasks.products_task_set import ProductTasks
from tasks.restaurants_task_set import RestaurantTasks
from tasks.users_task_set import UserTasks

from locust import HttpUser, between

faker = Faker()


class RafoodAPILoadTest(HttpUser):
	tasks = [CategoryTasks, UserTasks, RestaurantTasks, OfferTasks, ProductTasks]
	host = 'http://localhost:8000'
	wait_time = between(1, 3)
