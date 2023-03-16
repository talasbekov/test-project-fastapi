import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


class BiographicInfoBase(BaseModel):
    place_birth: str
    date_birth: datetime.date
    gender: bool
    citizenship: str
    nationality: str
    family_status: str
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
    family_status: Optional[str]
    address: Optional[str]
    residence_address: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True
