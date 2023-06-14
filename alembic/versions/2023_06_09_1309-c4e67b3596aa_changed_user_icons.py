"""changed user icons

Revision ID: c4e67b3596aa
Revises: fea4179cc54c
Create Date: 2023-06-09 13:09:18.800454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4e67b3596aa'
down_revision = 'fea4179cc54c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    icon = 'http://192.168.0.169:8083/static/placeholder.jpg'
    op.execute(
        f"UPDATE users "
        f"SET icon = '{icon}'"
        f" WHERE email in ('s_isabekov@sgo.kz', 'a_kibataev@sgo.kz',"
        f"                 'a_amankeldiuly@sgo.kz', 'b_abdyshev@sgo.kz');"
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    pass
