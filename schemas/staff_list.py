from datetime import datetime, date
from typing import Optional

from pydantic import Field

from schemas import NamedModel, ReadNamedModel, UserShortRead, Model


class StaffListBase(NamedModel):
    user_id: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class StaffListCreate(StaffListBase):
    pass


class StaffListUpdate(StaffListBase):
    pass


class StaffListUserCreate(Model):
    name: str


class StaffListRead(StaffListBase, ReadNamedModel):
    user_id: Optional[str] = Field(None, nullable=True)
    document_signed_by: Optional[str] = Field(None, nullable=True)
    document_signed_at: Optional[date] = Field(None, nullable=True)
    changes_size: Optional[int] = Field(None, nullable=True)
    rank: Optional[str] = Field(None, nullable=True)
    document_number: Optional[str] = Field(None, nullable=True)
    document_link: Optional[str] = Field(None, nullable=True)


class StaffListStatusRead(StaffListBase):
    id: Optional[str]
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

class StaffListApplyRead(Model):
    task_id: str
