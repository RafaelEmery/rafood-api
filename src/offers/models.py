import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, Double, ForeignKey, String, Time
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from core.config import settings


# TODO: add is active column
class Offer(settings.Base):
	__tablename__ = 'offers'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	product_id = Column(UUIDType(binary=False), ForeignKey('products.id'), nullable=False)
	price = Column(Double, nullable=False)
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(
		DateTime,
		nullable=False,
		default=datetime.datetime.now,
		onupdate=datetime.datetime.now,
	)

	product = relationship('Product', back_populates='offers')
	schedules = relationship('OfferSchedule', back_populates='offer', lazy='joined')


class OfferSchedule(settings.Base):
	__tablename__ = 'offer_schedules'

	id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
	offer_id = Column(UUIDType(binary=False), ForeignKey('offers.id'), nullable=False)
	day = Column(String(10), nullable=False)
	start_time = Column(Time, nullable=False)
	end_time = Column(Time, nullable=False)
	repeats = Column(Boolean, default=False)
	created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
	updated_at = Column(
		DateTime,
		nullable=False,
		default=datetime.datetime.now,
		onupdate=datetime.datetime.now,
	)

	offer = relationship('Offer', back_populates='schedules')
