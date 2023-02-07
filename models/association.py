from __future__ import annotations
from typing import List

from sqlalchemy import Table, Column, ForeignKey

from core import Base


class PositionPermission(Base):
    pass


position_permission_table = Table(
    "position_permission_table",
    Base.metadata,
    Column("position_id", ForeignKey("positions.id")),
    Column("permission_id", ForeignKey("permissions.id")),
)
