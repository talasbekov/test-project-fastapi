import uuid
import datetime

from typing import Optional, List

from pydantic import BaseModel


class BiographicInfoBase(BaseModel):
    place_birth: str
    gender: bool
    citizenship: str
    nationality: str
    family_status: str
    address: str
    profile_id: uuid.UUID


class BiographicInfoCreate(BiographicInfoBase):
    pass


class BiographicInfoUpdate(BiographicInfoBase):
    pass


class BiographicInfoRead(BiographicInfoBase):
    id: Optional[uuid.UUID]
    place_birth: Optional[str]
    gender: Optional[bool]
    citizenship: Optional[str]
    nationality: Optional[str]
    family_status: Optional[str]
    address: Optional[str]
    profile_id: Optional[uuid.UUID]
    created_at: Optional[datetime.date]
    updated_at: Optional[datetime.date]

    class Config:
        orm_mode = True
