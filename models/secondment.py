from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import NamedModel


class Secondment(NamedModel):

    __tablename__ = "secondments"

    staff_division_id = Column(
        String(),
        ForeignKey("staff_divisions.id"))
    staff_division = relationship("StaffDivision")

    state_body_id = Column(String(), ForeignKey("state_bodies.id"))
    state_body = relationship("StateBody")

    user_id = Column(String(), ForeignKey("users.id"))
    user = relationship("User", back_populates="secondments")
