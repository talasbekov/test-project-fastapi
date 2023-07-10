import uuid

from typing import Optional

from schemas import Model, ReadModel


class OptionBase(Model):
    question_id: uuid.UUID
    text: Optional[str]
    min_value: Optional[int]
    max_value: Optional[int]
    row_position: Optional[int]
    column_position: Optional[int]
    is_checked: Optional[bool]
    score: Optional[int]


class OptionCreate(OptionBase):
    pass


class OptionUpdate(OptionBase):
    question_id: Optional[uuid.UUID]


class OptionRead(OptionBase, ReadModel):
    question_id: Optional[uuid.UUID]
    score: Optional[int]

    class Config:
        orm_mode = True
