from __future__ import annotations
from typing import List

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from core import Base


class PositionPermission(Base):
    pass


position_permission_table = Table(
    "position_permission_table",
    Base.metadata,
    Column("position_id", ForeignKey("positions.id")),
    Column("permission_id", ForeignKey("permissions.id")),
)


class PositionId(PositionPermission):
    __tablename__ = "position_id"

    id: Mapped[str] = Column(primary_key=True)
    permission_id: Mapped[List[PermissionId]] = relationship(secondary=position_permission_table)


class PermissionId(PositionPermission):
    __tablename__ = "permission_id"

    id: Mapped[str] = Column(primary_key=True)
    position_id: Mapped[List[PositionId]] = relationship(secondary=position_permission_table)
