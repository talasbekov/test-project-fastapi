import uuid

from typing import Optional, List
from pydantic import BaseModel, Field
from schemas import TextModel, ReadTextModel


class OptionBase(TextModel):
    text: Optional[str]
    question_id: uuid.UUID
    score: Optional[int]
    diagram_description: Optional[str]
    diagram_descriptionKZ: Optional[str]
    report_description: Optional[str]
    report_descriptionKZ: Optional[str]


class OptionCreate(OptionBase):
    textKZ: Optional[str]


class OptionUpdate(OptionBase):
    question_id: Optional[uuid.UUID]


class OptionRead(OptionBase, ReadTextModel):
    question_id: Optional[uuid.UUID]
    score: Optional[int]

    class Config:
        orm_mode = True

class OptionReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[OptionRead] = Field([], nullable=False)