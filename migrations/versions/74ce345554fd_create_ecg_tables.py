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
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("date", sa.DateTime, nullable=False),
    )

    op.create_table(
        "leads",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("ecg_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(10), nullable=False),
        sa.Column("signal", sa.JSON, default=list, nullable=False),
        sa.ForeignKeyConstraint(
            ("ecg_id",),
            ["ecg.id"],
        ),
    )


def downgrade() -> None:
    op.drop_table("ecgs")
    op.drop_table("leads")
