from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import isActiveModel
from .association import hr_vacancy_hr_vacancy_requirements

class HrVacancy(isActiveModel):
    __tablename__ = "hr_vacancies"
    
    staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("staff_units.id"), nullable=True)
    archive_staff_unit_id = Column(UUID(as_uuid=True), ForeignKey("archive_staff_units.id"), nullable=True)
    
    hr_vacancy_requirements = relationship(
        "HrVacancyRequirements",
        secondary=hr_vacancy_hr_vacancy_requirements,
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
