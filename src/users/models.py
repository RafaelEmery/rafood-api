import datetime
import uuid

from sqlalchemy import Column, String, DateTime
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship

from core.config import settings


class User(settings.Base):
	__tablename__ = 'users'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	first_name = Column(String(256), nullable=False)
	last_name = Column(String(256), nullable=False)
	email = Column(String(256), nullable=False)
	password = Column(String(256), nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(
		DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now
	)

	restaurants = relationship('Restaurant', back_populates='owner')
