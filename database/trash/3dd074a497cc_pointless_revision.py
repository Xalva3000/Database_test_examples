"""pointless revision

Revision ID: 3dd074a497cc
Revises: 
Create Date: 2024-06-27 10:52:01.875078

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3dd074a497cc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(256), nullable=False),
        sa.Column('text', sa.Text, nullable=True),
        sa.Column('date_create', sa.DateTime, default=datetime.now)
    )


def downgrade() -> None:
    op.drop_table("books")
