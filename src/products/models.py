import datetime
import uuid

from sqlalchemy import Column, String, ForeignKey, Double, DateTime
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

from core.config import settings


class Product(settings.Base):
	__tablename__ = 'products'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	restaurant_id = Column(UUIDType(binary=False), ForeignKey('restaurants.id'), nullable=False)
	name = Column(String(256), nullable=False)
	price = Column(Double, nullable=False)
	category_id = Column(UUIDType(binary=False), ForeignKey('categories.id'), nullable=False)
	image_url = Column(String(256))
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(
		DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now
	)

	restaurant = relationship('Restaurant', back_populates='products')
	category = relationship('Category', back_populates='products', lazy='joined')
	offers = relationship('Offer', back_populates='offers', lazy='joined')
