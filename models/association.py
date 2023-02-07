from sqlalchemy import Table, Column, ForeignKey, String

from core import Base


position_permission_table = Table(
    "position_permission_table",
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
