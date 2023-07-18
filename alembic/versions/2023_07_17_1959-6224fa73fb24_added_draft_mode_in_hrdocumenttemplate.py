"""Added draft mode in HrDocumentTemplate

Revision ID: 6224fa73fb24
Revises: 87263d264688
Create Date: 2023-07-17 19:59:56.260420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6224fa73fb24'
down_revision = 'd1a279cadf15'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('hr_document_templates', sa.Column('is_draft', sa.Boolean(), nullable=True))


def downgrade() -> None:
    op.drop_column('hr_document_templates', 'is_draft')
