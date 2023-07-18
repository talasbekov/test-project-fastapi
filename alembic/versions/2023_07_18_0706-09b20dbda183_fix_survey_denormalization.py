"""fix(survey): denormalization


Revision ID: 09b20dbda183
Revises: d1a279cadf15
Create Date: 2023-07-18 07:06:38.794097

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '09b20dbda183'
down_revision = 'd1a279cadf15'
branch_labels = None
depends_on = None


def upgrade() -> None:
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('questions_quiz_id_fkey', 'questions', type_='foreignkey')
    op.drop_column('options', 'discriminator')
    op.drop_column('questions', 'quiz_id')
    op.drop_column('questions', 'discriminator')
    op.drop_table('quizzes')
    op.add_column('surveys', sa.Column('type', sa.String()))
    op.alter_column('surveys', 'is_kz_translate_required',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.execute(sa.text("UPDATE surveys " +
                        "SET type = 'SURVEY'")
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('surveys', 'is_kz_translate_required',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.add_column('questions', sa.Column('discriminator', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.add_column('questions', sa.Column('quiz_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('questions_quiz_id_fkey', 'questions', 'quizzes', ['quiz_id'], ['id'])
    op.add_column('options', sa.Column('discriminator', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.create_table('quizzes',
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('start_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('end_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('staff_position', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('jurisdiction_type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('certain_member_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('staff_division_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('nameKZ', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('is_kz_translate_required', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['certain_member_id'], ['users.id'], name='quizzes_certain_member_id_fkey'),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], name='quizzes_owner_id_fkey'),
    sa.ForeignKeyConstraint(['staff_division_id'], ['staff_divisions.id'], name='quizzes_staff_division_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='quizzes_pkey')
    )
    # ### end Alembic commands ###
