from sqlalchemy import TEXT, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base


class PositionGroup(Base):

    __tablename__ = "position_groups"

    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), primary_key=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), primary_key=True)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    description = Column(TEXT, nullable=True)

    group = relationship("Group", back_populates="positions", cascade="all,delete", uselist=False)
    position = relationship("Position", back_populates="groups", cascade="all,delete", uselist=False)
    user = relationship("User", cascade="all,delete", foreign_keys=assigned_to)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
