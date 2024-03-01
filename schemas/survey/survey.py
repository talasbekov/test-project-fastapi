import datetime

from typing import Optional, List
from pydantic import BaseModel, Field

from schemas import NamedModel, ReadNamedModel, UserShortRead
from models import (SurveyTypeEnum, SurveyStatusEnum, SurveyRepeatTypeEnum)
from .question import QuestionRead
from .survey_jurisdiction import SurveyJurisdictionRead, SurveyJurisdictionBase


class SurveyBase(NamedModel):
    description: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    is_kz_translate_required: Optional[bool]
    is_anonymous: Optional[bool]
    repeat_type: Optional[SurveyRepeatTypeEnum]
    comp_form_for_id: Optional[str]


class SurveyCreateWithJurisdiction(SurveyBase):
    type: SurveyTypeEnum
    jurisdictions: List[SurveyJurisdictionBase]
    owner_id: Optional[str]


class SurveyCreate(SurveyBase):
    type: SurveyTypeEnum
    owner_id: str


class SurveyUpdate(SurveyBase):
    name: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[SurveyStatusEnum]


class SurveyRead(SurveyBase, ReadNamedModel):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[SurveyStatusEnum]
    questions: Optional[List[QuestionRead]]
    type: Optional[SurveyTypeEnum]
    jurisdictions: Optional[List[SurveyJurisdictionRead]]
    comp_form_for: Optional[UserShortRead]

    class Config:
        orm_mode = True
    

class SurveyReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[SurveyRead] = Field([], nullable=False)
