import uuid

from sqlalchemy import TEXT, Column, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship

from core import Base
from models import Model

from .association import staff_unit_function


class StaffUnit(Model, Base):

    __tablename__ = "staff_units"

    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=False)
    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=False)

<<<<<<< HEAD
    staff_functions = relationship("StaffFunction",
                                   secondary=staff_unit_function)
=======
>>>>>>> 6c110be17855d7b804a09a64d79da1637d155bfa
    position = relationship("Position", cascade="all,delete")
    staff_division = relationship("StaffDivision", back_populates="staff_units", cascade="all,delete")

    users = relationship("User", back_populates="staff_unit", foreign_keys='User.staff_unit_id')
    actual_users = relationship("User", back_populates="actual_staff_unit", foreign_keys='User.actual_staff_unit_id')
<<<<<<< HEAD
=======

    staff_functions = relationship(
        "StaffFunction",
        secondary=staff_unit_function,
        back_populates='staff_units',
        cascade="all,delete"
    )
>>>>>>> 6c110be17855d7b804a09a64d79da1637d155bfa
