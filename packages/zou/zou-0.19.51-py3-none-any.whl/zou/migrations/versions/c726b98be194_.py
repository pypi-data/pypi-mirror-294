"""empty message

Revision ID: c726b98be194
Revises: fee7c696166e
Create Date: 2018-08-02 23:20:49.472287

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c726b98be194"
down_revision = "fee7c696166e"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "preview_file",
        sa.Column("extension", sa.String(length=6), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("preview_file", "extension")
    # ### end Alembic commands ###
