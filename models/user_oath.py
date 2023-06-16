from sqlalchemy import Column, TIMESTAMP, UUID, ForeignKey
from sqlalchemy.orm import relationship

from models import Model


class UserOath(Model):

    __tablename__ = "user_oaths"

    date = Column(TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    military_unit_id = Column(
        UUID(
            as_uuid=True),
        ForeignKey("military_units.id"))

    military_unit = relationship("MilitaryUnit", back_populates="user_oaths")
