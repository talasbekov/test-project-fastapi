"""feature: added equipment

Revision ID: ace37bbadeb7
Revises: 5f9e8b2612e5
Create Date: 2023-02-08 09:57:56.463184

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ace37bbadeb7'
down_revision = '5f9e8b2612e5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('equipments',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('quantity', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_equipment',
    sa.Column('document_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('subject_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['equipments.id'], )
    )
    op.create_table('position_permission',
    sa.Column('position_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('permission_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], )
    )
    op.drop_table('position_permission_table')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('position_permission_table',
    sa.Column('position_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('permission_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], name='position_permission_table_permission_id_fkey'),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], name='position_permission_table_position_id_fkey')
    )
    op.drop_table('position_permission')
    op.drop_table('hr_document_equipment')
    op.drop_table('equipments')
    # ### end Alembic commands ###
