from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship

from models import Model, NamedModel
from .association import users_badges

class BadgeType(NamedModel):
    __tablename__ = "badge_types"

    badges = relationship("Badge", back_populates="badge_type")


class Badge(Model):

    __tablename__ = "badges"

    url = Column(String, nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    badge_type_id = Column(UUID(as_uuid=True), ForeignKey("badge_types.id"))
    badge_type = relationship("BadgeType", back_populates="badges")

    users = relationship(
        "User",
        secondary=users_badges,
        back_populates='badges',
        cascade="all,delete"
    )
