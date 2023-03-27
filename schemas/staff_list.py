import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class StaffListBase(BaseModel):
    name: str
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

class StaffListRead(StaffListBase):
    id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    status: Optional[str]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
