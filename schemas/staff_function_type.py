import uuid
from typing import Optional

from pydantic import BaseModel


class StaffFunctionTypeBase(BaseModel):
    name: str


class DocumentStaffFunctionTypeBase(StaffFunctionTypeBase):
    can_cancel: bool


class ServiceStaffFunctionTypeBase(StaffFunctionTypeBase):
    pass


class DocumentStaffFunctionTypeCreate(DocumentStaffFunctionTypeBase):
    pass


class ServiceStaffFunctionTypeBase(ServiceStaffFunctionTypeBase):
    pass


class DocumentStaffFunctionTypeUpdate(DocumentStaffFunctionTypeBase):
    pass


class ServiceStaffFunctionTypeBase(ServiceStaffFunctionTypeBase):
    pass


class StaffFunctionTypeRead(StaffFunctionTypeBase):
    id: Optional[uuid.UUID]
    name: Optional[uuid.UUID]

    class Config:
        orm_mode=True


class DocumentStaffFunctionTypeRead(StaffFunctionTypeRead):
    can_cancel: Optional[bool]

    class Config:
        orm_mode=True


class ServiceStaffFunctionTypeRead(StaffFunctionTypeRead):

    class Config:
        orm_mode=True
