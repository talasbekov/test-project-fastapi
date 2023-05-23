import uuid
from typing import List, Optional

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from schemas import (DocumentStaffFunctionTypeRead,
                     ServiceStaffFunctionTypeRead, JurisdictionRead)


class StaffFunctionBase(NamedModel):
    hours_per_week: int


class DocumentStaffFunctionBase(StaffFunctionBase):
    priority: int
    role_id: uuid.UUID
    jurisdiction_id: uuid.UUID
    is_direct_supervisor: Optional[bool] = None


class ServiceStaffFunctionBase(StaffFunctionBase):

    type_id: uuid.UUID


class StaffFunctionCreate(StaffFunctionBase):
    pass


class DocumentStaffFunctionCreate(DocumentStaffFunctionBase):
    pass


class DocumentStaffFunctionAdd(DocumentStaffFunctionBase):
    hr_document_template_id: uuid.UUID

class DocumentStaffFunctionConstructorAdd(DocumentStaffFunctionAdd):
    staff_unit_id: uuid.UUID

class DocumentStaffFunctionConstructorAdd(DocumentStaffFunctionAdd):
    staff_unit_id: uuid.UUID

class DocumentStaffFunctionAppendToStaffUnit(Model):
    staff_function_id: uuid.UUID
    staff_unit_ids: list[uuid.UUID]


class ServiceStaffFunctionCreate(ServiceStaffFunctionBase):
    pass


class StaffFunctionUpdate(StaffFunctionBase):
    pass


class ServiceStaffFunctionUpdate(ServiceStaffFunctionBase):
    pass


class DocumentStaffFunctionUpdate(DocumentStaffFunctionBase):
    pass


class StaffUnitFunctions(Model):
    staff_unit_id: uuid.UUID
    staff_function_ids: List[uuid.UUID]


class StaffFunctionRead(StaffFunctionBase, ReadNamedModel):
    hours_per_week: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DocumentStaffFunctionTemplate(NamedModel):

    class Config:
        orm_mode = True


class DocumentStaffFunctionStep(ReadModel):

    hr_document_template: Optional[DocumentStaffFunctionTemplate]

    class Config:
        orm_mode = True


# class DocumentStaffFunctionInit(BaseModel):
#     hr_document_step: Optional[DocumentStaffFunctionStep]
#     priority: Optional[int]
#     role_id: Optional[uuid.UUID]
#     hours_per_week: Optional[int]
#     jurisdiction_id: Optional[uuid.UUID]


class DocumentStaffFunctionRead(StaffFunctionRead, DocumentStaffFunctionBase):
    
    priority: Optional[int]
    role_id: Optional[uuid.UUID]
    jurisdiction_id: Optional[uuid.UUID]

    role: Optional[DocumentStaffFunctionTypeRead]
    hr_document_step: Optional[DocumentStaffFunctionStep]
    jurisdiction: Optional[JurisdictionRead]


class ServiceStaffFunctionRead(StaffFunctionRead, ServiceStaffFunctionBase):

    type_id: Optional[uuid.UUID]
    type: Optional[ServiceStaffFunctionTypeRead]
