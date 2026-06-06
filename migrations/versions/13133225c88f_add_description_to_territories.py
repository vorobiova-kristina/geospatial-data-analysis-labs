"""add description to territories

Revision ID: 13133225c88f
Revises: 001_create_territories_metrics
Create Date: 2026-06-06 14:24:38.650825

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "13133225c88f"
down_revision: Union[str, Sequence[str], None] = "001_create_territories_metrics"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "territories",
        sa.Column("description", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("territories", "description")
