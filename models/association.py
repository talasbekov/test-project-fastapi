# Built library
import enum

from sqlalchemy import Table, Column, ForeignKey, String

from core import Base


users_badges = Table(
    "users_badges",
    Base.metadata,
    Column("user_id", ForeignKey("users.id")),
    Column("badge_id", ForeignKey("badges.id"))
)