"""added initial comment in hr_document

Revision ID: 576296a7cdac
Revises: 3e8266d38b99
Create Date: 2023-06-01 13:46:21.341564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "576296a7cdac"
down_revision = "461e308e6b57"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, "archive_staff_units", "users", ["user_replacing_id"], ["id"])
    op.add_column("hr_document_templates", sa.Column("is_due_date_required", sa.Boolean(), nullable=True))
    op.add_column("hr_document_templates", sa.Column("is_initial_comment_required", sa.Boolean(), nullable=True))
    op.add_column("hr_documents", sa.Column("initial_comment", sa.TEXT(), nullable=True))
    op.create_foreign_key(None, "staff_units", "users", ["user_replacing_id"], ["id"])
    op.add_column("hr_documents", sa.Column("initialized_at", sa.TIMESTAMP(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "staff_units", type_="foreignkey")
    op.drop_column("hr_documents", "initial_comment")
    op.drop_column("hr_document_templates", "is_initial_comment_required")
    op.drop_column("hr_document_templates", "is_due_date_required")
    op.drop_constraint(None, "archive_staff_units", type_="foreignkey")
    op.drop_column("hr_documents", "initialized_at")
    # ### end Alembic commands ###