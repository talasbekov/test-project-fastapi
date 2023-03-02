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


class ServiceStaffFunctionTypeCreate(ServiceStaffFunctionTypeBase):
    pass


class DocumentStaffFunctionTypeUpdate(DocumentStaffFunctionTypeBase):
    pass


class ServiceStaffFunctionTypeUpdate(ServiceStaffFunctionTypeBase):
    pass


class StaffFunctionTypeRead(StaffFunctionTypeBase):
    id: Optional[uuid.UUID]
    name: Optional[str]


class DocumentStaffFunctionTypeRead(StaffFunctionTypeRead):
    can_cancel: Optional[bool]

    class Config:
        orm_mode=True


class ServiceStaffFunctionTypeRead(StaffFunctionTypeRead):
    pass

    class Config:
        orm_mode=True