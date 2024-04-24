import datetime
import uuid

from enum import Enum

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Time, Enum as SQLEnum
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

from src.config import settings


class Restaurant(settings.Base):
	__tablename__ = 'restaurants'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	name = Column(String(256), nullable=False)
	image_url = Column(String(256))
	owner_id = Column(UUIDType(binary=False), ForeignKey('users.id'), nullable=False)
	street = Column(String(256), nullable=False)
	number = Column(Integer, nullable=False)
	neighborhood = Column(String(256), nullable=False)
	city = Column(String(256), nullable=False)
	state_abbr = Column(String(2), nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(DateTime, nullable=False, onupdate=datetime.datetime.now)

	owner = relationship('User')
	products = relationship('Product')
	schedules = relationship('RestaurantSchedule')


class DayType(Enum):
	WEEKDAY = 'weekday'
	WEEKEND = 'weekend'
	HOLIDAY = 'holiday'


class RestaurantSchedule(settings.Base):
	__tablename__ = 'restaurant_schedules'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	restaurant_id = Column(UUIDType(binary=False), ForeignKey('restaurants.id'), nullable=False)
	day_type = Column(SQLEnum(DayType), nullable=False)
	start_day = Column(String(10), nullable=True)
	end_day = Column(String(10), nullable=True)
	start_time = Column(Time, nullable=False)
	end_time = Column(Time, nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(DateTime, nullable=False, onupdate=datetime.datetime.now)

	restaurant = relationship('Restaurant')
