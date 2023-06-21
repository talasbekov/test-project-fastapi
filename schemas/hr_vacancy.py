import uuid
from typing import Optional, List

from schemas import (Model, ReadModel, HrVacancyRequirementsRead,
                     HrVacancyCandidateRead, StaffDivisionTypeRead)
from .staff_unit import StaffUnitRead


class HrVacancyBase(Model):
    staff_unit_id: uuid.UUID
    is_active: bool


class HrVacancyCreate(HrVacancyBase):
    hr_vacancy_requirements_ids: Optional[List[uuid.UUID]]


class HrVacancyUpdate(HrVacancyBase):
    staff_unit_id: Optional[uuid.UUID]
    archive_staff_unit_id: Optional[uuid.UUID]
    hr_vacancy_requirements_ids: Optional[List[uuid.UUID]]
    is_active: Optional[bool]


class HrVacancyRead(HrVacancyBase, ReadModel):
    staff_unit_id: Optional[uuid.UUID]
    archive_staff_unit_id: Optional[uuid.UUID]
    is_active: Optional[bool]
    hr_vacancy_requirements: Optional[List[HrVacancyRequirementsRead]]
    staff_unit: Optional[StaffUnitRead]
    archive_staff_unit: Optional[StaffUnitRead]
    candidates: Optional[List[HrVacancyCandidateRead]]

    class Config:
        orm_mode = True


class HrVacancyStaffDivisionRead(Model):
    id: Optional[uuid.UUID]
    staff_division_number: Optional[int]
    type_id: Optional[uuid.UUID]
    type: Optional[StaffDivisionTypeRead]
    vacancies: Optional[List[HrVacancyRead]]
