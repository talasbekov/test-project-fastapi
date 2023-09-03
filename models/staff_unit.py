import json

from sqlalchemy import Column, ForeignKey, ARRAY, String
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from models import isActiveModel
from .association import staff_unit_function, s_u_cand_stage_infos


class StaffUnit(isActiveModel):

    __tablename__ = "hr_erp_staff_units"

    # Properties
    requirements = Column(ARRAY(CLOB), nullable=True)
    position_id = Column(
        String(),
        ForeignKey("hr_erp_positions.id"),
        nullable=False)
    staff_division_id = Column(
        String(),
        ForeignKey("hr_erp_staff_divisions.id"),
        nullable=True)
    user_replacing_id = Column(
        String(),
        ForeignKey("hr_erp_users.id"),
        nullable=True)
    curator_of_id = Column(
        String(),
        ForeignKey("hr_erp_staff_divisions.id", ondelete='SET NULL'),
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
        secondary=s_u_cand_stage_infos,
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

@listens_for(StaffUnit, 'before_update')
def description_set_listener(mapper, connection, target):
    if isinstance(target.requirements, list):
        target.requirements = json.dumps(target.requirements)