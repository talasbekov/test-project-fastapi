"""feature: survey

Revision ID: 9381b17d68c4
Revises: 3d09ba117ccc
Create Date: 2023-06-17 10:51:31.460472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9381b17d68c4'
down_revision = '3d09ba117ccc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_types',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('survey_types',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answers',
    sa.Column('question_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['survey_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('surveys',
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('start_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('type_id', sa.UUID(), nullable=True),
    sa.Column('jurisdiction_id', sa.UUID(), nullable=True),
    sa.Column('owner_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['jurisdiction_id'], ['jurisdictions.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['survey_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('text', sa.TEXT(), nullable=False),
    sa.Column('is_required', sa.Boolean(), nullable=False),
    sa.Column('survey_id', sa.UUID(), nullable=True),
    sa.Column('question_type_id', sa.UUID(), nullable=True),
    sa.Column('discriminator', sa.String(length=255), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['question_type_id'], ['question_types.id'], ),
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
    sa.Column('min_value', sa.Integer(), nullable=False),
    sa.Column('max_value', sa.Integer(), nullable=False),
    sa.Column('row_position', sa.Integer(), nullable=False),
    sa.Column('column_position', sa.Integer(), nullable=False),
    sa.Column('is_checked', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
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
    op.drop_table('options')
    op.drop_table('questions')
    op.drop_table('surveys')
    op.drop_table('answers')
    op.drop_table('survey_types')
    op.drop_table('question_types')
    # ### end Alembic commands ###
