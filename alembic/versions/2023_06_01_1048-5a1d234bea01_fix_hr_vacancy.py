"""fix/hr-vacancy

Revision ID: 5a1d234bea01
Revises: ID: b6c2329ba373
Create Date: 2023-06-01 10:48:45.512943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a1d234bea01'
down_revision = 'b6c2329ba373'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hr_vacancy_candidates',
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('hr_vacancy_id', sa.String(), nullable=True),
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['hr_vacancy_id'], ['hr_vacancies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('hr_vacancy_hr_vacancy_candidates')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hr_vacancy_hr_vacancy_candidates',
    sa.Column('hr_vacancy_id', sa.String(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.String(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['hr_vacancy_id'], ['hr_vacancies.id'], name='hr_vacancy_hr_vacancy_candidates_hr_vacancy_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='hr_vacancy_hr_vacancy_candidates_user_id_fkey')
    )
    op.drop_table('hr_vacancy_candidates')
    # ### end Alembic commands ###
