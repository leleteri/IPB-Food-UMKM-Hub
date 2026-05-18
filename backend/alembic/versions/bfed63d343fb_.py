"""empty message

Revision ID: bfed63d343fb
Revises: c6df71dfd550
Create Date: 2026-05-18 11:28:16.714750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bfed63d343fb'
down_revision: Union[str, Sequence[str], None] = 'c6df71dfd550'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
