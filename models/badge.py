from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models import NamedModel
from .association import users_badges


class Badge(NamedModel):

    __tablename__ = "badges"

    url = Column(String, nullable=True)

    users = relationship(
        "User",
        secondary=users_badges,
        back_populates='badges',
        cascade="all,delete"
    )
