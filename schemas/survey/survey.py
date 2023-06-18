import uuid
import datetime

from typing import Optional

from schemas import NamedModel, ReadNamedModel


class SurveyBase(NamedModel):
    description: Optional[str]
    start_date: datetime.datetime
    end_date: datetime.datetime
    type_id: uuid.UUID
    jurisdiction_id: Optional[uuid.UUID]


class SurveyCreate(SurveyBase):
    pass


class SurveyUpdate(SurveyBase):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    type_id: Optional[uuid.UUID]


class SurveyRead(SurveyBase, ReadNamedModel):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    type_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
