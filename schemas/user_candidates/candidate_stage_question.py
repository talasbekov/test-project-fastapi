import uuid
from typing import Optional, List

from pydantic import BaseModel

from .candidate_stage_answer import CandidateStageAnswerRead


class CandidateStageQuestionBase(BaseModel):
    question: Optional[str]
    question_type: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class CandidateStageQuestionCreate(CandidateStageQuestionBase):
    candidate_stage_type_id: Optional[uuid.UUID]


class CandidateStageQuestionUpdate(CandidateStageQuestionBase):
    candidate_stage_type_id: Optional[uuid.UUID]


class CandidateStageQuestionRead(CandidateStageQuestionBase):
    id: Optional[uuid.UUID]
    candidate_stage_type_id: Optional[uuid.UUID]
    candidate_stage_answers: Optional[List[CandidateStageAnswerRead]]
