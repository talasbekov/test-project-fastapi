import uuid

from typing import List, Optional
from pydantic import BaseModel, Field
from schemas import Model, ReadModel, Model
from .question import QuestionRead
from .option import OptionRead

class AnswerBase(Model):
    question_id: str
    text: Optional[str]


class AnswerCreate(AnswerBase):
    option_ids: Optional[List[uuid.UUID]]


class AnswerUpdate(AnswerBase):
    question_id: Optional[uuid.UUID]
    option_ids: Optional[List[uuid.UUID]]


# read
class AnswerRead(AnswerBase, ReadModel):
    question_id: Optional[str]
    user_id: Optional[str]
    encrypted_used_id: Optional[str]
    score: Optional[int]
    question: Optional[QuestionRead]
    options: Optional[List[OptionRead]]

    class Config:
        orm_mode = True

class AnswerReadPagination(Model):
    total: int = Field(0, nullable=False)
    objects: List[AnswerRead] = Field([], nullable=False)


class AnswerAnalyze(Model):
    question_id: Optional[uuid.UUID]
    question_text: Optional[str]
    question_textKZ: Optional[str]
    option_id: Optional[uuid.UUID]
    option_text: Optional[str]
    option_textKZ: Optional[str]
    count: Optional[int]
    division_name: Optional[str]
