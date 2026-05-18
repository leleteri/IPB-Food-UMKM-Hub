"""empty message

Revision ID: c6df71dfd550
Revises: d3267169c1e4
Create Date: 2026-05-18 11:25:14.101529

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6df71dfd550'
down_revision: Union[str, Sequence[str], None] = 'd3267169c1e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
