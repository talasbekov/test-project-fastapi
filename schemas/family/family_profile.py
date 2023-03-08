import datetime
import uuid
from typing import Optional

from pydantic import BaseModel
from .family import FamilyRead


class FamilyProfileBase(BaseModel):

    profile_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class FamilyProfileCreate(FamilyProfileBase):
    pass


class FamilyProfileUpdate(FamilyProfileBase):
    pass


class FamilyProfileRead(FamilyProfileBase):

    id: Optional[uuid.UUID]

    family: Optional[FamilyRead]
