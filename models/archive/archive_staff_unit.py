from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from .association import archive_staff_unit_function


class ArchiveStaffUnit(Model):

    __tablename__ = "archive_staff_units"

    # Properties
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=False)
    staff_division_id = Column(
        UUID(as_uuid=True), ForeignKey("archive_staff_divisions.id"), nullable=False
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    actual_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    origin_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)

    # Relationships
    position = relationship("Position")
    staff_division = relationship(
        "ArchiveStaffDivision", back_populates="staff_units", foreign_keys=[staff_division_id]
    )
    staff_functions = relationship(
        "ArchiveStaffFunction",
        secondary=archive_staff_unit_function,
        back_populates="staff_units",
    )
    user = relationship("User", foreign_keys=user_id)
    actual_user = relationship("User", foreign_keys=actual_user_id)
