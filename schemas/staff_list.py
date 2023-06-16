import uuid
from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field

from schemas import NamedModel, ReadNamedModel, UserShortRead


class StaffListBase(NamedModel):
    user_id: Optional[uuid.UUID]

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
    user_id: Optional[uuid.UUID] = Field(None, nullable=True)
    document_signed_by: Optional[str] = Field(None, nullable=True)
    document_signed_at: Optional[date] = Field(None, nullable=True)
    changes_size: Optional[int] = Field(None, nullable=True)


class StaffListStatusRead(StaffListBase):
    id: Optional[uuid.UUID]
    status: Optional[str] = Field(None, nullable=True)
    updated_at: Optional[datetime]
    changes_size: Optional[int] = Field(None, nullable=True)
    user: Optional[UserShortRead] = Field(None, nullable=True)
    reg_number: Optional[str] = Field(None, nullable=True)
    document_signed_by: Optional[str] = Field(None, nullable=True)
    document_signed_at: Optional[date] = Field(None, nullable=True)

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
