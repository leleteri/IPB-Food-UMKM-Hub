"""empty message

Revision ID: 67281fe01d26
Revises: 1ba21884f920
Create Date: 2026-05-12 19:02:26.800271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67281fe01d26'
down_revision: Union[str, Sequence[str], None] = '1ba21884f920'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
