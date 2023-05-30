import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from schemas import (DocumentStaffFunctionRead, JurisdictionRead)


class HrDocumentStepBase(Model):
    hr_document_template_id: uuid.UUID
    staff_function_id: uuid.UUID
    is_direct_supervisor: Optional[bool] = None
    category: Optional[int] = None


class HrDocumentStepCreate(HrDocumentStepBase):
    pass


class HrDocumentStepUpdate(HrDocumentStepBase):
    pass


class HrDocumentStepRead(HrDocumentStepBase, ReadModel):
    hr_document_template_id: Optional[uuid.UUID]
    staff_function_id: Optional[uuid.UUID]
    staff_function: Optional[DocumentStaffFunctionRead]
    jurisdiction_id: Optional[uuid.UUID]
    jurisdiction: Optional[JurisdictionRead]

    class Config:
        orm_mode = True
