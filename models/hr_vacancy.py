from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model
from .association import hr_vacancy_hr_vacancy_requirements, hr_vacancy_hr_vacancy_candidates

class HrVacancy(Model):
    __tablename__ = "hr_vacancies"
    
    position_id = Column(UUID(as_uuid=True), ForeignKey("positions.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    staff_division_id = Column(UUID(as_uuid=True), ForeignKey("staff_divisions.id"), nullable=False)
    
    hr_vacancy_requirements = relationship(
        "HrVacancyRequirements",
        secondary=hr_vacancy_hr_vacancy_requirements,
        back_populates="hr_vacancies",
    )
    hr_vacancy_candidates = relationship(
        "StaffUnit",
        secondary=hr_vacancy_hr_vacancy_candidates,
        back_populates="hr_vacancies",
        cascade="all,delete"
    )
    position = relationship("Position", cascade="all,delete")
    staff_division = relationship("StaffDivision", cascade="all,delete")
