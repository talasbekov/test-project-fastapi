import uuid
import datetime

from typing import Optional, List

from schemas import NamedModel, ReadNamedModel
from .question import QuestionRead


class SurveyBase(NamedModel):
    description: Optional[str]
    start_date: datetime.datetime
    end_date: datetime.datetime
    is_anonymous: Optional[bool] = False
    jurisdiction_id: Optional[uuid.UUID]


class SurveyCreate(SurveyBase):
    pass


class SurveyUpdate(SurveyBase):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]


class SurveyRead(SurveyBase, ReadNamedModel):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    
    questions: Optional[List[QuestionRead]]

    class Config:
        orm_mode = True
