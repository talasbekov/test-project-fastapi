import uuid

from pydantic import BaseModel
from typing import Optional


class CourseProviderBase(BaseModel):
    name: str


class CourseProviderCreate(CourseProviderBase):
    pass


class CourseProviderUpdate(CourseProviderBase):
    pass


class CourseProviderRead(CourseProviderBase):
    id: Optional[uuid.UUID]
    name: str

    class Config:
        orm_mode = True
