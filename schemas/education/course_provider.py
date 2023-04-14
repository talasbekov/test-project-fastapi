import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class CourseProviderBase(NamedModel):
    pass


class CourseProviderCreate(CourseProviderBase):
    pass


class CourseProviderUpdate(CourseProviderBase):
    pass


class CourseProviderRead(CourseProviderBase, ReadNamedModel):

    class Config:
        orm_mode = True
