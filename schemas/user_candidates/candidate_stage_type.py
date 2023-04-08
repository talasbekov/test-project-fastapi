import uuid, datetime
from typing import Optional, List

from pydantic import BaseModel

from .candidate_stage_question import CandidateStageQuestionRead


class CandidateStageTypeBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        

class CandidateStageTypeCreate(CandidateStageTypeBase):
    pass


class CandidateStageTypeUpdate(CandidateStageTypeBase):
    pass


class CandidateStageTypeRead(CandidateStageTypeBase):
    id: Optional[uuid.UUID]
    candidate_stage_questions: Optional[List[CandidateStageQuestionRead]]
    name: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
