import uuid
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel

from schemas import NamedModel, ReadNamedModel, UserShortRead


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
    document_signed_by: Optional[str]
    document_signed_at: Optional[date]
    changes_size: Optional[int]


class StaffListStatusRead(StaffListBase):
    id: Optional[uuid.UUID]
    status: Optional[str]
    updated_at: Optional[datetime]
    changes_size: Optional[int]
    user: Optional[UserShortRead]
    reg_number: Optional[str]
    document_signed_by: Optional[str]
    document_signed_at: Optional[date]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
