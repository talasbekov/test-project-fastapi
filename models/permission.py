import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from core import Base


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=True, default=uuid.uuid4)
    name = Column(String(150), nullable=True)
    positions = relationship("Position", secondary="position_permission_table",
                            back_populates="permissions")
