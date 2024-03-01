import uuid
import datetime
from typing import Optional, List

from pydantic import BaseModel
from .candidate_stage_answer import CandidateStageAnswerRead
from schemas import ReadNamedModel


class CandidateStageQuestionBase(BaseModel):
    question: str
    question_type: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageQuestionCreate(CandidateStageQuestionBase):
    candidate_stage_type_id: Optional[str]


class CandidateStageQuestionUpdate(CandidateStageQuestionBase):
    candidate_stage_type_id: Optional[str]


class CandidateStageQuestionRead(CandidateStageQuestionBase):
    id: Optional[str]
    candidate_stage_type_id: Optional[str]
    question: Optional[str]
    question_type: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class CandidateStageQuestionReadIn(BaseModel):
    id: Optional[str]
    answer: Optional[CandidateStageAnswerRead]
    question: Optional[str]
    question_type: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageInfoReadAnswer(BaseModel):
    id: Optional[str]
    status: Optional[str]
    date_sign: Optional[datetime.date]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    is_waits: Optional[bool]
    candidate_stage_type_id: Optional[str]
    staff_unit_coordinate_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageQuestionType(ReadNamedModel):
    questions: Optional[List[CandidateStageQuestionReadIn]]
    candidate_stage_info: Optional[CandidateStageInfoReadAnswer]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
