from datetime import datetime
from uuid import uuid4

from src.products.models import Product
from src.products.outbox_events import (
	PRODUCT_AGGREGATE_TYPE,
	ProductOutboxEvent,
	build_product_outbox_event,
)


def test_build_product_outbox_event_created():
	product = Product(
		id=uuid4(),
		restaurant_id=uuid4(),
		name='Pizza',
		price=20.0,
		category_id=uuid4(),
		image_url='https://example.com/pizza.jpg',
		created_at=datetime.now(),
		updated_at=datetime.now(),
	)

	event = build_product_outbox_event(product, ProductOutboxEvent.CREATED)

	assert event.aggregatetype == PRODUCT_AGGREGATE_TYPE
	assert event.aggregateid == str(product.id)
	assert event.type == ProductOutboxEvent.CREATED
	assert event.payload is not None
	assert event.payload['id'] == str(product.id)
	assert event.payload['name'] == 'Pizza'
	assert event.payload['price'] == 20.0
