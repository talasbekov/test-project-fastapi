from typing import Optional

from schemas import NamedModel, ReadNamedModel


class StaffFunctionTypeBase(NamedModel):
    pass

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


class StaffFunctionTypeRead(StaffFunctionTypeBase, ReadNamedModel):

    class Config:
        orm_mode=True
        arbitrary_types_allowed = True


class DocumentStaffFunctionTypeRead(StaffFunctionTypeRead):
    can_cancel: Optional[bool]


class ServiceStaffFunctionTypeRead(StaffFunctionTypeRead):
    pass
