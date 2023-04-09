import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from .candidate_stage_type import CandidateStageTypeRead
from .candidate import CandidateRead
from schemas import StaffUnitRead


class CandidateStageInfoBase(BaseModel):
    candidate_id: uuid.UUID
    candidate_stage_type_id: uuid.UUID
    staff_unit_coordinate_id: Optional[uuid.UUID]
    is_waits: Optional[bool]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageInfoCreate(CandidateStageInfoBase):
    pass


class CandidateStageInfoUpdate(CandidateStageInfoBase):
    candidate_id: Optional[uuid.UUID]
    candidate_stage_type_id: Optional[uuid.UUID]
    status: Optional[str]


class CandidateStageInfoRead(CandidateStageInfoBase):
    id: Optional[uuid.UUID]
    status: Optional[str]
    candidate_id: Optional[uuid.UUID]
    candidate: Optional[CandidateRead]
    staff_unit_coordinate_id: Optional[uuid.UUID]
    staff_unit_coordinate: Optional[StaffUnitRead]
    candidate_stage_type_id: Optional[uuid.UUID]
    candidate_stage_type: Optional[CandidateStageTypeRead]
    date_sign: Optional[datetime.date]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
