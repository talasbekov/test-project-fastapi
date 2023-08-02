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


class StaffUnitHrVacancyRead(HrVacancyBase, ReadModel):
    is_active: Optional[bool]
    hr_vacancy_requirements: Optional[List[HrVacancyRequirementsRead]]
    candidates: Optional[List[HrVacancyCandidateRead]]
    is_responded: Optional[bool]

class HrVacancyRead(HrVacancyBase, ReadModel):
    staff_unit_id: Optional[uuid.UUID]
    archive_staff_unit_id: Optional[uuid.UUID]
    is_active: Optional[bool]
    hr_vacancy_requirements: Optional[List[HrVacancyRequirementsRead]]
    staff_unit: Optional[StaffUnitRead]
    archive_staff_unit: Optional[StaffUnitRead]
    candidates: Optional[List[HrVacancyCandidateRead]]
    is_responded: Optional[bool]


    class Config:
        orm_mode = True

    def to_dict(self, is_responded) -> dict:
        return {
            "id": self.id,
            "staff_unit_id": self.staff_unit_id,
            "archive_staff_unit_id": self.archive_staff_unit_id,
            "is_active": self.is_active,
            "hr_vacancy_requirements": self.hr_vacancy_requirements,
            "staff_unit": self.staff_unit,
            "archive_staff_unit": self.archive_staff_unit,
            "candidates": self.candidates,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            "is_responded": is_responded,
        }


class HrVacancyStaffDivisionRead(Model):
    id: Optional[uuid.UUID]
    staff_division_number: Optional[int]
    type_id: Optional[uuid.UUID]
    type: Optional[StaffDivisionTypeRead]
    vacancies: Optional[List[HrVacancyRead]]
