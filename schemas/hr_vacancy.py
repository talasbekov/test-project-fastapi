import uuid
from typing import Optional, List

from schemas import Model, ReadModel
from .hr_vacancy_requirements import HrVacancyRequirementsRead
from .staff_unit import StaffUnitRead
from .user import UserRead


class HrVacancyBase(Model):
    staff_unit_id: uuid.UUID


class HrVacancyCreate(HrVacancyBase):
    hr_vacancy_requirements_ids: Optional[List[uuid.UUID]]


class HrVacancyUpdate(HrVacancyBase):
    hr_vacancy_requirements_ids: Optional[List[uuid.UUID]]
    

class HrVacancyStaffDivision(Model):
    staff_division_ids: List[uuid.UUID]


class HrVacancyRead(HrVacancyBase, ReadModel):
    staff_unit_id: Optional[uuid.UUID]
    is_active: Optional[bool]
    hr_vacancy_requirements: Optional[List[HrVacancyRequirementsRead]]
    staff_unit: Optional[StaffUnitRead]
    hr_vacancy_candidates: Optional[List[UserRead]]
    
    class Config:
        orm_mode = True


class HrVacancyStaffDivisionRead(Model):
    id: uuid.UUID
    name: str
    vacancies: List[HrVacancyRead]
