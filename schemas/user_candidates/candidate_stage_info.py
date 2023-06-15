import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from .candidate_stage_type import CandidateStageTypeRead
from .candidate import CandidateRead

class CandidateStageInfoBase(BaseModel):
    candidate_id: uuid.UUID
    candidate_stage_type_id: uuid.UUID
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageInfoCreate(CandidateStageInfoBase):
    pass


class CandidateStageInfoUpdate(CandidateStageInfoBase):
    candidate_id: Optional[uuid.UUID]
    candidate_stage_type_id: Optional[uuid.UUID]
    status: Optional[str]


class CandidateStageInfoSendToApproval(BaseModel):
    staff_unit_coordinate_id: Optional[uuid.UUID]


class CandidateStageInfoRead(CandidateStageInfoBase):
    id: Optional[uuid.UUID]
    access: Optional[bool]
    status: Optional[str]
    candidate_id: Optional[uuid.UUID]
    candidate: Optional[CandidateRead]
    is_waits: Optional[bool]
    candidate_stage_type_id: Optional[uuid.UUID]
    candidate_stage_type: Optional[CandidateStageTypeRead]
    date_sign: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
