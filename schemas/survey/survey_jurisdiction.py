import uuid

from typing import Optional

from models import SurveyJurisdictionTypeEnum, SurveyStaffPositionEnum
from schemas import Model, ReadModel


class SurveyJurisdictionBase(Model):
    jurisdiction_type: SurveyJurisdictionTypeEnum
    staff_position: Optional[SurveyStaffPositionEnum]
    staff_division_id: Optional[str]
    certain_member_id: Optional[str]


class SurveyJurisdictionCreate(SurveyJurisdictionBase):
    survey_id: uuid.UUID


class SurveyJurisdictionUpdate(SurveyJurisdictionBase):
    survey_id: Optional[uuid.UUID]


class SurveyJurisdictionRead(SurveyJurisdictionBase, ReadModel):
    survey_id: Optional[uuid.UUID]
    
    class Config:
        orm_mode = True
