import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import Field

from schemas import (BaseModel,
                     NamedModel,
                     UserShortReadStatus,
                     StaffDivisionReadWithoutStaffUnit,
                     )
from .activity import ActivityRead
from .schedule_month import ScheduleMonthRead
from .exam import ExamScheduleRead


class MonthBase(NamedModel):
    order: Optional[int]


class MonthCreate(MonthBase):
    pass


class MonthUpdate(MonthBase):
    pass


class MonthRead(MonthBase):
    id: Optional[str]
    has_schedule_month: bool = True


class ScheduleYearBase(BaseModel):
    is_exam_required: Optional[bool]
    retry_count: Optional[int]
    plan_id: Optional[str]
    activity_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScheduleYearCreateString(ScheduleYearBase):
    activity_months: Optional[List[Optional[str]]]
    exam_months: Optional[List[Optional[str]]]
    staff_division_ids: List[str]


class ScheduleYearCreate(ScheduleYearBase):
    is_active: bool


class ScheduleYearUpdate(ScheduleYearBase):
    pass


class ScheduleYearRead(ScheduleYearBase):
    id: Optional[str]
    created_at: Optional[datetime]
    staff_divisions: Optional[List[StaffDivisionReadWithoutStaffUnit]]
    users: Optional[List[Optional[UserShortReadStatus]]]
    activity: Optional[ActivityRead]
    activity_months: Optional[List[MonthRead]]
    exam_months: Optional[List[MonthRead]]
    months: Optional[List[ScheduleMonthRead]]
    exams: Optional[List[ExamScheduleRead]]
    
class ScheduleYearReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[ScheduleYearRead] = Field([], nullable=False)
