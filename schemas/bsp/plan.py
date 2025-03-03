import uuid
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import Field, BaseModel

from schemas import UserShortReadStatus, CustomBaseModel
from .schedule_year import ScheduleYearRead

class BspPlanBase(CustomBaseModel):
    year: Optional[int]
    creator_id: Optional[str]
    status: Optional[Enum]
    signed_at: Optional[datetime]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class BspPlanCreate(BspPlanBase):
    pass


class BspPlanUpdate(BspPlanBase):
    pass

class BspPlanRead(BspPlanBase):
    created_at: Optional[datetime]
    id: Optional[str]
    creator: Optional[UserShortReadStatus]
    schedule_years: Optional[List[ScheduleYearRead]]

class BspPlanReadPagination(CustomBaseModel):
    total: int = Field(0, nullable=False)
    objects: List[BspPlanRead] = Field([], nullable=False)
