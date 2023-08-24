import uuid
import datetime

from typing import Optional, List
from pydantic import BaseModel, Field

from schemas import NamedModel, ReadNamedModel
from models import (SurveyTypeEnum, SurveyJurisdictionTypeEnum, SurveyStaffPositionEnum,
                    SurveyStatusEnum, SurveyRepeatTypeEnum)
from .question import QuestionRead


class SurveyBase(NamedModel):
    description: Optional[str]
    start_date: datetime.datetime
    end_date: datetime.datetime
    jurisdiction_type: SurveyJurisdictionTypeEnum
    certain_member_id: Optional[str]
    staff_division_id: Optional[str]
    staff_position: SurveyStaffPositionEnum
    is_kz_translate_required: Optional[bool]
    is_anonymous: Optional[bool]
    repeat_type: Optional[SurveyRepeatTypeEnum]


class SurveyCreate(SurveyBase):
    type: SurveyTypeEnum


class SurveyUpdate(SurveyBase):
    name: Optional[str]
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[SurveyStatusEnum]
    jurisdiction_type: Optional[SurveyJurisdictionTypeEnum]
    staff_position: Optional[SurveyStaffPositionEnum]


class SurveyRead(SurveyBase, ReadNamedModel):
    start_date: Optional[datetime.datetime]
    end_date: Optional[datetime.datetime]
    status: Optional[SurveyStatusEnum]
    questions: Optional[List[QuestionRead]]
    jurisdiction_type: Optional[SurveyJurisdictionTypeEnum]
    staff_position: Optional[SurveyStaffPositionEnum]
    type: Optional[SurveyTypeEnum]

    class Config:
        orm_mode = True


class SurveyReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[SurveyRead] = Field([], nullable=False)
