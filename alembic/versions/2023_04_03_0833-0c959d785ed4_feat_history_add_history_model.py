"""feat(history): add history model

Revision ID: 0c959d785ed4
Revises: f2d361d3fec3
Create Date: 2023-04-03 08:33:22.825073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c959d785ed4'
down_revision = 'f2d361d3fec3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('histories',
    sa.Column('date_from', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('date_to', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('staff_unit_id', sa.UUID(), nullable=True),
    sa.Column('rank_id', sa.UUID(), nullable=True),
    sa.Column('position_id', sa.UUID(), nullable=True),
    sa.Column('equipment_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['equipment_id'], ['equipments.id'], ),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ),
    sa.ForeignKeyConstraint(['rank_id'], ['ranks.id'], ),
    sa.ForeignKeyConstraint(['staff_unit_id'], ['staff_units.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('histories')
    # ### end Alembic commands ###
