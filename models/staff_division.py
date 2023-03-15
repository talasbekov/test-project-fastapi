import enum
import uuid

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, text, Boolean
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import backref, relationship

from core import Base
from models import NamedNestedModel


class GroupName(enum.Enum):
    DEPARTMENT = 1
    MANAGEMENT = 2
    TEAM = 3


class StaffDivision(NamedNestedModel, Base):

    __tablename__ = "staff_divisions"

    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
    description = Column(TEXT)
    is_combat_unit = Column(Boolean)

    children = relationship("StaffDivision")
    staff_units = relationship("StaffUnit", back_populates="staff_division")
