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
    jurisdiction_type: str
    certain_member_id: Optional[uuid.UUID]
    staff_division_id: Optional[uuid.UUID]


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
    jurisdiction_type: Optional[str]


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
    jurisdiction_type: Optional[str]

    class Config:
        orm_mode = True


class QuizRead(QuizBase, ReadNamedModel):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[str]
    questions: Optional[List[QuestionRead]]
    jurisdiction_type: Optional[str]

    class Config:
        orm_mode = True
