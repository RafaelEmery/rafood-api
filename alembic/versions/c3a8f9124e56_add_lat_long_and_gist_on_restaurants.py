"""add lat long and gist on restaurants

Revision ID: c3a8f9124e56
Revises: b7c4e8912d03
Create Date: 2026-05-23 14:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = 'c3a8f9124e56'
down_revision: str | None = 'b7c4e8912d03'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
	op.add_column('restaurants', sa.Column('latitude', sa.Float(), nullable=False))
	op.add_column('restaurants', sa.Column('longitude', sa.Float(), nullable=False))
	op.execute(
		"""
		CREATE INDEX ix_restaurants_location_gist ON restaurants
		USING GIST (
			geography(ST_SetSRID(ST_MakePoint(longitude, latitude), 4326))
		)
		"""
	)


def downgrade() -> None:
	op.execute('DROP INDEX IF EXISTS ix_restaurants_location_gist')
	op.drop_column('restaurants', 'longitude')
	op.drop_column('restaurants', 'latitude')
