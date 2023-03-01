import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import NamedModel

from .association import users_badges


class Badge(NamedModel, Base):

    __tablename__ = "badges"

    url = Column(String, nullable=True)

    users = relationship(
        "User",
        secondary=users_badges,
        back_populates='badges',
        cascade="all,delete"
    )
