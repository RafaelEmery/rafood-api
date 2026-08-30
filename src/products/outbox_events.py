from enum import Enum

from src.core.outbox.models import OutboxEvent
from src.products.models import Product
from src.products.schemas import ProductSchema

PRODUCT_AGGREGATE_TYPE = 'product'


class ProductOutboxEvent(str, Enum):
	CREATED = 'ProductCreated'
	UPDATED = 'ProductUpdated'
	DELETED = 'ProductDeleted'


def build_product_outbox_event(product: Product, event_type: ProductOutboxEvent) -> OutboxEvent:
	payload = ProductSchema.model_validate(product).model_dump(mode='json')

	return OutboxEvent(
		aggregatetype=PRODUCT_AGGREGATE_TYPE,
		aggregateid=str(product.id),
		type=event_type,
		payload=payload,
	)
