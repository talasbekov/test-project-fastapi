import uuid
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import Field

from schemas import BaseModel, UserShortReadStatus
from .schedule_year import ScheduleYearRead

class BspPlanBase(BaseModel):
    year: Optional[int]
    creator_id: Optional[uuid.UUID]
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
    id: Optional[uuid.UUID]
    creator: Optional[UserShortReadStatus]
    schedule_years: Optional[List[ScheduleYearRead]]

class BspPlanReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[BspPlanRead] = Field([], nullable=False)
