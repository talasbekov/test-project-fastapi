import uuid
from datetime import datetime
from typing import Optional, List

from schemas import (BaseModel,
                     NamedModel,
                     UserShortRead,
                     StaffDivisionReadWithoutStaffUnit,
                     )
from .activity import ActivityRead
from .schedule_month import ScheduleMonthRead
from .exam import ExamScheduleRead


class MonthBase(NamedModel):
    pass


class MonthCreate(MonthBase):
    pass


class MonthUpdate(MonthBase):
    pass


class MonthRead(MonthBase):
    id: Optional[uuid.UUID]


class ScheduleYearBase(BaseModel):
    is_exam_required: Optional[bool]
    retry_count: Optional[int]
    plan_id: Optional[uuid.UUID]
    activity_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScheduleYearCreateString(ScheduleYearBase):
    activity_months: Optional[List[Optional[str]]]
    exam_months: Optional[List[Optional[str]]]


class ScheduleYearCreate(ScheduleYearBase):
    pass


class ScheduleYearUpdate(ScheduleYearBase):
    pass


class ScheduleYearRead(ScheduleYearBase):
    id: Optional[uuid.UUID]
    created_at: Optional[datetime]
    staff_divisions: Optional[List[StaffDivisionReadWithoutStaffUnit]]
    users: Optional[List[Optional[UserShortRead]]]
    activity: Optional[ActivityRead]
    activity_months: Optional[List[MonthRead]]
    exam_months: Optional[List[MonthRead]]
    months: Optional[List[ScheduleMonthRead]]
    exams: Optional[List[ExamScheduleRead]]
