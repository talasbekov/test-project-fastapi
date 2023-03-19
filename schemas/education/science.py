import uuid
from typing import Optional

from pydantic import BaseModel


class ScienceBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ScienceCreate(ScienceBase):
    pass


class ScienceUpdate(ScienceBase):
    pass


class ScienceRead(ScienceBase):
    id: Optional[uuid.UUID]
    name: str
