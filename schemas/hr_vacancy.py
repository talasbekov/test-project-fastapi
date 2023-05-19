import uuid
from typing import Optional, List

from schemas import Model, ReadModel
from .hr_vacancy_requirements import HrVacancyRequirementsRead
from .position import PositionRead
from .staff_division import StaffDivisionRead
from .staff_unit import StaffUnitRead


class HrVacancyBase(Model):
    position_id: uuid.UUID
    staff_division_id: uuid.UUID
    

class HrVacancyCreate(HrVacancyBase):
    hr_vacancy_requirements_ids: Optional[List[uuid.UUID]]


class HrVacancyUpdate(HrVacancyBase):
    is_active: Optional[bool]
    hr_vacancy_requirements_ids: Optional[List[uuid.UUID]]


class HrVacancyRead(HrVacancyBase, ReadModel):
    position_id: Optional[uuid.UUID]
    staff_division_id: Optional[uuid.UUID]
    is_active: Optional[bool]
    hr_vacancy_requirements: Optional[List[HrVacancyRequirementsRead]]
    position: Optional[PositionRead]
    staff_division: Optional[StaffDivisionRead]
    hr_vacancy_candidates: Optional[StaffUnitRead]
    
    class Config:
        orm_mode = True
