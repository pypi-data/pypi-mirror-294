"""Add nb entities out field to entity table

Revision ID: 1e150c2cea4d
Revises: 9060dd4f6116
Create Date: 2021-11-22 16:39:09.420069

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1e150c2cea4d"
down_revision = "9060dd4f6116"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "entity", sa.Column("nb_entities_out", sa.Integer(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("entity", "nb_entities_out")
    # ### end Alembic commands ###
