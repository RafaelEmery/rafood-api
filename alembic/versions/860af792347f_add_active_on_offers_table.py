"""add active on offers table

Revision ID: 860af792347f
Revises: 54cd1f3291e2
Create Date: 2025-12-14 18:58:16.615468

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '860af792347f'
down_revision: Union[str, None] = '54cd1f3291e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
	op.add_column(
		'offers', sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true())
	)


def downgrade() -> None:
	op.drop_column('offers', 'active')
