import datetime

from typing import Optional

from pydantic import AnyUrl, root_validator
from datetime import date

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
    start_date: Optional[date] = date(1920, 1, 1)
    end_date: Optional[date] = date(1920, 1, 1)
    document_link: Optional[str] = "Данные отсутствуют!"
    course_provider: Optional[NamedModel] = NamedModel()

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    # @root_validator(pre=True)
    # def fill_none_values(cls, values):
    #     # Преобразуем GetterDict в dict
    #     values = dict(values)
    #
    #     defaults = {
    #         "start_date": date(1920, 1, 1),
    #         "end_date": date(1920, 1, 1),
    #         "document_link": "Данные отсутствуют!",
    #         "course_provider": NamedModel(),
    #     }
    #
    #     for key, default in defaults.items():
    #         values[key] = values.get(key) or default
    #
    #     return values

