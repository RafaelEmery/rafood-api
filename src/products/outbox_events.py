from typing import Any

from src.core.outbox.events import build_outbox_event
from src.core.outbox.models import OutboxEvent
from src.products.models import Product

PRODUCT_AGGREGATE_TYPE = 'product'
PRODUCT_CREATED = 'ProductCreated'
PRODUCT_UPDATED = 'ProductUpdated'
PRODUCT_DELETED = 'ProductDeleted'


def _product_payload(product: Product) -> dict[str, Any]:
	return {
		'id': str(product.id),
		'restaurant_id': str(product.restaurant_id),
		'name': product.name,
		'price': product.price,
		'category_id': str(product.category_id),
		'image_url': product.image_url,
		'created_at': product.created_at.isoformat() if product.created_at else None,
		'updated_at': product.updated_at.isoformat() if product.updated_at else None,
	}


def build_product_created_event(product: Product) -> OutboxEvent:
	return build_outbox_event(
		PRODUCT_AGGREGATE_TYPE,
		str(product.id),
		PRODUCT_CREATED,
		_product_payload(product),
	)


def build_product_updated_event(product: Product) -> OutboxEvent:
	return build_outbox_event(
		PRODUCT_AGGREGATE_TYPE,
		str(product.id),
		PRODUCT_UPDATED,
		_product_payload(product),
	)


def build_product_deleted_event(product: Product) -> OutboxEvent:
	return build_outbox_event(
		PRODUCT_AGGREGATE_TYPE,
		str(product.id),
		PRODUCT_DELETED,
		_product_payload(product),
	)
