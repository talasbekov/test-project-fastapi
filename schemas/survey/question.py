import uuid

from typing import Optional

from schemas import Model, ReadModel


class QuestionBase(Model):
    text: str
    is_required: Optional[bool]
    survey_id: uuid.UUID
    question_type_id: uuid.UUID


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    text: Optional[str]
    survey_id: Optional[uuid.UUID]
    question_type_id: Optional[uuid.UUID]


class QuestionRead(QuestionBase, ReadModel):
    text: Optional[str]
    survey_id: Optional[uuid.UUID]
    question_type_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
