"""update

Revision ID: 3813f6cf7fcd
Revises: a57982c155f4
Create Date: 2025-10-09 11:59:49.163279

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3813f6cf7fcd'
down_revision: Union[str, Sequence[str], None] = 'a57982c155f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
