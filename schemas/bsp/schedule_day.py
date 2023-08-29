import uuid
from typing import Optional

from datetime import time

from schemas import BaseModel, NamedModel


class DayBase(NamedModel):
    pass


class DayCreate(DayBase):
    pass


class DayUpdate(DayBase):
    pass


class DayRead(DayBase):
    pass


class ScheduleDayBase(BaseModel):
    day_id: Optional[str]
    start_time: Optional[time]
    end_time: Optional[time]
    month_id: Optional[str]

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


class ScheduleDayRead(ScheduleDayBase):
    id: Optional[str]
    day: Optional[DayRead]
