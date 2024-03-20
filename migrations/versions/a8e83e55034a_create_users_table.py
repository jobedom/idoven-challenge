# pylint: disable=invalid-name, no-member

"""Create users table

Revision ID: a8e83e55034a
Revises: 74ce345554fd
Create Date: 2024-03-20 00:47:12.555194

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a8e83e55034a"
down_revision: Union[str, None] = "74ce345554fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users_table = op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("is_admin", sa.Boolean, default=False, nullable=False),
    )

    op.bulk_insert(
        users_table,
        [
            {
                "email": "idoven@example.com",
                "password": "aaaa",
                "is_admin": True,
            }
        ],
    )


def downgrade() -> None:
    op.drop_table("users")
