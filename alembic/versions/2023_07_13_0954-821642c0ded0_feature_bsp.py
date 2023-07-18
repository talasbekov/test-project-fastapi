"""feature bsp

Revision ID: 821642c0ded0
Revises: 7b43fce4da7e
Create Date: 2023-07-10 09:54:13.549546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '821642c0ded0'
down_revision = '59ab1232c593'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activities',
    sa.Column('parent_group_id', sa.UUID(), nullable=True),
    sa.Column('instructions', sa.TEXT(), nullable=True, default=''),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_group_id'], ['activities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('days',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('months',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('places',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('nameKZ', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bsp_plans',
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.Enum('ACTIVE', 'DRAFT', name='planstatus'), nullable=True),
    sa.Column('signed_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedule_years',
    sa.Column('plan_id', sa.UUID(), nullable=True),
    sa.Column('activity_id', sa.UUID(), nullable=True),
    sa.Column('is_exam_required', sa.Boolean(), nullable=True),
    sa.Column('retry_count', sa.Integer(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['activity_id'], ['activities.id'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['bsp_plans.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exam_schedules',
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('end_time', sa.Time(), nullable=True),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.Column('schedule_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule_years.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedule_exam_months',
    sa.Column('schedule_year_id', sa.UUID(), nullable=True),
    sa.Column('month_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['month_id'], ['months.id'], ),
    sa.ForeignKeyConstraint(['schedule_year_id'], ['schedule_years.id'], )
    )
    op.create_table('schedule_months',
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('place_id', sa.UUID(), nullable=True),
    sa.Column('schedule_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule_years.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedule_year_months',
    sa.Column('schedule_year_id', sa.UUID(), nullable=True),
    sa.Column('month_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['month_id'], ['months.id'], ),
    sa.ForeignKeyConstraint(['schedule_year_id'], ['schedule_years.id'], )
    )
    op.create_table('schedule_year_staff_divisions',
    sa.Column('schedule_year_id', sa.UUID(), nullable=True),
    sa.Column('staff_division_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_year_id'], ['schedule_years.id'], ),
    sa.ForeignKeyConstraint(['staff_division_id'], ['staff_divisions.id'], )
    )
    op.create_table('schedule_year_users',
    sa.Column('schedule_year_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_year_id'], ['schedule_years.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('attendances',
    sa.Column('attendance_date', sa.Date(), nullable=True),
    sa.Column('schedule_id', sa.UUID(), nullable=True),
    sa.Column('class_status', sa.Enum('STARTED', 'COMPLETED', 'WAITING', name='calssstatus'),
              nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule_months.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exam_results',
    sa.Column('exam_date', sa.Date(), nullable=True),
    sa.Column('grade', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('exam_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['exam_id'], ['exam_schedules.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exam_schedule_instructors',
    sa.Column('exam_schedule_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['exam_schedule_id'], ['exam_schedules.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('schedule_days',
    sa.Column('day_id', sa.UUID(), nullable=True),
    sa.Column('start_time', sa.Time(), nullable=True),
    sa.Column('end_time', sa.Time(), nullable=True),
    sa.Column('month_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['day_id'], ['days.id'], ),
    sa.ForeignKeyConstraint(['month_id'], ['schedule_months.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedule_month_instructors',
    sa.Column('schedule_month_id', sa.UUID(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['schedule_month_id'], ['schedule_months.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('attended_users',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('attendance_id', sa.UUID(), nullable=True),
    sa.Column('attendance_status', sa.Enum('ATTENDED', 'LATE',
                                           'ABSENT_REASON', 'ABSENT',
                                           name='attendancestatus'),
                                           nullable=True),
    sa.Column('reason', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['attendance_id'], ['attendances.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('absent_users')
    op.drop_table('attended_users')
    op.drop_table('schedule_month_instructors')
    op.drop_table('schedule_days')
    op.drop_table('exam_schedule_instructors')
    op.drop_table('exam_results')
    op.drop_table('attendances')
    op.drop_table('schedule_year_users')
    op.drop_table('schedule_year_staff_divisions')
    op.drop_table('schedule_year_months')
    op.drop_table('schedule_months')
    op.drop_table('schedule_exam_months')
    op.drop_table('exam_schedules')
    op.drop_table('schedule_years')
    op.drop_table('bsp_plans')
    op.drop_table('places')
    op.drop_table('months')
    op.drop_table('days')
    op.drop_table('activities')
    # ### end Alembic commands ###
