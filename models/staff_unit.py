from sqlalchemy import Column, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship

from models import isActiveModel
from .association import staff_unit_function, staff_unit_candidate_stage_infos

class StaffUnit(isActiveModel):

    __tablename__ = "staff_units"

    # Properties
    requirements = Column(ARRAY(JSON(none_as_null=True)))
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=False)
    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
    user_replacing_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    curator_of_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=True)
    
    # Relationships
    position = relationship("Position", cascade="all,delete", foreign_keys=[position_id])
    staff_division = relationship(
        "StaffDivision", back_populates="staff_units", foreign_keys=[staff_division_id]
    )
    users = relationship("User", back_populates="staff_unit", foreign_keys="User.staff_unit_id")
    actual_users = relationship(
        "User", back_populates="actual_staff_unit", foreign_keys="User.actual_staff_unit_id"
    )
    user_replacing = relationship("User", back_populates="staff_unit_replacing", foreign_keys=user_replacing_id)
    staff_functions = relationship(
        "StaffFunction",
        secondary=staff_unit_function,
        back_populates="staff_units",
    )
    candidate_stage_infos = relationship(
        "CandidateStageInfo",
        secondary=staff_unit_candidate_stage_infos,
        back_populates="staff_unit_coordinate_ids",
        cascade="all,delete",
    )
    hr_vacancy = relationship(
        "HrVacancy",
        back_populates="staff_unit",
        cascade="all,delete"
    )
    courted_group = relationship(
        "StaffDivision",
        back_populates="curators",
        foreign_keys=[curator_of_id],
    )
