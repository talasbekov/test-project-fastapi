import uuid

from typing import Optional, List
from pydantic import BaseModel, Field

from models import QuestionTypeEnum
from schemas import TextModel, ReadTextModel, Model
from .option import OptionRead


class QuestionBase(TextModel):
    is_required: Optional[bool]
    question_type: QuestionTypeEnum
    survey_id: Optional[str]
    score: Optional[int]


class OptionBase(TextModel):
    text: Optional[str]
    score: Optional[int]
    diagram_description: Optional[str]
    diagram_descriptionKZ: Optional[str]
    report_description: Optional[str]
    report_descriptionKZ: Optional[str]


class OptionCreate(OptionBase):
    pass


class QuestionCreate(QuestionBase):
    pass

class QuestionCreateList(QuestionCreate):
    options: Optional[List[OptionCreate]]


class QuestionUpdate(QuestionBase):
    text: Optional[str]
    question_type: Optional[str]


class QuestionRead(QuestionBase, ReadTextModel):
    question_type: Optional[QuestionTypeEnum]
    score: Optional[int]

    options: Optional[List[OptionRead]]

    class Config:
        orm_mode = True

class QuestionReadPagination(Model):
    total: int = Field(0, nullable=False)
    objects: List[QuestionRead] = Field([], nullable=False)
