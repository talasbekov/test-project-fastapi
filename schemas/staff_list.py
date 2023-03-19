import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class StaffListBase(BaseModel):
    name: str
    status: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffListCreate(StaffListBase):
    pass


class StaffListUpdate(StaffListBase):
    pass


class StaffListRead(StaffListBase):
    id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]

    created_at: Optional[datetime]
    updated_at: Optional[datetime]
