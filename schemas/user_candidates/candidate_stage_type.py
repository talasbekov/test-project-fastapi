import uuid, datetime
from typing import Optional, List

from pydantic import BaseModel

from .candidate_stage_question import CandidateStageQuestionRead
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class CandidateStageTypeBase(NamedModel):

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        

class CandidateStageTypeCreate(CandidateStageTypeBase):
    pass


class CandidateStageTypeUpdate(CandidateStageTypeBase):
    pass


class CandidateStageTypeRead(CandidateStageTypeBase, ReadNamedModel):
    candidate_stage_questions: Optional[List[CandidateStageQuestionRead]]
