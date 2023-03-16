import uuid
import datetime

from typing import Optional, List

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
    profile_id: uuid.UUID


class BiographicInfoCreate(BiographicInfoBase):
    pass


class BiographicInfoUpdate(BiographicInfoBase):
    pass


class BiographicInfoRead(BiographicInfoBase):
    id: Optional[uuid.UUID]
    place_birth: Optional[str]
    date_birth: Optional[datetime.datetime]
    gender: Optional[bool]
    citizenship: Optional[str]
    nationality: Optional[str]
    family_status_id: Optional[uuid.UUID]
    address: Optional[str]
    profile_id: Optional[uuid.UUID]
    family_status: Optional[FamilyStatusRead]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True
