"""add phone number

Revision ID: bacd2e4fa3e6
Revises: 49e16d3b3a5a
Create Date: 2026-05-29 12:55:18.817635

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bacd2e4fa3e6'
down_revision: Union[str, Sequence[str], None] = '49e16d3b3a5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
