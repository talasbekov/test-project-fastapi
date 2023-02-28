import uuid
from typing import Optional

from pydantic import BaseModel


class StaffUnitBase(BaseModel):
    name: str
    max_rank_id: uuid.UUID


class StaffUnitCreate(StaffUnitBase):
    pass


class StaffUnitUpdate(StaffUnitBase):
    pass


class StaffUnitRead(StaffUnitBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    max_rank_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
