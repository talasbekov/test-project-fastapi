import uuid
from typing import Optional

from pydantic import BaseModel


class JurisdictionBase(BaseModel):
    name: str


class JurisdictionCreate(JurisdictionBase):
    pass


class JurisdictionUpdate(JurisdictionBase):
    pass


class JurisdictionRead(JurisdictionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True
