import uuid
from typing import Optional, List
from datetime import date

from schemas import BaseModel, UserShortRead
from .schedule_month import ScheduleMonthRead
from .activity import ActivityRead


class AttendedUserBase(BaseModel):
    attendance_status: Optional[str]
    user_id: Optional[uuid.UUID]
    attendance_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AttendedUserCreate(AttendedUserBase):
    pass


class AttendedUserUpdate(AttendedUserBase):
    pass


class AttendedUserRead(AttendedUserBase):
    id: Optional[uuid.UUID]
    user: Optional[UserShortRead]


class AttendanceChangeStatus(BaseModel):
    attendance_id: uuid.UUID
    attendance_status: Optional[str]
    user_ids: List[uuid.UUID]


class AttendanceBase(BaseModel):
    attendance_date: Optional[date]
    schedule_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(AttendanceBase):
    pass


class AttendanceRead(AttendanceBase):
    id: Optional[uuid.UUID]
    schedule: Optional[ScheduleMonthRead]
    attended_users: Optional[List[AttendedUserRead]]


class AttendancePercentageRead(BaseModel):
    activity: Optional[ActivityRead]
    percentage: Optional[int]
