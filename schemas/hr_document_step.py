import uuid
from typing import Optional

from schemas import Model, ReadModel
from schemas import (DocumentStaffFunctionRead, JurisdictionRead)


class HrDocumentStepBase(Model):
    hr_document_template_id: str
    staff_function_id: str
    is_direct_supervisor: Optional[bool] = None
    category: Optional[int] = None


class HrDocumentStepCreate(HrDocumentStepBase):
    pass


class HrDocumentStepUpdate(HrDocumentStepBase):
    pass


class HrDocumentStepRead(HrDocumentStepBase, ReadModel):
    hr_document_template_id: Optional[str]
    staff_function_id: Optional[str]
    staff_function: Optional[DocumentStaffFunctionRead]
    jurisdiction_id: Optional[str]
    jurisdiction: Optional[JurisdictionRead]

    class Config:
        orm_mode = True
