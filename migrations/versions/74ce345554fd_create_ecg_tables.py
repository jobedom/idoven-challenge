# pylint: disable=invalid-name, no-member

"""Create ECG tables

Revision ID: 74ce345554fd
Revises: 
Create Date: 2024-03-18 23:50:33.204514

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "74ce345554fd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ecgs",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("owner_id", sa.Integer, nullable=False),
        sa.Column("date", sa.DateTime, nullable=False),
        sa.Column("leads", sa.JSON, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("ecgs")
