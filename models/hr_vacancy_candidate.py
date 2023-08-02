from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import Model


class HrVacancyCandidate(Model):
    __tablename__ = "hr_vacancy_candidates"

    user_id = Column(String(), ForeignKey("users.id"))
    hr_vacancy_id = Column(String(), ForeignKey("hr_vacancies.id"))

    user = relationship(
        "User",
        back_populates="hr_vacancies"
    )
    hr_vacancy = relationship(
        "HrVacancy",
        back_populates="candidates"
    )
