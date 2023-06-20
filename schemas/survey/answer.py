import uuid

from typing import List, Optional, Dict

from schemas import Model, ReadModel
from .option import OptionRead


class AnswerBase(Model):
    question_id: uuid.UUID
    text: Optional[str]
    option_id: Optional[uuid.UUID]
    option_ids: Optional[List[uuid.UUID]]
    scale_value: Optional[int]
    grid_values: Optional[Dict[str, Dict[str, bool]]]
    checkbox_grid_values: Optional[Dict[str, Dict[str, bool]]]


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    question_id: Optional[uuid.UUID]


# read
class AnswerRead(AnswerBase, ReadModel):
    question_id: Optional[uuid.UUID]
    options: Optional[List[OptionRead]]
    user_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
