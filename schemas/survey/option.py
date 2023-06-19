import uuid

from typing import Optional, List

from schemas import Model, ReadModel


class OptionBase(Model):
    question_id: uuid.UUID
    text: Optional[str]
    min_value: Optional[int]
    max_value: Optional[int]
    row_position: Optional[int]
    column_position: Optional[int]
    is_checked: Optional[bool]
    

class OptionCreate(OptionBase):
    question_id: uuid.UUID
    text: Optional[str]
    min_value: Optional[int]
    max_value: Optional[int]
    row_position: Optional[int]
    column_position: Optional[int]
    is_checked: Optional[bool]


class OptionUpdate(OptionBase):
    question_id: Optional[uuid.UUID]
    text: Optional[str]
    min_value: Optional[int]
    max_value: Optional[int]
    row_position: Optional[int]
    column_position: Optional[int]
    is_checked: Optional[bool]


class OptionRead(OptionBase, ReadModel):
    question_id: Optional[uuid.UUID]
    text: Optional[str]
    min_value: Optional[int]
    max_value: Optional[int]
    row_position: Optional[int]
    column_position: Optional[int]
    is_checked: Optional[bool]

    class Config:
        orm_mode = True
