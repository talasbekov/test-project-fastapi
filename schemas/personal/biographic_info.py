import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from .family_status import FamilyStatusRead


class BiographicInfoBase(BaseModel):
    place_birth: str
    gender: bool
    citizenship: str
    nationality: str
    family_status_id: str
    address: str
    residence_address: str
    profile_id: str


class BiographicInfoCreate(BiographicInfoBase):
    pass


class BiographicInfoUpdate(BaseModel):
    residence_address: Optional[str]


class BiographicInfoRead(BiographicInfoBase):
    id: Optional[str]
    place_birth: Optional[str]
    gender: Optional[bool]
    citizenship: Optional[str]
    nationality: Optional[str]
    family_status_id: Optional[str]
    address: Optional[str]
    residence_address: Optional[str]
    profile_id: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    family_status: Optional[FamilyStatusRead]

    class Config:
        orm_mode = True
