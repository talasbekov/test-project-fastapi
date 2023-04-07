import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel, validator

from models import CandidateStatusEnum
from .candidate_stage_info import CandidateStageInfoRead
from .candidate_essay_type import CandidateEssayTypeRead


class CandidateBase(BaseModel):
    staff_unit_curator_id: uuid.UUID
    staff_unit_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateUserRead(BaseModel):
    id: uuid.UUID
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]

    class Config:
        orm_mode = True


class StaffUnitCandidateRead(BaseModel):
    id: uuid.UUID
    users: Optional[List[CandidateUserRead]] = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
         

class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(CandidateBase):
    staff_unit_curator_id: Optional[uuid.UUID]
    staff_unit_id: Optional[uuid.UUID]
    status: Optional[str]
    debarment_reason: Optional[str]

    @validator('debarment_reason', pre=True)
    def validate_debarment_reason(cls, value, values):
        status = values.get('status')
        if status == CandidateStatusEnum.ACTIVE and value is not None:
            raise ValueError('debarment_reason должен быть пустым для статуса Активный')
        elif status == CandidateStatusEnum.DRAFT and value is None:
            raise ValueError('debarment_reason обязателен для статуса Черновик')
        return value


class CandidateEssayUpdate(BaseModel):
    essay_id: uuid.UUID


class CandidateRead(CandidateBase):
    id: Optional[uuid.UUID]
    status: Optional[str]
    debarment_reason: Optional[str]
    progress: Optional[int]
    current_stage: Optional[uuid.UUID]
    essay_id: Optional[uuid.UUID]
    essay: Optional[CandidateEssayTypeRead]
    last_edit_date: Optional[datetime.date]
    staff_unit_curator_id: Optional[uuid.UUID]
    staff_unit_curator: Optional[StaffUnitCandidateRead]
    staff_unit_id: Optional[uuid.UUID]
    staff_unit: Optional[StaffUnitCandidateRead]
    candidate_stage_infos: Optional[List[CandidateStageInfoRead]]
