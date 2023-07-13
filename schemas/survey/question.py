import uuid

from typing import Optional, List
from pydantic import BaseModel, Field
from schemas import TextModel, ReadTextModel
from .option import OptionRead


class QuestionBase(TextModel):
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


class QuestionRead(QuestionBase, ReadTextModel):
    question_type: Optional[str]
    score: Optional[int]

    options: Optional[List[OptionRead]]

    class Config:
        orm_mode = True

class QuestionReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[QuestionRead] = Field([], nullable=False)
