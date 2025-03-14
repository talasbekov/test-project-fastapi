import uuid

from typing import Optional, List
from pydantic import BaseModel, Field
from schemas import TextModel, ReadTextModel, Model


class OptionBase(TextModel):
    text: Optional[str]
    question_id: str
    score: Optional[int]
    diagram_description: Optional[str]
    diagram_descriptionKZ: Optional[str]
    report_description: Optional[str]
    report_descriptionKZ: Optional[str]


class OptionCreate(OptionBase):
    textKZ: Optional[str]


class OptionUpdate(OptionBase):
    question_id: Optional[str]


class OptionRead(OptionBase, ReadTextModel):
    question_id: Optional[str]
    score: Optional[int]

    class Config:
        orm_mode = True

class OptionReadPagination(Model):
    total: int = Field(0, nullable=False)
    objects: List[OptionRead] = Field([], nullable=False)