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
    day_id: Optional[uuid.UUID]
    start_time: Optional[time]
    end_time: Optional[time]
    month_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScheduleDayCreate(ScheduleDayBase):
    pass


class ScheduleDayUpdate(ScheduleDayBase):
    pass


class ScheduleDayRead(ScheduleDayBase):
    id: Optional[uuid.UUID]
    day: Optional[DayRead]
