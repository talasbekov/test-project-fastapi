import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from core import Base
from models import TimeBaseModel
from .association import users_badges


class Badge(TimeBaseModel, Base):

    __tablename__ = "badges"

    id = Column(UUID(as_uuid=True), primary_key=True,
                nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    url = Column(String, nullable=True)

    users = relationship(
        "User",
        secondary=users_badges,
        back_populates='badges',
        cascade="all,delete"
    )
