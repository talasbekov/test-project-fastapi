import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas import (DocumentStaffFunctionTypeRead, JurisdictionRead,
                     ServiceStaffFunctionTypeRead)


class StaffFunctionBase(BaseModel):
    name: str
    hours_per_week: int


class DocumentStaffFunctionBase(StaffFunctionBase):
    priority: int
    role_id: uuid.UUID
    jurisdiction_id: uuid.UUID


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


class StaffUnitFunctions(BaseModel):
    staff_unit_id: uuid.UUID
    staff_function_ids: List[uuid.UUID]


class StaffFunctionRead(StaffFunctionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    hours_per_week: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DocumentStaffFunctionTemplate(BaseModel):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True


class DocumentStaffFunctionStep(BaseModel):
    hr_document_template: Optional[DocumentStaffFunctionTemplate]

    class Config:
        orm_mode = True


class DocumentStaffFunctionRead(StaffFunctionRead, DocumentStaffFunctionBase):
    
    priority: Optional[int]
    role_id: Optional[uuid.UUID]
    role: Optional[DocumentStaffFunctionTypeRead]

    jurisdiction_id: Optional[uuid.UUID]
    jurisdiction: Optional[JurisdictionRead]

    hr_document_step: Optional[DocumentStaffFunctionStep]


class ServiceStaffFunctionRead(StaffFunctionRead, ServiceStaffFunctionBase):

    type_id: Optional[uuid.UUID]
    type: Optional[ServiceStaffFunctionTypeRead]
