import uuid
from typing import Optional

from schemas import Model, ReadModel, UserRead


class HrVacancyCandidateBase(Model):
    user_id: uuid.UUID
    hr_vacancy_id: uuid.UUID


class HrVacancyCandidateRead(HrVacancyCandidateBase, ReadModel):
    user_id: Optional[uuid.UUID]
    hr_vacancy_id: Optional[uuid.UUID]
    user: Optional[UserRead]

    class Config:
        orm_mode = True
