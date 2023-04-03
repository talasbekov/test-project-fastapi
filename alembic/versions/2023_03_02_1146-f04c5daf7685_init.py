"""init

Revision ID: f2bfe17f02b7
Revises: 
Create Date: 2023-03-02 11:46:48.090016

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f04c5daf7685'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('badges',
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('document_function_types',
    sa.Column('can_cancel', sa.Boolean(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('equipments',
    sa.Column('quantity', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_templates',
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('subject_type', sa.Enum('CANDIDATE', 'EMPLOYEE', 'PERSONNEL', 'STAFF', name='subjecttype'), nullable=True),
    sa.Column('properties', postgresql.JSON(none_as_null=True, astext_type=sa.Text()), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ranks',
    sa.Column('order', sa.Integer(), nullable=True),
    sa.Column('military_url', sa.TEXT(), nullable=True),
    sa.Column('employee_url', sa.TEXT(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('service_function_types',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff_divisions',
    sa.Column('parent_group_id', sa.UUID(), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('is_combat_unit', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_group_id'], ['staff_divisions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('positions',
    sa.Column('max_rank_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['max_rank_id'], ['ranks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('jurisdictions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff_functions',
    sa.Column('hours_per_week', sa.Integer(), nullable=True),
    sa.Column('discriminator', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=True),
    sa.Column('jurisdiction_id', sa.UUID(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('type_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['document_function_types.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['service_function_types.id'], ),
    sa.ForeignKeyConstraint(['jurisdiction_id'], ['jurisdictions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_steps',
    sa.Column('hr_document_template_id', sa.UUID(), nullable=False),
    sa.Column('staff_function_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['hr_document_template_id'], ['hr_document_templates.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_function_id'], ['staff_functions.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff_units',
    sa.Column('position_id', sa.UUID(), nullable=False),
    sa.Column('staff_division_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ),
    sa.ForeignKeyConstraint(['staff_division_id'], ['staff_divisions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_statuses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff_unit_functions',
    sa.Column('staff_unit_id', sa.UUID(), nullable=False),
    sa.Column('staff_function_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['staff_function_id'], ['staff_functions.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_unit_id'], ['staff_units.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('staff_unit_id', 'staff_function_id')
    )
    op.create_table('users',
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=True),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('father_name', sa.String(length=150), nullable=True),
    sa.Column('icon', sa.TEXT(), nullable=True),
    sa.Column('call_sign', sa.String(length=255), nullable=True),
    sa.Column('id_number', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=32), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('rank_id', sa.UUID(), nullable=True),
    sa.Column('staff_unit_id', sa.UUID(), nullable=False),
    sa.Column('actual_staff_unit_id', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(length=255), nullable=True),
    sa.Column('status_till', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('cabinet', sa.String(length=255), nullable=True),
    sa.Column('service_phone_number', sa.String(length=32), nullable=True),
    sa.Column('is_military', sa.Boolean(), nullable=True),
    sa.Column('personal_id', sa.String(length=255), nullable=True),
    sa.Column('supervised_by', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['actual_staff_unit_id'], ['staff_units.id'], ),
    sa.ForeignKeyConstraint(['rank_id'], ['ranks.id'], ),
    sa.ForeignKeyConstraint(['staff_unit_id'], ['staff_units.id'], ),
    sa.ForeignKeyConstraint(['supervised_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('call_sign'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id_number')
    )
    op.create_table('hr_documents',
    sa.Column('hr_document_template_id', sa.UUID(), nullable=True),
    sa.Column('status_id', sa.UUID(), nullable=True),
    sa.Column('initialized_by_id', sa.UUID(), nullable=True),
    sa.Column('due_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('properties', postgresql.JSON(none_as_null=True, astext_type=sa.Text()), nullable=True),
    sa.Column('reg_number', sa.String(), nullable=True),
    sa.Column('signed_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('last_step_id', sa.UUID(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['initialized_by_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['hr_document_template_id'], ['hr_document_templates.id'], ),
    sa.ForeignKeyConstraint(['last_step_id'], ['hr_document_steps.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['hr_document_statuses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('reg_number')
    )
    op.create_table('events',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('date_since', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('date_to', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_equipments',
    sa.Column('document_id', sa.UUID(), nullable=True),
    sa.Column('subject_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['equipments.id'], )
    )
    op.create_table('sport_types',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_infos',
    sa.Column('hr_document_step_id', sa.UUID(), nullable=False),
    sa.Column('assigned_to_id', sa.UUID(), nullable=True),
    sa.Column('signed_by_id', sa.UUID(), nullable=True),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.Column('is_signed', sa.Boolean(), nullable=True),
    sa.Column('signed_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('hr_document_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['assigned_to_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['hr_document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['hr_document_step_id'], ['hr_document_steps.id'], ),
    sa.ForeignKeyConstraint(['signed_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profiles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('personal_profiles',
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('family_statuses',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('biographic_infos',
    sa.Column('place_birth', sa.String(), nullable=True),
    sa.Column('date_birth', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('gender', sa.Boolean(), nullable=True),
    sa.Column('citizenship', sa.String(), nullable=True),
    sa.Column('nationality', sa.String(), nullable=True),
    sa.Column('family_status_id', sa.UUID(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('residence_address', sa.String(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['personal_profiles.id'], ),
    sa.ForeignKeyConstraint(['family_status_id'], ['family_statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('driving_licenses',
    sa.Column('document_number', sa.String(), nullable=True),
    sa.Column('category', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('date_of_issue', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('date_to', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('document_link', sa.TEXT(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['personal_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('identification_cards',
    sa.Column('document_number', sa.String(), nullable=True),
    sa.Column('date_of_issue', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('date_to', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('issued_by', sa.String(), nullable=True),
    sa.Column('document_link', sa.TEXT(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['personal_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('passports',
    sa.Column('document_number', sa.String(), nullable=True),
    sa.Column('date_of_issue', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('date_to', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('document_link', sa.TEXT(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['personal_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sport_achievements',
    sa.Column('assignment_date', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('document_link', sa.TEXT(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('sport_type_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['personal_profiles.id'], ),
    sa.ForeignKeyConstraint(['sport_type_id'], ['sport_types.id'],),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sport_degrees',
    sa.Column('assignment_date', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('document_link', sa.TEXT(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('sport_type_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['personal_profiles.id'], ),
    sa.ForeignKeyConstraint(['sport_type_id'], ['sport_types.id'],),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tax_declarations',
    sa.Column('year', sa.String(), nullable=True),
    sa.Column('is_paid', sa.Boolean(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['personal_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_financial_infos',
    sa.Column('iban', sa.String(), nullable=True),
    sa.Column('housing_payments_iban', sa.String(), nullable=True),
    sa.Column('profile_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
              nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['personal_profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_users',
    sa.Column('document_id', sa.UUID(), nullable=True),
    sa.Column('subject_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['users.id'], )
    )
    op.create_table('user_stats',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('physical_training', sa.Integer(), nullable=True),
    sa.Column('fire_training', sa.Integer(), nullable=True),
    sa.Column('attendance', sa.Integer(), nullable=True),
    sa.Column('activity', sa.Integer(), nullable=True),
    sa.Column('opinion_of_colleagues', sa.Integer(), nullable=True),
    sa.Column('opinion_of_management', sa.Integer(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users_badges',
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('badge_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['badge_id'], ['badges.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_badges')
    op.drop_table('user_stats')
    op.drop_table('hr_document_users')
    op.drop_table('hr_document_infos')
    op.drop_table('hr_document_equipments')
    op.drop_table('events')
    op.drop_table('users')
    op.drop_table('staff_unit_functions')
    op.drop_table('hr_documents')
    op.drop_table('staff_units')
    op.drop_table('hr_document_steps')
    op.drop_table('staff_functions')
    op.drop_table('positions')
    op.drop_table('staff_divisions')
    op.drop_table('service_function_types')
    op.drop_table('ranks')
    op.drop_table('jurisdictions')
    op.drop_table('hr_document_templates')
    op.drop_table('equipments')
    op.drop_table('document_function_types')
    op.drop_table('badges')
    op.drop_table('user_financial_infos')
    op.drop_table('tax_declarations')
    op.drop_table('sport_degrees')
    op.drop_table('sport_achievements')
    op.drop_table('passports')
    op.drop_table('identification_cards')
    op.drop_table('driving_licences')
    op.drop_table('biographic_infos')
    op.drop_table('personal_profiles')
    op.drop_table('profiles')
    # ### end Alembic commands ###
