import uuid

from typing import List, Optional
from pydantic import BaseModel, Field
from schemas import Model, ReadModel
from .option import OptionRead
from .question import QuestionRead

class AnswerBase(Model):
    question_id: uuid.UUID
    text: Optional[str]
    option_id: Optional[uuid.UUID]
    option_ids: Optional[List[uuid.UUID]]


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    question_id: Optional[uuid.UUID]


# read
class AnswerRead(AnswerBase, ReadModel):
    question_id: Optional[uuid.UUID]
    question: Optional[QuestionRead]
    options: Optional[List[OptionRead]]
    user_id: Optional[uuid.UUID]
    encrypted_used_id: Optional[str]
    score: Optional[int]

    class Config:
        orm_mode = True

class AnswerReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[AnswerRead] = Field([], nullable=False)
