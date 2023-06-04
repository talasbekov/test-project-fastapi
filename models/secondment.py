from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import NamedModel


class Secondment(NamedModel):

    __tablename__ = "secondments"

    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"))
    staff_division = relationship("StaffDivision")

    state_body_id = Column(UUID(as_uuid=True), ForeignKey("state_bodies.id"))
    state_body = relationship("StateBody")

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="secondments")
