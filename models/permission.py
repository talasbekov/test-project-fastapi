import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel

from .association import user_permissions


class Permission(NamedModel, Base):

    __tablename__ = "permissions"

    users = relationship(
        "User",
        secondary=user_permissions,
        back_populates="permissions",
        cascade="all,delete"
    )
