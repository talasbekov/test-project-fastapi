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
    pass


class OptionUpdate(OptionBase):
    question_id: Optional[uuid.UUID]
    pass


class OptionRead(OptionBase, ReadModel):
    question_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
