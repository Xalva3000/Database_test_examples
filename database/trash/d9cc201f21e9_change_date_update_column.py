"""change date update column

Revision ID: d9cc201f21e9
Revises: b7ba0d94332f
Create Date: 2024-06-27 11:20:42.444820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'd9cc201f21e9'
down_revision: Union[str, None] = 'b7ba0d94332f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'books',
        'date_update',
        onupdate=sa.func.current_timestamp(),
    )


def downgrade() -> None:
    op.alter_column(
        'books',
        'date_update',
        onupdate=text("TIMEZONE('utc', now())"),
    )
