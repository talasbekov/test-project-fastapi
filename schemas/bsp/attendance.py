import uuid
from typing import Optional, List
from datetime import date

from schemas import BaseModel, UserRead
from .schedule_month import ScheduleMonthRead

class AttendedUserBase(BaseModel):
    is_attended: Optional[bool]
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
    user: Optional[UserRead]


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


class AbsentUserBase(BaseModel):
    reason: Optional[str]
    absent_date: Optional[date]
    user_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class AbsentUserCreate(AttendanceBase):
    pass


class AbsentUserUpdate(AttendanceBase):
    pass


class AbsentUserRead(AttendanceBase):
    id: Optional[uuid.UUID]
    user: Optional[UserRead]
