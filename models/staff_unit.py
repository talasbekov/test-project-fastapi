from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import isActiveModel
from .association import staff_unit_function, staff_unit_candidate_stage_infos, hr_vacancy_hr_vacancy_candidates


class StaffUnit(isActiveModel):

    __tablename__ = "staff_units"

    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=False)
    staff_division_id = Column(
        UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=False
    )   

    position = relationship("Position", cascade="all,delete", foreign_keys=[position_id])
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
    candidate_stage_infos = relationship(
        "CandidateStageInfo",
        secondary=staff_unit_candidate_stage_infos,
        back_populates="staff_unit_coordinate_ids",
        cascade="all,delete",
    )
    hr_vacancies = relationship(
        "HrVacancy",
        secondary=hr_vacancy_hr_vacancy_candidates,
        back_populates="hr_vacancy_candidates",
    )
