from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model, NamedModel

class BadgeType(NamedModel):
    __tablename__ = "badge_types"

    url = Column(String, nullable=True)

    badges = relationship("Badge", back_populates="type")


class Badge(Model):

    __tablename__ = "badges"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    type_id = Column(UUID(as_uuid=True), ForeignKey("badge_types.id"))
    type = relationship("BadgeType", back_populates="badges")
    user = relationship("User", back_populates='badges')

    history = relationship("BadgeHistory", back_populates="badge", uselist=False)
