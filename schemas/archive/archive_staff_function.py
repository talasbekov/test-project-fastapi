import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas import JurisdictionRead, ServiceStaffFunctionTypeRead



class ArchiveStaffFunctionBase(BaseModel):
    name: str
    hours_per_week: int
    origin_id: uuid.UUID



class ArchiveDocumentStaffFunctionBase(ArchiveStaffFunctionBase):
    priority: int
    role_id: uuid.UUID
    jurisdiction_id: uuid.UUID
    

class ArchiveServiceStaffFunctionBase(ArchiveStaffFunctionBase):

    type_id: uuid.UUID


class ArchiveStaffFunctionCreate(ArchiveStaffFunctionBase):
    pass


class ArchiveDocumentStaffFunctionCreate(ArchiveDocumentStaffFunctionBase):
    pass


class ArchiveDocumentStaffFunctionAdd(ArchiveDocumentStaffFunctionBase):
    hr_document_template_id: uuid.UUID


class ArchiveServiceStaffFunctionCreate(ArchiveServiceStaffFunctionBase):
    pass


class ArchiveStaffFunctionUpdate(ArchiveStaffFunctionBase):
    pass


class ArchiveServiceStaffFunctionUpdate(ArchiveServiceStaffFunctionBase):
    pass


class ArchiveDocumentStaffFunctionUpdate(ArchiveDocumentStaffFunctionBase):
    pass


class ArchiveStaffUnitFunctions(BaseModel):
    staff_unit_id: uuid.UUID
    staff_function_ids: List[uuid.UUID]


class ArchiveStaffFunctionRead(ArchiveStaffFunctionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    hours_per_week: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ArchiveDocumentStaffFunctionTemplate(BaseModel):

    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True


class ArchiveDocumentStaffFunctionStep(BaseModel):

    id: Optional[uuid.UUID]
    hr_document_template: Optional[ArchiveDocumentStaffFunctionTemplate]

    class Config:
        orm_mode = True


class ArchiveDocumentStaffFunctionRead(ArchiveStaffFunctionRead, ArchiveDocumentStaffFunctionBase):
    
    priority: Optional[int]
    role_id: Optional[uuid.UUID]
    role: Optional[ArchiveStaffFunctionRead]

    jurisdiction_id: Optional[uuid.UUID]
    jurisdiction: Optional[JurisdictionRead]

    hr_document_step: Optional[ArchiveDocumentStaffFunctionStep]


class ArchiveServiceStaffFunctionRead(ArchiveStaffFunctionRead, ArchiveServiceStaffFunctionBase):

    type_id: Optional[uuid.UUID]
    type: Optional[ServiceStaffFunctionTypeRead]
