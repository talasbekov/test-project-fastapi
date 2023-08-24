import uuid

from typing import List, Optional
from pydantic import BaseModel, Field
from schemas import Model, ReadModel


class AnswerBase(Model):
    question_id: str
    text: Optional[str]
    option_ids: Optional[List[str]]


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    question_id: Optional[str]


# read
class AnswerRead(AnswerBase, ReadModel):
    question_id: Optional[str]
    user_id: Optional[str]
    encrypted_used_id: Optional[str]
    score: Optional[int]

    class Config:
        orm_mode = True

class AnswerReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[AnswerRead] = Field([], nullable=False)
