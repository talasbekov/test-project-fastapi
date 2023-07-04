import uuid
import datetime

from typing import Optional, List

from schemas import NamedModel, ReadNamedModel
from .question import QuestionRead

# base
class Base(NamedModel):
    description: Optional[str]
    start_date: datetime.datetime
    end_date: datetime.datetime
    jurisdiction_id: Optional[uuid.UUID]
    is_kz_required: Optional[bool]


class SurveyBase(Base):
    is_anonymous: Optional[bool]


class QuizBase(Base):
    pass


#create
class SurveyCreate(SurveyBase):
    pass


class QuizCreate(QuizBase):
    pass


#update
class SurveyUpdate(SurveyBase):
    name: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[str]


class QuizUpdate(QuizBase):
    name: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[str]


#read
class SurveyRead(SurveyBase, ReadNamedModel):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[str]
    questions: Optional[List[QuestionRead]]

    class Config:
        orm_mode = True


class QuizRead(QuizBase, ReadNamedModel):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[str]
    questions: Optional[List[QuestionRead]]

    class Config:
        orm_mode = True
