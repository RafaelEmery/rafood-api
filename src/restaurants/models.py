import datetime
import uuid

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Time
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

# FIXME: understand why this import is working to create users or restaurants
from products.models import Product  # noqa
from core.config import settings


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
	updated_at = Column(
		DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now
	)

	owner = relationship('User', back_populates='restaurants', lazy='joined')
	products = relationship('Product', back_populates='restaurant', lazy='joined')
	schedules = relationship('RestaurantSchedule', back_populates='restaurant', lazy='joined')


# TODO: add active boolean column
class RestaurantSchedule(settings.Base):
	__tablename__ = 'restaurant_schedules'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	restaurant_id = Column(UUIDType(binary=False), ForeignKey('restaurants.id'), nullable=False)
	day_type = Column(String(10), nullable=False)
	start_day = Column(String(10), nullable=False)
	end_day = Column(String(10), nullable=False)
	start_time = Column(Time, nullable=False)
	end_time = Column(Time, nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(
		DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now
	)

	restaurant = relationship('Restaurant', back_populates='schedules')
