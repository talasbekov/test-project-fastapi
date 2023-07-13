import uuid
from datetime import datetime
from typing import Optional, List
from enum import Enum

from schemas import BaseModel, UserRead
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
    id: Optional[uuid.UUID]
    creator: Optional[UserRead]
    schedule_years: Optional[List[ScheduleYearRead]]
