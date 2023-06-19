import uuid

from typing import Optional, List

from schemas import Model, ReadModel
from .option import OptionRead


class QuestionBase(Model):
    text: str
    is_required: Optional[bool]
    survey_id: uuid.UUID
    question_type: str


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    text: Optional[str]
    survey_id: Optional[uuid.UUID]
    question_type: Optional[str]


class QuestionRead(QuestionBase, ReadModel):
    text: Optional[str]
    survey_id: Optional[uuid.UUID]
    question_type: Optional[str]

    options: Optional[List[OptionRead]]
    
    class Config:
        orm_mode = True
