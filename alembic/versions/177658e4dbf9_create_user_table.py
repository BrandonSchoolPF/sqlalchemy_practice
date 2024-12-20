"""Create User Table

Revision ID: 177658e4dbf9
Revises: 
Create Date: 2024-12-19 13:55:03.155571

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '177658e4dbf9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "employee",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable= False),
        sa.Column("current", sa.Boolean, default = True)
    )


def downgrade() -> None:
    op.drop_table("employee")
