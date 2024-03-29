"""feat: added notifications

Revision ID: b6c2329ba373
Revises: bd9403c8f894
Create Date: 2023-04-26 01:41:18.077233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6c2329ba373'
down_revision = 'bd9403c8f894'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('message', sa.TEXT(), nullable=False),
    sa.Column('sender_id', sa.String(), nullable=False),
    sa.Column('receiver_id', sa.String(), nullable=False),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notifications_receiver_id'), 'notifications', ['receiver_id'], unique=False)
    op.create_index(op.f('ix_notifications_sender_id'), 'notifications', ['sender_id'], unique=False)
    op.create_unique_constraint(None, 'abroad_travels', ['id'])
    op.drop_constraint('histories_emergency_rank_id_fkey', 'histories', type_='foreignkey')
    op.drop_column('histories', 'emergency_rank_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('histories', sa.Column('emergency_rank_id', sa.String(), autoincrement=False, nullable=True))
    op.create_foreign_key('histories_emergency_rank_id_fkey', 'histories', 'ranks', ['emergency_rank_id'], ['id'])
    op.drop_constraint(None, 'abroad_travels', type_='unique')
    op.drop_index(op.f('ix_notifications_sender_id'), table_name='notifications')
    op.drop_index(op.f('ix_notifications_receiver_id'), table_name='notifications')
    op.drop_table('notifications')
    # ### end Alembic commands ###
