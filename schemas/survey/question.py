import uuid

from typing import Optional, List
from pydantic import validator, root_validator

from schemas import Model, ReadModel
from .option import OptionRead


class QuestionBase(Model):
    text: str
    is_required: Optional[bool]
    question_type: str
    survey_id: Optional[uuid.UUID]
    quiz_id: Optional[uuid.UUID]
    score: Optional[int]

    @validator('score')
    def validate_score(cls, score, values):
        quiz_id = values.get('quiz_id')

        if score is not None and quiz_id is None:
            raise ValueError('Score is only available for quiz questions')

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
    text: Optional[str]
    question_type: Optional[str]


class QuestionRead(QuestionBase, ReadModel):
    text: Optional[str]
    question_type: Optional[str]

    options: Optional[List[OptionRead]]

    class Config:
        orm_mode = True
