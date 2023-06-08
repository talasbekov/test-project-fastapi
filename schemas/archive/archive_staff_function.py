import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas import JurisdictionRead, ServiceStaffFunctionTypeRead


class ArchiveStaffFunctionBase(BaseModel):
    name: str
    nameKZ: Optional[str]
    hours_per_week: int


class ArchiveDocumentStaffFunctionBase(ArchiveStaffFunctionBase):
    priority: int
    role_id: uuid.UUID
    jurisdiction_id: uuid.UUID


class ArchiveServiceStaffFunctionBase(ArchiveStaffFunctionBase):

    type_id: Optional[uuid.UUID]


class ArchiveStaffFunctionCreate(ArchiveStaffFunctionBase):
    origin_id: Optional[uuid.UUID]


class ArchiveDocumentStaffFunctionCreate(ArchiveDocumentStaffFunctionBase):
    origin_id: Optional[uuid.UUID]


class NewArchiveStaffFunctionCreate(ArchiveStaffFunctionBase):
    pass


class NewArchiveDocumentStaffFunctionCreate(ArchiveDocumentStaffFunctionBase):
    pass


class ArchiveDocumentStaffFunctionAdd(ArchiveDocumentStaffFunctionBase):
    hr_document_template_id: uuid.UUID


class ArchiveServiceStaffFunctionCreate(ArchiveServiceStaffFunctionBase):
    origin_id: Optional[uuid.UUID]


class ArchiveStaffFunctionUpdate(ArchiveStaffFunctionBase):
    origin_id: Optional[uuid.UUID]


class NewArchiveServiceStaffFunctionCreate(ArchiveServiceStaffFunctionBase):
    pass


class NewArchiveStaffFunctionUpdate(ArchiveStaffFunctionBase):
    pass


class ArchiveServiceStaffFunctionUpdate(ArchiveServiceStaffFunctionBase):
    origin_id: Optional[uuid.UUID]


class ArchiveDocumentStaffFunctionUpdate(ArchiveDocumentStaffFunctionBase):
    origin_id: Optional[uuid.UUID]


class NewArchiveServiceStaffFunctionUpdate(ArchiveServiceStaffFunctionBase):
    pass


class NewArchiveDocumentStaffFunctionUpdate(ArchiveDocumentStaffFunctionBase):
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


class AllArchiveStaffFunctionsRead(ArchiveServiceStaffFunctionRead,
                                   ArchiveDocumentStaffFunctionRead,
                                   ArchiveServiceStaffFunctionBase):
    pass

