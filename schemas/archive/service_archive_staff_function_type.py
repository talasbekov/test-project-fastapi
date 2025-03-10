import datetime

from typing import Optional

from pydantic import Field
from schemas import Model


class ServiceArchiveStaffFunctionTypeBase(Model):
    nameKZ: Optional[str] = Field(None, nullable=True)
    name: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class NewServiceArchiveStaffFunctionTypeCreate(
        ServiceArchiveStaffFunctionTypeBase):
    pass


class NewServiceArchiveStaffFunctionTypeUpdate(
        ServiceArchiveStaffFunctionTypeBase):
    pass


class ServiceArchiveStaffFunctionTypeCreate(
        ServiceArchiveStaffFunctionTypeBase):
    origin_id: Optional[str]


class ServiceArchiveStaffFunctionTypeUpdate(
        ServiceArchiveStaffFunctionTypeBase):
    origin_id: Optional[str]


class ServiceArchiveStaffFunctionTypeRead(ServiceArchiveStaffFunctionTypeBase):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
