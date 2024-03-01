from typing import List

from pydantic import Field

from schemas import NamedModel, ReadNamedModel, BaseModel


class CourseProviderBase(NamedModel):
    pass


class CourseProviderCreate(CourseProviderBase):
    pass


class CourseProviderUpdate(CourseProviderBase):
    pass


class CourseProviderRead(CourseProviderBase, ReadNamedModel):

    class Config:
        orm_mode = True


class CourseProviderReadPagination(BaseModel):
    total: int = Field(0, nullable=False)
    objects: List[CourseProviderRead] = Field([], nullable=False)
