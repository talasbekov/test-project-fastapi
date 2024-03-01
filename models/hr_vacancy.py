from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import isActiveModel
from .association import hr_v_hr_vacancy_req


class HrVacancy(isActiveModel):
    __tablename__ = "hr_erp_hr_vacancies"

    staff_unit_id = Column(
        String(),
        ForeignKey("hr_erp_staff_units.id"),
        nullable=True)
    archive_staff_unit_id = Column(
        String(),
        ForeignKey("hr_erp_archive_staff_units.id"),
        nullable=True)

    hr_vacancy_requirements = relationship(
        "HrVacancyRequirements",
        secondary=hr_v_hr_vacancy_req,
        back_populates="hr_vacancies"
    )
    candidates = relationship(
        "HrVacancyCandidate",
        back_populates="hr_vacancy"
    )
    staff_unit = relationship(
        "StaffUnit",
        back_populates="hr_vacancy"
    )
    archive_staff_unit = relationship(
        "ArchiveStaffUnit",
        back_populates="hr_vacancy"
    )
