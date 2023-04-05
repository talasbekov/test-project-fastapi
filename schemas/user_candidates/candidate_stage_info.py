import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from .candidate_stage_type import CandidateStageTypeRead


class CandidateStageInfoBase(BaseModel):
    candidate_id: uuid.UUID
    candidate_stage_type_id: uuid.UUID
    staff_unit_coordinate_id: uuid.UUID
    is_waits: Optional[bool]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageInfoCreate(CandidateStageInfoBase):
    pass


class CandidateStageInfoUpdate(CandidateStageInfoBase):
    pass


class CandidateStageInfoRead(CandidateStageInfoBase):
    id: Optional[uuid.UUID]
    status: Optional[str]
    candidate_id: Optional[uuid.UUID]
    staff_unit_coordinate_id: Optional[uuid.UUID]
    candidate_stage_type_id: Optional[uuid.UUID]
    candidate_stage_type: Optional[CandidateStageTypeRead]
    date_sign: Optional[datetime.date]
