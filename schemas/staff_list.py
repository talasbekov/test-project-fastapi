import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel, UserRead


class StaffListBase(NamedModel):
    user_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffListCreate(StaffListBase):
    status: str


class StaffListUpdate(StaffListBase):
    pass


class StaffListUserCreate(BaseModel):
    name: str

class StaffListRead(StaffListBase, ReadNamedModel):
    user_id: Optional[uuid.UUID]
    status: Optional[str]
