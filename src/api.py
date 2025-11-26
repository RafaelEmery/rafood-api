from fastapi import APIRouter

from src.categories import api as categories
from src.offers import api as offers
from src.products import api as products
from src.restaurants import api as restaurants
from src.users import api as users

api_router = APIRouter()


api_router.include_router(restaurants.router, prefix='/restaurants', tags=['restaurants'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(categories.router, prefix='/categories', tags=['categories'])
api_router.include_router(products.router, prefix='/products', tags=['products'])
api_router.include_router(offers.router, prefix='/offers', tags=['offers'])
