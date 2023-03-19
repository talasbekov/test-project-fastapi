import uuid
from typing import Optional

from pydantic import BaseModel


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
