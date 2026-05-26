from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.products.schemas import ProductSchema


class OfferWithProductSchema(BaseModel):
	"""
	Schema for an offer with its product

	Created on a different file to avoid circular imports.
	FIXME: solve circular imports on Offer and Product schemas.
	"""

	id: UUID
	product: ProductSchema
	price: float
	active: bool
	created_at: datetime
	updated_at: datetime

	class Config:
		from_attributes = True
