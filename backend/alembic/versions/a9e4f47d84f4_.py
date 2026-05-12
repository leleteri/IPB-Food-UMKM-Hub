"""empty message

Revision ID: a9e4f47d84f4
Revises: 67281fe01d26
Create Date: 2026-05-12 19:02:56.797353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9e4f47d84f4'
down_revision: Union[str, Sequence[str], None] = '67281fe01d26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
