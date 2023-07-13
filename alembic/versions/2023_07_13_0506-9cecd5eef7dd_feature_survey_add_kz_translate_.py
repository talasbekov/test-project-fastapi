"""feature(survey): add kz translate required column

Revision ID: 9cecd5eef7dd
Revises: 984201b8ecf3
Create Date: 2023-07-13 05:06:28.208613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cecd5eef7dd'
down_revision = '5895ed1b9641'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quizzes', sa.Column('is_kz_translate_required', sa.Boolean(), nullable=True))
    op.add_column('surveys', sa.Column('is_kz_translate_required', sa.Boolean(), nullable=True))
    op.execute("ALTER TYPE candidatestatusenum ADD VALUE 'COMPLETED'")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TYPE candidatestatusenum DROP VALUE 'COMPLETED'")
    op.drop_column('surveys', 'is_kz_translate_required')
    op.drop_column('quizzes', 'is_kz_translate_required')
    # ### end Alembic commands ###
