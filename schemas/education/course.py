import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl, BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from .course_provider import CourseProviderRead


class CourseBase(NamedModel):
    profile_id: Optional[uuid.UUID]
    course_provider_id: Optional[uuid.UUID]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[AnyUrl]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseRead(CourseBase, ReadNamedModel):
    profile_id: Optional[uuid.UUID]
    course_provider_id: Optional[uuid.UUID]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[str]

    course_provider: Optional[CourseProviderRead]
