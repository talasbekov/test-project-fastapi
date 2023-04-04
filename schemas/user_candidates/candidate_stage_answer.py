import uuid
from typing import Optional

from pydantic import BaseModel

from .candidate_category import CandidateCategoryRead


class CandidateStageAnswerBase(BaseModel):
    candidate_stage_question_id: uuid.UUID
    type: Optional[str]
    answer_str: Optional[str]
    answer_bool: Optional[bool]
    answer: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    candidate_essay_type_id: Optional[uuid.UUID]
    candidate_id: uuid.UUID
    category_id: Optional[uuid.UUID]
    category: Optional[CandidateCategoryRead]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageAnswerCreate(CandidateStageAnswerBase):
    sport_score: Optional[int]

class CandidateStageListAnswerCreate(BaseModel):
    candidate_stage_answers: Optional[list[CandidateStageAnswerBase]]

class CandidateStageAnswerUpdate(CandidateStageAnswerBase):
    pass


class CandidateStageAnswerRead(CandidateStageAnswerBase):
    id: Optional[uuid.UUID]
    is_sport_passed: Optional[bool]

class CandidateStageAnswerIdRead(BaseModel):
    id: Optional[uuid.UUID]
    type: Optional[str]
