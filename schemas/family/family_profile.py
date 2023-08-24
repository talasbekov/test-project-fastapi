import uuid
from typing import Optional, List

from pydantic import BaseModel

from .family import FamilyRead


class FamilyProfileBase(BaseModel):

    profile_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class FamilyProfileCreate(FamilyProfileBase):
    pass


class FamilyProfileUpdate(FamilyProfileBase):
    pass


class FamilyProfileRead(FamilyProfileBase):

    id: Optional[str]
    profile_id: Optional[str]

    family: Optional[List[FamilyRead]]
