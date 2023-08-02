from sqlalchemy import Column, TIMESTAMP, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class UserOath(Model):

    __tablename__ = "user_oaths"

    date = Column('oath_date', TIMESTAMP(timezone=True), nullable=True)
    user_id = Column(String(), ForeignKey("users.id"))
    military_unit_id = Column(
        String(),
        ForeignKey("military_units.id"))

    military_unit = relationship("MilitaryUnit", back_populates="user_oaths")
