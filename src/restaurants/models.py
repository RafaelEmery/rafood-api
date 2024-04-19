import datetime
import uuid

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy_utils import UUIDType

from config import settings


class Restaurant(settings.Base):
	__tablename__ = 'restaurants'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	name = Column(String(256), nullable=False)
	image_url = Column(String(256))
	owner_id = Column(UUIDType(binary=False), nullable=False)
	street = Column(String(256), nullable=False)
	number = Column(Integer, nullable=False)
	neighborhood = Column(String(256), nullable=False)
	city = Column(String(256), nullable=False)
	state_abbr = Column(String(2), nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(DateTime, nullable=False, onupdate=datetime.datetime.now)
