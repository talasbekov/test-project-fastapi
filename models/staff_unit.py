from sqlalchemy import Column, ForeignKey, ARRAY, String
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.orm import relationship

from models import isActiveModel
from .association import staff_unit_function, staff_unit_candidate_stage_infos


class StaffUnit(isActiveModel):

    __tablename__ = "staff_units"

    # Properties
    requirements = Column(ARRAY(CLOB), nullable=True)
    position_id = Column(
        String(),
        ForeignKey("positions.id"),
        nullable=False)
    staff_division_id = Column(
        String(),
        ForeignKey("staff_divisions.id"),
        nullable=True)
    user_replacing_id = Column(
        String(),
        ForeignKey("users.id"),
        nullable=True)
    curator_of_id = Column(
        String(),
        ForeignKey("staff_divisions.id", ondelete='SET NULL'),
        nullable=True)

    # Relationships
    position = relationship(
        "Position",
        cascade="all,delete",
        foreign_keys=[position_id],
        lazy="joined")
    staff_division = relationship(
        "StaffDivision", 
        back_populates="staff_units", 
        foreign_keys=[staff_division_id],
        lazy="joined"
    )
    users = relationship(
        "User",
        back_populates="staff_unit",
        foreign_keys="User.staff_unit_id")
    actual_users = relationship(
        "User",
        back_populates="actual_staff_unit",
        foreign_keys="User.actual_staff_unit_id"
    )
    user_replacing = relationship(
        "User",
        back_populates="staff_unit_replacing",
        foreign_keys=user_replacing_id)
    staff_functions = relationship(
        "StaffFunction",
        secondary=staff_unit_function,
        back_populates="staff_units",
        lazy="joined"
    )
    candidate_stage_infos = relationship(
        "CandidateStageInfo",
        secondary=staff_unit_candidate_stage_infos,
        back_populates="staff_unit_coordinate_ids",
        cascade="all,delete",
        lazy="joined"
    )
    hr_vacancy = relationship(
        "HrVacancy",
        back_populates="staff_unit",
        cascade="all,delete",
        lazy="joined"
    )
    courted_group = relationship(
        "StaffDivision",
        back_populates="curators",
        foreign_keys=[curator_of_id],
        lazy="joined"
    )
