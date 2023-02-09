import uuid
import enum

from sqlalchemy import TIMESTAMP, Column, String, text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSON, TEXT
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
    desciption = Column(TEXT)
    children = relationship("Group")
    users = relationship("User", back_populates="group", cascade ="all,delete")
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
