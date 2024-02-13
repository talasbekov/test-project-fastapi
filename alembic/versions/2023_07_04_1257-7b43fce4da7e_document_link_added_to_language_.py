"""document_link added to language_proficiency

Revision ID: 7b43fce4da7e
Revises: dac7288a7141
Create Date: 2023-07-04 12:57:34.154260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b43fce4da7e'
down_revision = 'dac7288a7141'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('language_proficiencies', sa.Column('document_number', sa.String(), nullable=True))
    op.add_column('language_proficiencies', sa.Column('document_link', sa.TEXT(), nullable=True))
    op.add_column('language_proficiencies', sa.Column('assignment_date', sa.DATE(), nullable=True))


def downgrade() -> None:
    op.drop_column('language_proficiencies', 'assignment_date')
    op.drop_column('language_proficiencies', 'document_link')
    op.drop_column('language_proficiencies', 'document_number')