from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from .association import staff_unit_function


class StaffUnit(Model):

    __tablename__ = "staff_units"

    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=False)
    staff_division_id = Column(
        UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=False
    )   

    position = relationship("Position", cascade="all,delete")
    staff_division = relationship(
        "StaffDivision", back_populates="staff_units", foreign_keys=[staff_division_id]
    )

    users = relationship("User", back_populates="staff_unit", foreign_keys="User.staff_unit_id")
    actual_users = relationship(
        "User", back_populates="actual_staff_unit", foreign_keys="User.actual_staff_unit_id"
    )
    staff_functions = relationship(
        "StaffFunction",
        secondary=staff_unit_function,
        back_populates="staff_units",
        cascade="all,delete",
    )
