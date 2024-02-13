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
    candidate_essay_type_id: Optional[str]
    candidate_id: str
    category_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageAnswerCreate(CandidateStageAnswerBase):
    candidate_stage_question_id: str
    sport_score: Optional[int]
    answer_id: Optional[str]


class CandidateStageListAnswerCreate(BaseModel):
    candidate_stage_answers: Optional[List[CandidateStageAnswerCreate]]


class CandidateStageAnswerUpdate(CandidateStageAnswerBase):
    candidate_stage_question_id: str


class CandidateStageQuestionRead(BaseModel):
    question: Optional[str]
    question_type: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageAnswerRead(CandidateStageAnswerBase):
    id: Optional[str]
    is_sport_passed: Optional[bool]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    candidate_stage_question_id: Optional[str]
    candidate_stage_question: Optional[CandidateStageQuestionRead]


class CandidateStageAnswerIdRead(BaseModel):
    id: Optional[str]
    type: Optional[str]
