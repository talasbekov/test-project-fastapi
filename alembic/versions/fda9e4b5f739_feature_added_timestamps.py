"""feature: added timestamps

Revision ID: fda9e4b5f739
Revises: 549071e55938
Create Date: 2023-02-06 22:26:57.186917

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fda9e4b5f739'
down_revision = '549071e55938'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hr_document_templates', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('hr_document_templates', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('hr_documents', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('hr_documents', sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hr_documents', 'updated_at')
    op.drop_column('hr_documents', 'created_at')
    op.drop_column('hr_document_templates', 'updated_at')
    op.drop_column('hr_document_templates', 'created_at')
    # ### end Alembic commands ###
