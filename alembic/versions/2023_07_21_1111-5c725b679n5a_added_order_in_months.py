"""added_order_in_months

Revision ID: 8d265b679e4c
Revises: 09b20dbda183
Create Date: 2023-07-19 06:05:02.528988

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '5c725b679n5a'
down_revision = 'b0729833b50a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('months', sa.Column('order', sa.Integer(),
                                    sa.Identity(start=1, cycle=True),
                                    nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('months', 'order')
    # ### end Alembic commands ###