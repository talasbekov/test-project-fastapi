"""feature: survey

Revision ID: 363e359a19a9
Revises: 3d09ba117ccc
Create Date: 2023-06-20 10:04:21.129097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '363e359a19a9'
down_revision = '3d09ba117ccc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('surveys',
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('start_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('jurisdiction_id', sa.UUID(), nullable=True),
    sa.Column('is_anonymous', sa.Boolean(), nullable=True),
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
    sa.Column('survey_id', sa.UUID(), nullable=True),
    sa.Column('question_type', sa.Enum('TEXT', 'SINGLE_SELECTION', 'MULTIPLE_SELECTION', 'SCALE', 'GRID', 'CHECKBOX_GRID', name='questiontypeenum'), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['survey_id'], ['surveys.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('options',
    sa.Column('question_id', sa.UUID(), nullable=True),
    sa.Column('discriminator', sa.String(length=255), nullable=True),
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
    # ### end Alembic commands ###
