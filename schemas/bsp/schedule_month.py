import uuid
from typing import Optional, List
from datetime import date

from schemas import (BaseModel,
                     NamedModel,
                     UserShortRead,
                     StaffDivisionReadWithoutStaffUnit, )
from .activity import ActivityRead
from .schedule_day import ScheduleDayRead


class PlaceBase(NamedModel):
    pass


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(PlaceBase):
    pass


class PlaceRead(PlaceBase):
    id: Optional[uuid.UUID]


class MonthRead(NamedModel):
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
    activity: Optional[ActivityRead]
    staff_divisions: Optional[List[StaffDivisionReadWithoutStaffUnit]]
    activity_months: Optional[List[MonthRead]]

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            start_date=orm_obj.start_date,
            end_date=orm_obj.end_date,
            place_id=orm_obj.place_id,
            schedule_id=orm_obj.schedule_id,
            instructors=orm_obj.instructors,
            place=orm_obj.place,
            days=orm_obj.days,
            activity=orm_obj.schedule.activity,
            staff_divisions=orm_obj.schedule.staff_divisions,
            activity_months=orm_obj.schedule.activity_months
        )
