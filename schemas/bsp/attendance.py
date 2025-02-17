import uuid
from typing import Optional, List
from datetime import date

from pydantic import Field

from schemas import BaseModel, UserShortReadStatus
from .schedule_month import ScheduleMonthRead
from .activity import ActivityRead


class AttendedUserBase(BaseModel):
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


class AttendanceUserStatus(BaseModel):
    attendance_status: Optional[str]
    reason: Optional[str]
    user_id: Optional[str]


class AttendanceChangeStatus(BaseModel):
    attendance_id: str
    user_status: Optional[List[AttendanceUserStatus]]


class AttendanceChangeStatusWithSchedule(BaseModel):
    schedule_id: str
    attendance_status: Optional[str]
    reason: Optional[str]
    user_id: str
    date: date
    activity: Optional[str]


class AttendanceBase(BaseModel):
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


class AttendancePercentageRead(BaseModel):
    activity: Optional[ActivityRead]
    percentage: Optional[int]


class AttendanceReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[AttendanceRead] = Field([], nullable=False)
