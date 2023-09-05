import uuid
from typing import Optional, List, Any

from datetime import time, date, datetime

from schemas import BaseModel, NamedModel, Model

class DayBase(NamedModel):
    pass


class DayCreate(DayBase):
    pass


class DayUpdate(DayBase):
    pass


class DayRead(DayBase):
    pass


class ActivityDateBase(Model):
    activity_date: date


class ActivityDateCreate(ActivityDateBase):
    pass


class ActivityDateUpdate(ActivityDateBase):
    pass


class ActivityDateRead(ActivityDateBase):
    pass


class ScheduleDayBase(BaseModel):
    day_id: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]
    month_id: Optional[str]
    activity_month_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScheduleDayCreate(ScheduleDayBase):
    pass


class ScheduleDayCreateWithString(BaseModel):
    day: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]


class ScheduleDayUpdate(ScheduleDayBase):
    pass

class MonthRead(NamedModel):
    order: Optional[int]
    id: Optional[uuid.UUID]

class ScheduleDayRead(ScheduleDayBase):
    id: Optional[str]
    day: Optional[DayRead]
    activity_dates: Optional[List[ActivityDateRead]]
    activity_month: Optional[MonthRead]
    start_time: Optional[str]
    end_time: Optional[str]

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            day=orm_obj.day,
            activity_dates=orm_obj.activity_dates,
            activity_month=orm_obj.activity_month,
            start_time=orm_obj.start_time.strftime('%H:%M:%S'),
            end_time=orm_obj.end_time.strftime('%H:%M:%S')
        )

