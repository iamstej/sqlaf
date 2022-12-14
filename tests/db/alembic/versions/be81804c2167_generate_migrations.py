"""./generate_migrations

Revision ID: be81804c2167
Revises: 10fff1c96965
Create Date: 2022-01-13 22:36:18.340592

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "be81804c2167"
down_revision = "10fff1c96965"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("booking", sa.Column("guest_names", postgresql.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("booking", "guest_names")
    # ### end Alembic commands ###
