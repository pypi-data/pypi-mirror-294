"""add archived fields

Revision ID: 8588f254d6b8
Revises: f0c6cbb61869
Create Date: 2022-09-06 14:03:39.729550

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8588f254d6b8"
down_revision = "f0c6cbb61869"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("person", sa.Column("archived", sa.Boolean(), default=False))
    op.add_column(
        "task_status", sa.Column("archived", sa.Boolean(), default=False)
    )
    op.add_column(
        "task_type", sa.Column("archived", sa.Boolean(), default=False)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("task_type", "archived")
    op.drop_column("task_status", "archived")
    op.drop_column("person", "archived")
    # ### end Alembic commands ###
