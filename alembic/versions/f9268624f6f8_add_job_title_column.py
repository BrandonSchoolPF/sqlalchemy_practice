"""add job_title column

Revision ID: f9268624f6f8
Revises: 177658e4dbf9
Create Date: 2024-12-19 14:04:04.903915

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f9268624f6f8'
down_revision: Union[str, None] = '177658e4dbf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "employee",
        sa.Column("job_title", sa.String(64), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("employee", "job_title")
