import enum
import uuid

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import backref, relationship

from core import Base
from models import NamedModel


class GroupName(enum.Enum):
    DEPARTMENT = 1
    MANAGEMENT = 2
    TEAM = 3


class StaffDivision(NamedModel, Base):

    __tablename__ = "staff_divisions"

    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
    description = Column(TEXT)
    children = relationship("StaffDivision")
    users = relationship("User", back_populates="staff_division", cascade="all,delete")
