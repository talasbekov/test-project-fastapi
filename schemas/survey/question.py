import uuid

from typing import Optional, List
from pydantic import root_validator

from schemas import NamedModel, ReadNamedModel
from .option import OptionRead


class QuestionBase(NamedModel):
    is_required: Optional[bool]
    question_type: str
    survey_id: Optional[uuid.UUID]
    quiz_id: Optional[uuid.UUID]
    score: Optional[int]

    @root_validator
    def validate_ids(cls, values):
        survey_id, quiz_id = values.get('survey_id'), values.get('quiz_id')
        if survey_id is not None and quiz_id is not None:
            raise ValueError(
                "Both survey_id and quiz_id cannot be non-null at the same time"
                )
        elif survey_id is None and quiz_id is None:
            raise ValueError(
                "Both survey_id and quiz_id cannot be null at the same time"
                )
        return values


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    question_type: Optional[str]


class QuestionRead(QuestionBase, ReadNamedModel):
    question_type: Optional[str]
    score: Optional[int]

    options: Optional[List[OptionRead]]

    class Config:
        orm_mode = True
