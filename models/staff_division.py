import enum
import uuid

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import backref, relationship

from core import Base
from models import TimeBaseModel


class GroupName(enum.Enum):
    DEPARTMENT = 1
    MANAGEMENT = 2
    TEAM = 3


class StaffDivision(TimeBaseModel, Base):

    __tablename__ = "staff_divisions"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
    name = Column(String(255))
    description = Column(TEXT)
    children = relationship("StaffDivision")
    users = relationship("User", back_populates="staff_division", cascade="all,delete")
