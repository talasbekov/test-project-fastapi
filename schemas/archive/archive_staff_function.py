import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas import JurisdictionRead, ServiceStaffFunctionTypeRead, NamedModel, Model


class ArchiveStaffFunctionBase(NamedModel):
    hours_per_week: int


class ArchiveDocumentStaffFunctionBase(ArchiveStaffFunctionBase):
    priority: int
    role_id: str
    jurisdiction_id: str


class ArchiveServiceStaffFunctionBase(ArchiveStaffFunctionBase):

    type_id: Optional[str]


class ArchiveStaffFunctionCreate(ArchiveStaffFunctionBase):
    origin_id: Optional[str]


class ArchiveDocumentStaffFunctionCreate(ArchiveDocumentStaffFunctionBase):
    origin_id: Optional[str]


class NewArchiveStaffFunctionCreate(ArchiveStaffFunctionBase):
    pass


class NewArchiveDocumentStaffFunctionCreate(ArchiveDocumentStaffFunctionBase):
    pass


class ArchiveDocumentStaffFunctionAdd(ArchiveDocumentStaffFunctionBase):
    hr_document_template_id: str


class ArchiveServiceStaffFunctionCreate(ArchiveServiceStaffFunctionBase):
    origin_id: Optional[str]


class ArchiveStaffFunctionUpdate(ArchiveStaffFunctionBase):
    origin_id: Optional[str]


class NewArchiveServiceStaffFunctionCreate(ArchiveServiceStaffFunctionBase):
    pass


class NewArchiveStaffFunctionUpdate(ArchiveStaffFunctionBase):
    pass


class ArchiveServiceStaffFunctionUpdate(ArchiveServiceStaffFunctionBase):
    origin_id: Optional[str]


class ArchiveDocumentStaffFunctionUpdate(ArchiveDocumentStaffFunctionBase):
    origin_id: Optional[str]


class NewArchiveServiceStaffFunctionUpdate(ArchiveServiceStaffFunctionBase):
    pass


class NewArchiveDocumentStaffFunctionUpdate(ArchiveDocumentStaffFunctionBase):
    pass


class ArchiveStaffUnitFunctions(Model):
    staff_unit_id: str
    staff_function_ids: List[str]


class ArchiveStaffFunctionRead(ArchiveStaffFunctionBase):
    id: Optional[str]
    name: Optional[str]
    hours_per_week: Optional[int]
    discriminator: Optional[str]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ArchiveDocumentStaffFunctionTemplate(Model):

    id: Optional[str]
    name: Optional[str]

    class Config:
        orm_mode = True


class ArchiveDocumentStaffFunctionStep(Model):

    id: Optional[str]
    hr_document_template: Optional[ArchiveDocumentStaffFunctionTemplate]

    class Config:
        orm_mode = True


class ArchiveDocumentStaffFunctionRead(ArchiveStaffFunctionRead,
                                       ArchiveDocumentStaffFunctionBase):

    priority: Optional[int]
    role_id: Optional[str]
    role: Optional[ArchiveStaffFunctionRead]

    jurisdiction_id: Optional[str]
    jurisdiction: Optional[JurisdictionRead]

    hr_document_step: Optional[ArchiveDocumentStaffFunctionStep]


class ArchiveServiceStaffFunctionRead(ArchiveStaffFunctionRead,
                                      ArchiveServiceStaffFunctionBase):

    type_id: Optional[str]
    type: Optional[ServiceStaffFunctionTypeRead]


class AllArchiveStaffFunctionsRead(ArchiveServiceStaffFunctionRead,
                                   ArchiveDocumentStaffFunctionRead,
                                   ArchiveServiceStaffFunctionBase):
    pass
