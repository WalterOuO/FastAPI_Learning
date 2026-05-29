"""create posts table

Revision ID: ed6a57e850d5
Revises: 
Create Date: 2026-05-29 11:16:30.107910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed6a57e850d5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
        sa.Column('title', sa.String(), nullable=False) 
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
