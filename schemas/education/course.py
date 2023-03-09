import uuid
import datetime

from pydantic import BaseModel
from typing import Optional

from .course_provider import CourseProviderRead


class CourseBase(BaseModel):
    name: str
    profile_id: Optional[uuid.UUID]
    course_provider_id: Optional[uuid.UUID]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseRead(CourseBase):
    id: Optional[uuid.UUID]
    name: str
    profile_id: Optional[uuid.UUID]
    course_provider_id: Optional[uuid.UUID]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: str

    course_provider: Optional[CourseProviderRead]
