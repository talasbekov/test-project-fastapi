"""init: db

Revision ID: f9f7edaa69b6
Revises: 
Create Date: 2023-02-09 12:51:33.844398

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f9f7edaa69b6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('badges',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('equipments',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('quantity', sa.BigInteger(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('groups',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('parent_group_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['parent_group_id'], ['groups.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_templates',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('path', sa.String(length=255), nullable=True),
    sa.Column('subject_type', sa.Enum('CANDIDATE', 'EMPLOYEE', 'PERSONNEL', 'STAFF', name='subjecttype'), nullable=True),
    sa.Column('properties', postgresql.JSON(none_as_null=True, astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permissions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ranks',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_steps',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('hr_document_template_id', sa.UUID(), nullable=False),
    sa.Column('position_id', sa.UUID(), nullable=False),
    sa.Column('role_id', sa.UUID(), nullable=False),
    sa.Column('previous_step_id', sa.UUID(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['hr_document_template_id'], ['hr_document_templates.id'], ),
    sa.ForeignKeyConstraint(['previous_step_id'], ['hr_document_steps.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_documents',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('hr_document_template_id', sa.UUID(), nullable=True),
    sa.Column('status', sa.Enum('INITIALIZED', 'IN_PROGRESS', 'COMPLETED', 'CANCELED', 'ON_REVISION', name='hrdocumentstatus'), nullable=True),
    sa.Column('due_date', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('properties', postgresql.JSON(none_as_null=True, astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['hr_document_template_id'], ['hr_document_templates.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('positions',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('max_rank_id', sa.UUID(), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['max_rank_id'], ['ranks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_equipment',
    sa.Column('document_id', sa.UUID(), nullable=True),
    sa.Column('subject_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['equipments.id'], )
    )
    op.create_table('position_permission',
    sa.Column('position_id', sa.UUID(), nullable=True),
    sa.Column('permission_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], )
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=True),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('father_name', sa.String(length=150), nullable=True),
    sa.Column('group_id', sa.UUID(), nullable=True),
    sa.Column('call_sign', sa.String(length=255), nullable=True),
    sa.Column('id_number', sa.String(length=255), nullable=True),
    sa.Column('phone_number', sa.String(length=32), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('position_id', sa.UUID(), nullable=True),
    sa.Column('actual_position_id', sa.UUID(), nullable=True),
    sa.Column('rank_id', sa.UUID(), nullable=True),
    sa.Column('birthday', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['actual_position_id'], ['positions.id'], ),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], ),
    sa.ForeignKeyConstraint(['rank_id'], ['ranks.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('call_sign'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id_number')
    )
    op.create_table('document_users',
    sa.Column('document_id', sa.UUID(), nullable=True),
    sa.Column('subject_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['users.id'], )
    )
    op.create_table('events',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('date_since', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('date_to', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('hr_document_infos',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('hr_document_step_id', sa.UUID(), nullable=False),
    sa.Column('signed_by', sa.UUID(), nullable=True),
    sa.Column('comment', sa.TEXT(), nullable=True),
    sa.Column('is_signed', sa.Boolean(), nullable=True),
    sa.Column('hr_document_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['hr_document_id'], ['hr_documents.id'], ),
    sa.ForeignKeyConstraint(['hr_document_step_id'], ['hr_document_steps.id'], ),
    sa.ForeignKeyConstraint(['signed_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_stats',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('physical_training', sa.Integer(), nullable=True),
    sa.Column('fire_training', sa.Integer(), nullable=True),
    sa.Column('attendance', sa.Integer(), nullable=True),
    sa.Column('activity', sa.Integer(), nullable=True),
    sa.Column('opinion_of_colleagues', sa.Integer(), nullable=True),
    sa.Column('opinion_of_management', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
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
    op.drop_table('hr_document_infos')
    op.drop_table('events')
    op.drop_table('document_users')
    op.drop_table('users')
    op.drop_table('position_permission')
    op.drop_table('hr_document_equipment')
    op.drop_table('positions')
    op.drop_table('hr_documents')
    op.drop_table('hr_document_steps')
    op.drop_table('roles')
    op.drop_table('ranks')
    op.drop_table('permissions')
    op.drop_table('hr_document_templates')
    op.drop_table('groups')
    op.drop_table('equipments')
    op.drop_table('badges')
    # ### end Alembic commands ###
