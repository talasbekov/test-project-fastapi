from sqlalchemy import Column, ForeignKey, ARRAY, String
from sqlalchemy.dialects.oracle import CLOB
from sqlalchemy.orm import relationship

from models import Model
from .association import (
    archive_staff_unit_function,
    archive_staff_unit_candidate_stage_infos
)

from enum import Enum as EnumBase


class FormEnum(EnumBase):
    form1 = "Форма 1"
    form2 = "Форма 2"
    form3 = "Форма 3"


class ArchiveStaffUnit(Model):

    __tablename__ = "archive_staff_units"

    requirements = Column(ARRAY(CLOB))

    # Properties
    position_id = Column(
        String(),
        ForeignKey("positions.id"),
        nullable=False)
    staff_division_id = Column(
        String(), ForeignKey("archive_staff_divisions.id"), nullable=False
    )
    user_id = Column(String(), ForeignKey("users.id"), nullable=True)
    curator_of_id = Column(
        String(),
        ForeignKey("staff_divisions.id", ondelete='SET NULL'),
        nullable=True)
    actual_user_id = Column(
        String(),
        ForeignKey("users.id"),
        nullable=True)
    origin_id = Column(
        String(),
        ForeignKey("staff_units.id"),
        nullable=True)
    user_replacing_id = Column(
        String(),
        ForeignKey("users.id"),
        nullable=True)
    user_replacing = relationship(
        "User",
        back_populates="archive_staff_unit_replacing",
        foreign_keys=user_replacing_id)
    # Relationships
    position = relationship(
        "Position",
        cascade="all,delete",
        foreign_keys=[position_id],
        passive_deletes=True)
    user = relationship("User", foreign_keys=user_id)
    actual_user = relationship("User", foreign_keys=actual_user_id)
    staff_division = relationship(
        "ArchiveStaffDivision",
        back_populates="staff_units",
        foreign_keys=[staff_division_id]
    )
    staff_functions = relationship(
        "ArchiveStaffFunction",
        secondary=archive_staff_unit_function,
        back_populates="staff_units",
    )
    candidate_stage_infos = relationship(
        "CandidateStageInfo",
        secondary=archive_staff_unit_candidate_stage_infos,
        back_populates="archive_staff_unit_coordinate_ids",
        cascade="all,delete",
    )
    hr_vacancy = relationship(
        "HrVacancy",
        back_populates="archive_staff_unit",
        cascade="all,delete"
    )
