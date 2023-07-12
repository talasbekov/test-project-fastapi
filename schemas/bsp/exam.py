import uuid
from datetime import date, time
from typing import Optional, List

from schemas import BaseModel, UserRead
from .schedule_month import PlaceRead

class ExamScheduleBase(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    start_time: Optional[time]
    end_time: Optional[time]
    place_id: Optional[uuid.UUID]
    schedule_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ExamScheduleCreate(ExamScheduleBase):
    pass


class ExamScheduleUpdate(ExamScheduleBase):
    pass


class ExamScheduleRead(ExamScheduleBase):
    id: Optional[uuid.UUID]
    instructors: Optional[List[Optional[UserRead]]]
    place: Optional[PlaceRead]


class ExamResultBase(BaseModel):
    exam_date: Optional[date]
    grade: Optional[int]
    user_id: Optional[uuid.UUID]
    exam_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ExamResultCreate(ExamResultBase):
    pass


class ExamResultUpdate(ExamResultBase):
    pass


class ExamResultRead(ExamResultBase):
    id: Optional[uuid.UUID]
    user: Optional[UserRead]
    exam: Optional[ExamScheduleRead]
