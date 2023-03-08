import uuid
import datetime

from pydantic import BaseModel
from typing import Optional


class CourseBase(BaseModel):
    name: str
    profile_id: Optional[uuid.UUID]
    provider_id: str
    course_provider_id: Optional[uuid.UUID]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: str


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: Optional[uuid.UUID]
    name: str
    profile_id: Optional[uuid.UUID]
    provider_id: str
    course_provider_id: Optional[uuid.UUID]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: str

    class Config:
        orm_mode = True
