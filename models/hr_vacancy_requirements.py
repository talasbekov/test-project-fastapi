from sqlalchemy.orm import relationship

from models import NamedModel
from .association import hr_vacancy_hr_vacancy_requirements

class HrVacancyRequirements(NamedModel):
    __tablename__ = "hr_vacancies_requirements"
    
    hr_vacancies = relationship(
        "HrVacancy",
        secondary=hr_vacancy_hr_vacancy_requirements,
        back_populates="hr_vacancy_requirements"
    )