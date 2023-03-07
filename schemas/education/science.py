import uuid

from pydantic import BaseModel
from typing import Optional


class ScienceBase(BaseModel):
    name: str


class ScienceCreate(ScienceBase):
    pass


class ScienceUpdate(ScienceBase):
    pass


class ScienceRead(ScienceBase):
    id: Optional[uuid.UUID]
    name: str

    class Config:
        orm_mode = True
