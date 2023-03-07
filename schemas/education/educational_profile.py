import uuid

from pydantic import BaseModel
from typing import Optional


class EducationalProfileBase(BaseModel):
    profile_id: Optional[uuid.UUID]


class EducationalProfileCreate(EducationalProfileBase):
    pass


class EducationalProfileUpdate(EducationalProfileBase):
    pass


class EducationalProfileRead(EducationalProfileBase):
    id: Optional[uuid.UUID]
    profile_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
