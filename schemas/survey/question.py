import uuid

from typing import Optional, List

from schemas import Model, ReadModel
from .option import OptionRead


class QuestionBase(Model):
    text: str
    is_required: Optional[bool]
    question_type: str
    survey_id: Optional[uuid.UUID]
    quiz_id: Optional[uuid.UUID]
    score: Optional[int]
    diagram_description: Optional[str]
    report_description: Optional[str]


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    text: Optional[str]
    question_type: Optional[str]


class QuestionRead(QuestionBase, ReadModel):
    text: Optional[str]
    question_type: Optional[str]
    score: Optional[int]

    options: Optional[List[OptionRead]]

    class Config:
        orm_mode = True
