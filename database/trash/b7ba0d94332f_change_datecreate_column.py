"""change datecreate column

Revision ID: b7ba0d94332f
Revises: 02259563440c
Create Date: 2024-06-27 11:14:19.075164

"""
from datetime import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'b7ba0d94332f'
down_revision: Union[str, None] = '02259563440c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'books',
        'date_update',
        onupdate=text("TIMEZONE('utc', now())"),
    )


def downgrade() -> None:
    op.alter_column(
        'books',
        'date_update',
        onupdate=datetime.utcnow,
    )
