"""add unique constraint to category name

Revision ID: 54cd1f3291e2
Revises: 0a83557f5a74
Create Date: 2025-12-10 08:25:13.176945

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '54cd1f3291e2'
down_revision: str | None = '0a83557f5a74'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
	# Deleting repeated categories on categories table
	op.execute("""
        DELETE FROM categories a USING categories b
        WHERE a.id > b.id AND a.name = b.name
    """)

	op.create_unique_constraint('uq_categories_name', 'categories', ['name'])


def downgrade() -> None:
	op.drop_constraint('uq_categories_name', 'categories', type_='unique')
