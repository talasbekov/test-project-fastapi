import uuid
import datetime
from typing import Optional, List

from pydantic import BaseModel


class CandidateStageAnswerBase(BaseModel):

    type: Optional[str]
    answer_str: Optional[str]
    answer_bool: Optional[bool]
    answer: Optional[str]
    document_link: Optional[str]
    document_number: Optional[str]
    candidate_essay_type_id: Optional[uuid.UUID]
    candidate_id: uuid.UUID
    category_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageAnswerCreate(CandidateStageAnswerBase):
    candidate_stage_question_id: uuid.UUID
    sport_score: Optional[int]
    answer_id: Optional[uuid.UUID]


class CandidateStageListAnswerCreate(BaseModel):
    candidate_stage_answers: Optional[List[CandidateStageAnswerCreate]]


class CandidateStageAnswerUpdate(CandidateStageAnswerBase):
    candidate_stage_question_id: uuid.UUID


class CandidateStageQuestionRead(BaseModel):
    question: Optional[str]
    question_type: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageAnswerRead(CandidateStageAnswerBase):
    id: Optional[uuid.UUID]
    is_sport_passed: Optional[bool]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    candidate_stage_question_id: Optional[uuid.UUID]
    candidate_stage_question: Optional[CandidateStageQuestionRead]


class CandidateStageAnswerIdRead(BaseModel):
    id: Optional[uuid.UUID]
    type: Optional[str]
