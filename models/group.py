import enum
import uuid

from sqlalchemy import TIMESTAMP, Column, Enum, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TEXT, UUID
from sqlalchemy.orm import backref, relationship

from core import Base


class GroupName(enum.Enum):
    DEPARTMENT = 1
    MANAGEMENT = 2
    TEAM = 3


class Group(Base):
    
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    parent_group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=True)
    name = Column(String(255))
    description = Column(TEXT)
    children = relationship("Group")
    users = relationship("User", back_populates="group", cascade="all,delete")

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
