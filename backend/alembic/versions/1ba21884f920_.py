"""empty message

Revision ID: 1ba21884f920
Revises: 794a64f4566c
Create Date: 2026-05-12 18:48:45.287959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ba21884f920'
down_revision: Union[str, Sequence[str], None] = '794a64f4566c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
