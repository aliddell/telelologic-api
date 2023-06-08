"""Create users table

Revision ID: 00362f094954
Revises: 
Create Date: 2023-06-07 17:22:08.858838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00362f094954'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String),
        sa.Column("authenticated", sa.Boolean),
    )


def downgrade() -> None:
    op.drop_table("users")
