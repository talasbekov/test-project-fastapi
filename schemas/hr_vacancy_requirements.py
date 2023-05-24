import uuid
from typing import Optional

from schemas import NamedModel, ReadNamedModel


class HrVacancyRequirementsBase(NamedModel):
    pass


class HrVacancyRequirementsCreate(HrVacancyRequirementsBase):
    pass


class HrVacancyRequirementsUpdate(HrVacancyRequirementsBase):
    pass


class HrVacancyRequirementsRead(HrVacancyRequirementsBase, ReadNamedModel):

    class Config:
        orm_mode = True
