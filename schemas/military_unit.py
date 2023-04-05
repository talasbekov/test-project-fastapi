import uuid
from typing import Optional

from pydantic import BaseModel


class MilitaryUnitBase(BaseModel):
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class MilitaryUnitCreate(MilitaryUnitBase):
    pass


class MilitaryUnitUpdate(MilitaryUnitBase):
    pass


class MilitaryUnitRead(MilitaryUnitBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
