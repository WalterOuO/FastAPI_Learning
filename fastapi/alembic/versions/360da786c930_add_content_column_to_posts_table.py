"""add content column to posts table

Revision ID: 360da786c930
Revises: ed6a57e850d5
Create Date: 2026-05-29 11:45:59.236323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '360da786c930'
down_revision: Union[str, Sequence[str], None] = 'ed6a57e850d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
