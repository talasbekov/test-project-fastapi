"""bsp_schedule_year_is_active

Revision ID: b0729833b50a
Revises: 8d265b679e4c
Create Date: 2023-07-20 12:59:10.363799

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = 'b0729833b50a'
down_revision = '8d265b679e4c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('schedule_years', sa.Column('is_active', sa.Boolean(), default=True))
    conn = op.get_bind()
    conn.execute(
        text(f"""UPDATE schedule_years
                 SET is_active = 'true';""")
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('schedule_years', 'is_active')
    # ### end Alembic commands ###