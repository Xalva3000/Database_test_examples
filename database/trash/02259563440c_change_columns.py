"""change columns

Revision ID: 02259563440c
Revises: 3dd074a497cc
Create Date: 2024-06-27 11:04:13.433802

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '02259563440c'
down_revision: Union[str, None] = '3dd074a497cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'books',
        'date_create',
        default=None,
        server_default=text("TIMEZONE('utc', now())")
    )
    op.add_column(
        'books',
        sa.Column('date_update', sa.DateTime,
                  server_default=text("TIMEZONE('utc', now())"),
                  onupdate=datetime.utcnow)
    )



def downgrade() -> None:
    op.alter_column(
        'books',
        'date_create',
        default=datetime.now,
        server_default=None
    )
    op.drop_column('books', 'date_update')
