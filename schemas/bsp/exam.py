import uuid
from datetime import date, time
from typing import Optional, List
from pydantic import Field

from schemas import BaseModel, UserShortReadStatus
from .schedule_month import PlaceRead
from .activity import ActivityRead

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


class ExamScheduleCreateWithInstructors(ExamScheduleBase):
    instructor_ids: List[Optional[uuid.UUID]]


class ExamScheduleCreate(ExamScheduleBase):
    pass

class ExamScheduleUpdate(ExamScheduleBase):
    pass


class ExamScheduleRead(ExamScheduleBase):
    id: Optional[uuid.UUID]
    instructors: Optional[List[Optional[UserShortReadStatus]]]
    place: Optional[PlaceRead]
    activity: Optional[ActivityRead]

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            start_date=orm_obj.start_date,
            end_date=orm_obj.end_date,
            start_time=orm_obj.start_time,
            end_time=orm_obj.end_time,
            schedule_id=orm_obj.schedule_id,
            place_id=orm_obj.place_id,
            place=orm_obj.place,
            instructors=orm_obj.instructors,
            activity=orm_obj.schedule.activity
        )


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
    user: Optional[UserShortReadStatus]
    exam: Optional[ExamScheduleRead]

class ExamResultReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[ExamResultRead] = Field([], nullable=False)