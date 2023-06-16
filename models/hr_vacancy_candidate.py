from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models import Model


class HrVacancyCandidate(Model):
    __tablename__ = "hr_vacancy_candidates"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    hr_vacancy_id = Column(UUID(as_uuid=True), ForeignKey("hr_vacancies.id"))

    user = relationship(
        "User",
        back_populates="hr_vacancies"
    )
    hr_vacancy = relationship(
        "HrVacancy",
        back_populates="candidates"
    )
