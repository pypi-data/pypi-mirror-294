"""Add notifications enabled flag

Revision ID: 590aa1ffe731
Revises: 54ee0d1d60ba
Create Date: 2019-06-30 13:19:43.298001

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "590aa1ffe731"
down_revision = "54ee0d1d60ba"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "person",
        sa.Column("notifications_enabled", sa.Boolean(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("person", "notifications_enabled")
    # ### end Alembic commands ###
