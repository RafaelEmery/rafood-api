from fastapi import APIRouter

from restaurants import api as restaurants
from users import api as users
from categories import api as categories


api_router = APIRouter()


api_router.include_router(restaurants.router, prefix='/restaurants', tags=['restaurants'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(categories.router, prefix='/categories', tags=['categories'])
