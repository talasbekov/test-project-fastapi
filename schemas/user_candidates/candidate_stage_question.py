import uuid, datetime
from typing import Optional, List

from pydantic import BaseModel
from .candidate_stage_answer import CandidateStageAnswerRead
 


class CandidateStageQuestionBase(BaseModel):
    question: str
    question_type: str

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
    question: Optional[str]
    question_type: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class CandidateStageQuestionReadIn(BaseModel):
    id: Optional[uuid.UUID]
    answer: Optional[CandidateStageAnswerRead]
    question: Optional[str]
    question_type: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageInfoReadAnswer(BaseModel):
    id: Optional[uuid.UUID]
    status: Optional[str]   
    date_sign: Optional[datetime.date]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime] 
    is_waits: Optional[bool]
    candidate_stage_type_id: Optional[uuid.UUID]
    staff_unit_coordinate_id: Optional[uuid.UUID]


    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CandidateStageQuestionType(BaseModel):
    id: Optional[uuid.UUID]
    questions: Optional[List[CandidateStageQuestionReadIn]]
    name: Optional[str]
    candidate_stage_info: Optional[CandidateStageInfoReadAnswer]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
