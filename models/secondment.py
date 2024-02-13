from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import NamedModel


class Secondment(NamedModel):

    __tablename__ = "hr_erp_secondments"

    staff_division_id = Column(
        String(),
        ForeignKey("hr_erp_staff_divisions.id"))
    staff_division = relationship("StaffDivision")

    state_body_id = Column(String(), ForeignKey("hr_erp_state_bodies.id"))
    state_body = relationship("StateBody")

    user_id = Column(String(), ForeignKey("hr_erp_users.id"))
    user = relationship("User", back_populates="secondments")
