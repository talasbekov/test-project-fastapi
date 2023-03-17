import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from .family_status import FamilyStatusRead


class BiographicInfoBase(BaseModel):
    place_birth: str
    date_birth: datetime.datetime
    gender: bool
    citizenship: str
    nationality: str
    family_status_id: uuid.UUID
    address: str
    residence_address: str
    profile_id: uuid.UUID


class BiographicInfoCreate(BiographicInfoBase):
    pass


class BiographicInfoUpdate(BaseModel):
    residence_address: Optional[str]


class BiographicInfoRead(BiographicInfoBase):
    id: Optional[uuid.UUID]
    place_birth: Optional[str]
    date_birth: Optional[datetime.date]
    gender: Optional[bool]
    citizenship: Optional[str]
    nationality: Optional[str]
    family_status_id: Optional[uuid.UUID]
    address: Optional[str]
    residence_address: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    family_status: Optional[FamilyStatusRead]

    class Config:
        orm_mode = True
