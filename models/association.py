from sqlalchemy import Table, Column, ForeignKey, String

from core import Base


position_permission = Table(
    "position_permission",
    Base.metadata,
    Column("position_id", ForeignKey("positions.id")),
    Column("permission_id", ForeignKey("permissions.id")),
)

users_badges = Table(
    "users_badges",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("badge_id", ForeignKey("badges.id"))
)

hr_document_equipment = Table(
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
