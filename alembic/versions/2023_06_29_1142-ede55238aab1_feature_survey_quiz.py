"""feature/survey & quiz

Revision ID: ede55238aab1
Revises: dac7288a7141
Create Date: 2023-06-29 11:42:34.682686

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ede55238aab1'
down_revision = 'dac7288a7141'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('quizzes',
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('start_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('jurisdiction_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('owner_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['jurisdiction_id'], ['jurisdictions.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('surveys',
    sa.Column('is_anonymous', sa.Boolean(), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('start_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('jurisdiction_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('owner_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['jurisdiction_id'], ['jurisdictions.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('text', sa.TEXT(), nullable=False),
    sa.Column('is_required', sa.Boolean(), nullable=False),
    sa.Column('question_type', sa.Enum('TEXT', 'SINGLE_SELECTION', 'MULTIPLE_SELECTION', 'SCALE', 'GRID', 'CHECKBOX_GRID', name='questiontypeenum'), nullable=False),
    sa.Column('discriminator', sa.String(length=255), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('survey_id', sa.UUID(), nullable=True),
    sa.Column('quiz_id', sa.UUID(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['quiz_id'], ['quizzes.id'], ),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('options',
    sa.Column('question_id', sa.UUID(), nullable=True),
    sa.Column('discriminator', sa.String(length=255), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('text', sa.TEXT(), nullable=True),
    sa.Column('min_value', sa.Integer(), nullable=True),
    sa.Column('max_value', sa.Integer(), nullable=True),
    sa.Column('row_position', sa.Integer(), nullable=True),
    sa.Column('column_position', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answers',
    sa.Column('question_id', sa.UUID(), nullable=True),
    sa.Column('discriminator', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('text', sa.TEXT(), nullable=True),
    sa.Column('option_id', sa.UUID(), nullable=True),
    sa.Column('scale_value', sa.Integer(), nullable=True),
    sa.Column('grid_values', sa.JSON(), nullable=True),
    sa.Column('checkbox_grid_values', sa.JSON(), nullable=True),
    sa.ForeignKeyConstraint(['option_id'], ['options.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answers_options',
    sa.Column('option_id', sa.UUID(), nullable=True),
    sa.Column('answer_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['answer_id'], ['answers.id'], ),
    sa.ForeignKeyConstraint(['option_id'], ['options.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers_options')
    op.drop_table('answers')
    op.drop_table('options')
    op.drop_table('questions')
    op.drop_table('surveys')
    op.drop_table('quizzes')
    # ### end Alembic commands ###
