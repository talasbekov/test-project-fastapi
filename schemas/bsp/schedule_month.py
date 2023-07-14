import uuid
from typing import Optional, List
from datetime import date

from schemas import BaseModel, NamedModel, UserShortRead
from .schedule_day import ScheduleDayRead

class PlaceBase(NamedModel):
    pass


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(PlaceBase):
    pass


class PlaceRead(PlaceBase):
    id: Optional[uuid.UUID]


class ScheduleMonthBase(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    place_id: Optional[uuid.UUID]
    schedule_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScheduleMonthCreate(ScheduleMonthBase):
    pass


class ScheduleMonthUpdate(ScheduleMonthBase):
    pass


class ScheduleMonthRead(ScheduleMonthBase):
    id: Optional[uuid.UUID]
    instructors: Optional[List[Optional[UserShortRead]]]
    place: Optional[PlaceRead]
    days: Optional[List[Optional[ScheduleDayRead]]]
