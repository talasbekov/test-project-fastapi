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

staff_unit_function = Table(
    "staff_unit_functions",
    Base.metadata,
    Column("staff_unit_id", ForeignKey("staff_units.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
    Column("staff_function_id", ForeignKey("staff_functions.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
)

