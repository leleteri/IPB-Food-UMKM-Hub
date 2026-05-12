"""empty message

Revision ID: bec891356dd2
Revises: 7931d9913f74
Create Date: 2026-05-12 19:07:44.010872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bec891356dd2'
down_revision: Union[str, Sequence[str], None] = '7931d9913f74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
