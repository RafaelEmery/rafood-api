import datetime
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

from config import settings


class Category(settings.Base):
	__tablename__ = 'categories'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	name = Column(String(256), nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(DateTime, nullable=False, onupdate=datetime.datetime.now)

	products = relationship('Product', back_populates='category')
