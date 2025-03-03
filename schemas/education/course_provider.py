from typing import List

from pydantic import Field, BaseModel

from schemas import NamedModel, ReadNamedModel, CustomBaseModel


class CourseProviderBase(NamedModel):
    pass


class CourseProviderCreate(CourseProviderBase):
    pass


class CourseProviderUpdate(CourseProviderBase):
    pass


class CourseProviderRead(CourseProviderBase, ReadNamedModel):

    class Config:
        orm_mode = True


class CourseProviderReadPagination(CustomBaseModel):
    total: int = Field(0, nullable=False)
    objects: List[CourseProviderRead] = Field([], nullable=False)
