import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ServiceArchiveStaffFunctionTypeBase(BaseModel):
    nameKZ: Optional[str] = Field(None, nullable=True)
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NewServiceArchiveStaffFunctionTypeCreate(ServiceArchiveStaffFunctionTypeBase):
    pass


class NewServiceArchiveStaffFunctionTypeUpdate(ServiceArchiveStaffFunctionTypeBase):
    pass


class ServiceArchiveStaffFunctionTypeCreate(ServiceArchiveStaffFunctionTypeBase):
    origin_id: Optional[uuid.UUID]


class ServiceArchiveStaffFunctionTypeUpdate(ServiceArchiveStaffFunctionTypeBase):
    origin_id: Optional[uuid.UUID]


class ServiceArchiveStaffFunctionTypeRead(ServiceArchiveStaffFunctionTypeBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
