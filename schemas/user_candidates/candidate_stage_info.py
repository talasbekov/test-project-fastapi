from typing import Optional
import uuid
from pydantic import BaseModel
from typing import Any
# import date
from datetime import datetime
from .candidate_stage_question import CandidateStageQuestionRead

class CandidateStageInfoBase(BaseModel):
    status: Optional[str]
    date_sign: Optional[datetime]
    candidate_stage_type_id: Optional[uuid.UUID]
    candidate_stage_id : Optional[uuid.UUID]
    staff_unit_coordinate_id: Optional[uuid.UUID]
    is_waits: Optional[bool]
    
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class CandidateStageInfoCreate(CandidateStageInfoBase):
    pass


class CandidateStageInfoUpdate(CandidateStageInfoBase):
    pass


class CandidateStageInfoRead(CandidateStageInfoBase):
    date_sign: Optional[Any]
    id: Optional[uuid.UUID] 
