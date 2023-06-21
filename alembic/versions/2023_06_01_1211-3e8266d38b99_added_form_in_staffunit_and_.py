"""Added form in StaffUnit and ArchiveStaffUnit

Revision ID: 3e8266d38b99
Revises: 5a1d234bea01
Create Date: 2023-06-01 12:11:35.941080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e8266d38b99'
down_revision = '5a1d234bea01'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('archive_staff_units', sa.Column('curator_of_id', sa.UUID(), nullable=True))
    op.add_column('archive_staff_units', sa.Column('form', sa.Enum('form1', 'form2', 'form3', name='formenum'), nullable=True))
    op.create_foreign_key(None, 'archive_staff_units', 'staff_divisions', ['curator_of_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'archive_staff_units', 'users', ['user_replacing_id'], ['id'])
    op.add_column('staff_units', sa.Column('form', sa.Enum('form1', 'form2', 'form3', name='formenum'), nullable=True))
    op.create_foreign_key(None, 'staff_units', 'users', ['user_replacing_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'staff_units', type_='foreignkey')
    op.drop_column('staff_units', 'form')
    op.drop_constraint(None, 'archive_staff_units', type_='foreignkey')
    op.drop_constraint(None, 'archive_staff_units', type_='foreignkey')
    op.drop_column('archive_staff_units', 'form')
    op.drop_column('archive_staff_units', 'curator_of_id')
    # ### end Alembic commands ###
