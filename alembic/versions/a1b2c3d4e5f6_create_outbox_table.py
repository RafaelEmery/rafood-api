"""create outbox table

Revision ID: a1b2c3d4e5f6
Revises: c3a8f9124e56
Create Date: 2026-08-23 19:20:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa
import sqlalchemy_utils as sa_utils
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = 'a1b2c3d4e5f6'
down_revision: str | None = 'c3a8f9124e56'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
	op.create_table(
		'outbox',
		sa.Column('id', sa_utils.types.uuid.UUIDType(binary=False), nullable=False),
		sa.Column('aggregatetype', sa.String(length=255), nullable=False),
		sa.Column('aggregateid', sa.String(length=255), nullable=False),
		sa.Column('type', sa.String(length=255), nullable=False),
		sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
		sa.PrimaryKeyConstraint('id'),
	)


def downgrade() -> None:
	op.drop_table('outbox')
