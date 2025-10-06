"""init

Revision ID: a57982c155f4
Revises: 216447c9519a
Create Date: 2025-10-06 13:21:48.706671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a57982c155f4'
down_revision: Union[str, Sequence[str], None] = '216447c9519a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
