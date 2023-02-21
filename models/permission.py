import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base

from .association import user_permissions


class Permission(Base):

    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String(150), nullable=True)
    users = relationship(
        "User",
        secondary=user_permissions,
        back_populates="permissions",
        cascade="all,delete"
    )
