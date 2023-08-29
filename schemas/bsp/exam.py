import uuid
from datetime import date, time
from typing import Optional, List
from pydantic import Field

from schemas import (BaseModel,
                     UserShortReadStatus,
                     UserShortReadAgeCategory,
                     StaffDivisionReadWithoutStaffUnit)
from .schedule_month import PlaceRead
from .activity import ActivityRead


class ExamScheduleBase(BaseModel):
    start_date: Optional[date]
    end_date: Optional[date]
    start_time: Optional[time]
    end_time: Optional[time]
    place_id: Optional[str]
    schedule_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ExamScheduleCreateWithInstructors(ExamScheduleBase):
    instructor_ids: Optional[List[Optional[str]]]


class ExamScheduleCreate(ExamScheduleBase):
    pass

class ExamScheduleUpdate(ExamScheduleBase):
    pass


class ExamScheduleRead(ExamScheduleBase):
    id: Optional[str]
    instructors: Optional[List[Optional[UserShortReadStatus]]]
    place: Optional[PlaceRead]
    activity: Optional[ActivityRead]
    class_status: Optional[str]
    staff_divisions: Optional[List[StaffDivisionReadWithoutStaffUnit]]
    class_status: Optional[str]

    @classmethod
    def from_orm(cls, orm_obj):
        return cls(
            id=orm_obj.id,
            start_date=orm_obj.start_date,
            end_date=orm_obj.end_date,
            start_time=orm_obj.start_time.strftime('%H:%M:%S'),
            end_time=orm_obj.end_time.strftime('%H:%M:%S'),
            schedule_id=orm_obj.schedule_id,
            place_id=orm_obj.place_id,
            place=orm_obj.place,
            instructors=(orm_obj.instructors
                         if orm_obj.instructors != [] else None),
            activity=(orm_obj.schedule.activity
                      if orm_obj.schedule else None),
            staff_divisions=(orm_obj.schedule.staff_divisions
                             if orm_obj.schedule else None),
            class_status=orm_obj.class_status
        )

class ExamScheduleReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[ExamScheduleRead] = Field([], nullable=False)


class ExamResultBase(BaseModel):
    exam_date: Optional[date]
    grade: Optional[int]
    user_id: Optional[str]
    exam_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ExamResultCreate(ExamResultBase):
    pass


class ExamResultUpdate(ExamResultBase):
    pass


class ExamUserResult(BaseModel):
    grade: Optional[int]
    results: Optional[dict]
    user_id: Optional[uuid.UUID]


class ExamChangeResults(BaseModel):
    exam_id: uuid.UUID
    users_results: Optional[List[ExamUserResult]]


class ExamResultRead(ExamResultBase):
    id: Optional[str]
    user: Optional[UserShortReadAgeCategory]
    exam: Optional[ExamScheduleRead]
    results: Optional[dict]


class ExamResultReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[ExamResultRead] = Field([], nullable=False)