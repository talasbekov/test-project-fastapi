from sqlalchemy import TEXT, Column, ForeignKey, String, Table

from core import Base

users_badges = Table(
    "users_badges",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("badge_id", ForeignKey("badges.id"))
)

hr_document_equipments = Table(
    "hr_document_equipments",
    Base.metadata,
    Column("document_id", ForeignKey("hr_documents.id")),
    Column("subject_id", ForeignKey("equipments.id")),
)

hr_documents_users = Table(
    "hr_document_users",
    Base.metadata,
    Column("document_id", ForeignKey("hr_documents.id")),
    Column("subject_id", ForeignKey("users.id"))
)

user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
)

staff_unit_functions = Table(
    "staff_unit_functions",
    Base.metadata,
    Column("staff_unit_id", ForeignKey("staff_units.id")),
    Column("staff_function_id", ForeignKey("staff_functions.id"))
)