import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel, UserShortRead


class StaffListBase(NamedModel):
    user_id: uuid.UUID

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffListCreate(StaffListBase):
    pass


class StaffListUpdate(StaffListBase):
    pass


class StaffListUserCreate(BaseModel):
    name: str

class StaffListRead(StaffListBase, ReadNamedModel):
    user_id: Optional[uuid.UUID]

class StaffListStatusRead(StaffListBase):
    id: Optional[uuid.UUID]
    status: Optional[dict]
    updated_at: Optional[datetime]
    changes_count: Optional[int]
    user: Optional[UserShortRead]
    reg_number: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True