import datetime
import uuid
from typing import Optional

from pydantic import AnyUrl

from schemas import NamedModel, ReadNamedModel
from .course_provider import CourseProviderRead


class CourseBase(NamedModel):
    profile_id: Optional[str]
    course_provider_id: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[AnyUrl]
    educational_profile_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseRead(CourseBase, ReadNamedModel):
    profile_id: Optional[str]
    course_provider_id: Optional[str]
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[str]
    educational_profile_id: Optional[str]

    course_provider: Optional[CourseProviderRead]
    
class CourseShortRead(NamedModel):
    start_date: Optional[datetime.date]
    end_date: Optional[datetime.date]
    document_link: Optional[str]

    course_provider: Optional[NamedModel]

