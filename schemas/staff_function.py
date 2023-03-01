import uuid
from typing import Optional

from pydantic import BaseModel

from .staff_function_type import (DocumentStaffFunctionTypeRead,
                                  ServiceStaffFunctionTypeRead)


class StaffFunctionBase(BaseModel):
    name: str
    hours_per_week: int


class DocumentStaffFunctionBase(StaffFunctionBase):
    priority: int
    role_id: uuid.UUID


class ServiceStaffFunctionBase(StaffFunctionBase):

    type_id: uuid.UUID


class StaffFunctionCreate(StaffFunctionBase):
    pass


class DocumentStaffFunctionCreate(DocumentStaffFunctionBase):
    pass


class ServiceStaffFunctionCreate(ServiceStaffFunctionBase):
    pass


class StaffFunctionUpdate(StaffFunctionBase):
    pass


class ServiceStaffFunctionUpdate(ServiceStaffFunctionBase):
    pass


class DocumentStaffFunctionUpdate(DocumentStaffFunctionBase):
    pass


class StaffFunctionRead(StaffFunctionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    hours_per_week: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DocumentStaffFunctionRead(StaffFunctionRead):
    priority: Optional[int]
    role_id: Optional[uuid.UUID]
    role: Optional[DocumentStaffFunctionTypeRead]


class ServiceStaffFunctionRead(StaffFunctionRead):

    type_id = Optional[uuid.UUID]
    type = Optional[ServiceStaffFunctionTypeRead]
