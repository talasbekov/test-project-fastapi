from typing import Optional, List
from datetime import date

from pydantic import Field

from schemas import UserShortReadStatus, Model
from .schedule_month import ScheduleMonthRead
from .activity import ActivityRead


class AttendedUserBase(Model):
    attendance_status: Optional[str]
    user_id: Optional[str]
    attendance_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AttendedUserCreate(AttendedUserBase):
    pass


class AttendedUserUpdate(AttendedUserBase):
    pass


class AttendedUserRead(AttendedUserBase):
    id: Optional[str]
    user: Optional[UserShortReadStatus]


class AttendanceUserStatus(Model):
    attendance_status: Optional[str]
    reason: Optional[str]
    user_id: Optional[str]


class AttendanceChangeStatus(Model):
    attendance_id: str
    user_status: Optional[List[AttendanceUserStatus]]


class AttendanceChangeStatusWithSchedule(Model):
    schedule_id: str
    attendance_status: Optional[str]
    reason: Optional[str]
    user_id: str
    date: date
    activity: Optional[str]


class AttendanceBase(Model):
    attendance_date: Optional[date]
    schedule_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    id: Optional[str]
    schedule: Optional[ScheduleMonthRead]
    attended_users: Optional[List[AttendedUserRead]]
    class_status: Optional[str]


class AttendanceReadShort(AttendanceBase):
    id: Optional[str]
    class_status: Optional[str]


class AttendancePercentageRead(Model):
    activity: Optional[ActivityRead]
    percentage: Optional[int]


class AttendanceReadPagination(Model):
    total: int = Field(0, nullable=False)
    objects: List[AttendanceRead] = Field([], nullable=False)
