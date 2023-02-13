"""refactor: changed table names

Revision ID: f6f67b8ffa25
Revises: f1e92f92a36b
Create Date: 2023-02-13 09:17:16.249096

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6f67b8ffa25'
down_revision = 'f1e92f92a36b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hr_document_equipments',
    sa.Column('document_id', sa.UUID(), nullable=True),
    sa.Column('subject_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['equipments.id'], )
    )
    op.create_table('hr_document_users',
    sa.Column('document_id', sa.UUID(), nullable=True),
    sa.Column('subject_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['users.id'], )
    )
    op.drop_table('document_users')
    op.drop_table('hr_document_equipment')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hr_document_equipment',
    sa.Column('document_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('subject_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], name='hr_document_equipment_document_id_fkey'),
    sa.ForeignKeyConstraint(['subject_id'], ['equipments.id'], name='hr_document_equipment_subject_id_fkey')
    )
    op.create_table('document_users',
    sa.Column('document_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('subject_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], name='document_users_document_id_fkey'),
    sa.ForeignKeyConstraint(['subject_id'], ['users.id'], name='document_users_subject_id_fkey')
    )
    op.drop_table('hr_document_users')
    op.drop_table('hr_document_equipments')
    # ### end Alembic commands ###
