import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel, validator

from models import CandidateStatusEnum
from .candidate_essay_type import CandidateEssayTypeRead


class CandidateBase(BaseModel):
    staff_unit_curator_id: str
    staff_unit_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateUserRead(BaseModel):
    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]

    class Config:
        orm_mode = True


class StaffUnitCandidateRead(BaseModel):
    id: str
    users: Optional[List[CandidateUserRead]] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(CandidateBase):
    staff_unit_curator_id: Optional[str]
    staff_unit_id: Optional[str]
    status: Optional[str]
    debarment_reason: Optional[str]
    is_physical_passed: Optional[bool]
    recommended_by: Optional[str]

    @validator('debarment_reason', pre=True)
    def validate_debarment_reason(cls, value, values):
        status = values.get('status')
        if status == CandidateStatusEnum.ACTIVE and value is not None:
            raise ValueError(
                'debarment_reason должен быть пустым для статуса Активный')
        elif status == CandidateStatusEnum.DRAFT and value is None:
            raise ValueError(
                'debarment_reason обязателен для статуса Черновик')
        return value


class CandidateEssayUpdate(BaseModel):
    essay_id: Optional[str]
    name: Optional[str]
    nameKZ: Optional[str]


class CandidateRead(CandidateBase):
    id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    status: Optional[str]
    is_physical_passed: Optional[bool]
    attempt_number: Optional[int]
    debarment_reason: Optional[str]
    progress: Optional[int]
    current_stage: Optional[str]
    essay_id: Optional[str]
    essay: Optional[CandidateEssayTypeRead]
    last_edit_date: Optional[datetime.date]
    staff_unit_curator_id: Optional[str]
    staff_unit_curator: Optional[StaffUnitCandidateRead]
    staff_unit_id: Optional[str]
    staff_unit: Optional[StaffUnitCandidateRead]
    recommended_by: Optional[str]
    recommended_by_user: Optional[CandidateUserRead]
