import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String, text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON
from sqlalchemy.orm import relationship, backref

from core import Base

class GroupName(enum.Enum):
    DEPARTMENT = "Департамент"
    MANAGEMENT = "Управление"
    TEAM = "Отдел"

class Group(Base):
    
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=True)
    name = Column(String(255))
    children = relationship("Group", backref=backref('children', remote_side=[id]))
