import uuid
from typing import Optional

from pydantic import BaseModel


class SpecialtyBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class SpecialtyCreate(SpecialtyBase):
    pass


class SpecialtyUpdate(SpecialtyBase):
    pass


class SpecialtyRead(SpecialtyBase):
    id: Optional[uuid.UUID]
    name: str
