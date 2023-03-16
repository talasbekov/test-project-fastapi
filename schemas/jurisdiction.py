import uuid
from typing import List, Optional

from pydantic import BaseModel


class JurisdictionBase(BaseModel):
    name_kz: str
    name_ru: str


class JurisdictionCreate(JurisdictionBase):
    pass


class JurisdictionUpdate(JurisdictionBase):
    pass


class JurisdictionRead(JurisdictionBase):
    id: Optional[uuid.UUID]
    name_kz: Optional[str]
    name_ru: Optional[str]

    class Config:
        orm_mode = True
