import uuid
from typing import Optional, List
from datetime import date

from schemas import (BaseModel,
                     NamedModel,
                     UserShortReadStatus,
                     StaffDivisionReadWithoutStaffUnit, )
from .activity import ActivityRead
from .schedule_day import ScheduleDayRead, ScheduleDayCreateWithString


class PlaceBase(NamedModel):
    pass


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(PlaceBase):
    pass


class PlaceRead(PlaceBase):
    id: Optional[str]


class MonthRead(NamedModel):
    id: Optional[str]


class ScheduleMonthBase(BaseModel):
    start_date: date
    end_date: date
    place_id: str
    schedule_id: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScheduleMonthCreate(ScheduleMonthBase):
    pass


class ScheduleMonthCreateWithDay(ScheduleMonthBase):
    days: List[ScheduleDayCreateWithString]
    instructor_ids: List[Optional[str]]


class ScheduleMonthUpdate(ScheduleMonthBase):
    pass


class ScheduleMonthRead(ScheduleMonthBase):
    id: Optional[str]
    instructors: Optional[List[Optional[UserShortReadStatus]]]
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
            activity=(orm_obj.schedule.activity
                      if orm_obj.schedule else None),
            staff_divisions=(orm_obj.schedule.staff_divisions
                             if orm_obj.schedule else None),
            activity_months=(orm_obj.schedule.activity_months
                             if orm_obj.schedule else None)
        )
