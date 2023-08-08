from sqlalchemy.orm import relationship

from models import NamedModel
from .association import hr_v_hr_vacancy_req


class HrVacancyRequirements(NamedModel):
    __tablename__ = "hr_erp_hr_vac_req"

    hr_vacancies = relationship(
        "HrVacancy",
        secondary=hr_v_hr_vacancy_req,
        back_populates="hr_vacancy_requirements"
    )
