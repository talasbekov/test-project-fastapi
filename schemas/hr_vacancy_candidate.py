import uuid
from typing import Optional

from schemas import Model, ReadModel, UserRead


class HrVacancyCandidateBase(Model):
    user_id: str
    hr_vacancy_id: str


class HrVacancyCandidateRead(HrVacancyCandidateBase, ReadModel):
    user_id: Optional[str]
    hr_vacancy_id: Optional[str]
    user: Optional[UserRead]

    class Config:
        orm_mode = True
