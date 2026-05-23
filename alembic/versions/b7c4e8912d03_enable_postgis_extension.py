"""enable postgis extension

Revision ID: b7c4e8912d03
Revises: 860af792347f
Create Date: 2026-05-23 12:00:00.000000

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b7c4e8912d03'
down_revision: str | None = '860af792347f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
	op.execute('CREATE EXTENSION IF NOT EXISTS postgis')


def downgrade() -> None:
	op.execute('DROP EXTENSION IF EXISTS postgis')
