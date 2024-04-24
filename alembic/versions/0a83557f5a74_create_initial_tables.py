"""create inicial tables

Revision ID: 0a83557f5a74
Revises:
Create Date: 2024-04-23 22:07:15.814474

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as sa_utils


# revision identifiers, used by Alembic.
revision: str = '0a83557f5a74'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.create_table(
		'categories',
		sa.Column('id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('name', sa.String(length=256), nullable=False),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.PrimaryKeyConstraint('id'),
	)

	op.create_table(
		'users',
		sa.Column('id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('first_name', sa.String(length=256), nullable=False),
		sa.Column('last_name', sa.String(length=256), nullable=False),
		sa.Column('email', sa.String(length=256), nullable=False),
		sa.Column('password', sa.String(length=256), nullable=False),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.PrimaryKeyConstraint('id'),
	)

	op.create_table(
		'restaurants',
		sa.Column('id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('name', sa.String(length=256), nullable=False),
		sa.Column('image_url', sa.String(length=256), nullable=True),
		sa.Column('owner_id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('street', sa.String(length=256), nullable=False),
		sa.Column('number', sa.Integer(), nullable=False),
		sa.Column('neighborhood', sa.String(length=256), nullable=False),
		sa.Column('city', sa.String(length=256), nullable=False),
		sa.Column('state_abbr', sa.String(length=2), nullable=False),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.ForeignKeyConstraint(
			['owner_id'],
			['users.id'],
		),
		sa.PrimaryKeyConstraint('id'),
	)

	op.create_table(
		'products',
		sa.Column('id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('restaurant_id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('name', sa.String(length=256), nullable=False),
		sa.Column('price', sa.Double(), nullable=False),
		sa.Column('category_id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('image_url', sa.String(length=256), nullable=True),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.ForeignKeyConstraint(
			['category_id'],
			['categories.id'],
		),
		sa.ForeignKeyConstraint(
			['restaurant_id'],
			['restaurants.id'],
		),
		sa.PrimaryKeyConstraint('id'),
	)

	op.create_table(
		'restaurant_schedules',
		sa.Column('id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('restaurant_id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column(
			'day_type', sa.Enum('WEEKDAY', 'WEEKEND', 'HOLIDAY', name='daytype'), nullable=False
		),
		sa.Column('start_day', sa.String(length=10), nullable=True),
		sa.Column('end_day', sa.String(length=10), nullable=True),
		sa.Column('start_time', sa.Time(), nullable=False),
		sa.Column('end_time', sa.Time(), nullable=False),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.ForeignKeyConstraint(
			['restaurant_id'],
			['restaurants.id'],
		),
		sa.PrimaryKeyConstraint('id'),
	)

	op.create_table(
		'offers',
		sa.Column('id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('product_id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('price', sa.Double(), nullable=False),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.ForeignKeyConstraint(
			['product_id'],
			['products.id'],
		),
		sa.PrimaryKeyConstraint('id'),
	)

	op.create_table(
		'offer_schedules',
		sa.Column('id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('offer_id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('day', sa.String(length=10), nullable=False),
		sa.Column('start_time', sa.Time(), nullable=False),
		sa.Column('end_time', sa.Time(), nullable=False),
		sa.Column('repeats', sa.Boolean(), nullable=True),
		sa.Column('created_at', sa.DateTime(), nullable=False),
		sa.Column('updated_at', sa.DateTime(), nullable=False),
		sa.ForeignKeyConstraint(
			['offer_id'],
			['offers.id'],
		),
		sa.PrimaryKeyConstraint('id'),
	)


def downgrade() -> None:
	op.drop_table('offer_schedules')

	op.drop_table('offers')

	op.drop_table('restaurant_schedules')

	op.drop_table('products')

	op.drop_table('restaurants')

	op.drop_table('users')

	op.drop_table('categories')
