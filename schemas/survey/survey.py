import uuid
import datetime

from typing import Optional, List

from schemas import NamedModel, ReadNamedModel
from .question import QuestionRead


class SurveyBase(NamedModel):
    description: Optional[str]
    start_date: datetime.datetime
    end_date: datetime.datetime
    type: str
    jurisdiction_id: Optional[uuid.UUID]


class SurveyCreate(SurveyBase):
    pass


class SurveyUpdate(SurveyBase):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    type: Optional[str]


class SurveyRead(SurveyBase, ReadNamedModel):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    type: Optional[str]
    
    questions: Optional[List[QuestionRead]]

    class Config:
        orm_mode = True
