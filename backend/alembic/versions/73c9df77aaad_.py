"""empty message

Revision ID: 73c9df77aaad
Revises: bfed63d343fb
Create Date: 2026-05-18 11:29:14.614105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73c9df77aaad'
down_revision: Union[str, Sequence[str], None] = 'bfed63d343fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
