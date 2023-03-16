import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas import DocumentStaffFunctionRead, StaffUnitRead, JurisdictionRead


class HrDocumentStepBase(BaseModel):
    hr_document_template_id: uuid.UUID 
    staff_function_id: uuid.UUID 


class HrDocumentStepCreate(HrDocumentStepBase):
    pass


class HrDocumentStepUpdate(HrDocumentStepBase):
    pass


class HrDocumentStepRead(HrDocumentStepBase):
    id: Optional[uuid.UUID]
    hr_document_template_id: Optional[uuid.UUID]
    staff_function_id: Optional[uuid.UUID]
    staff_function: Optional[DocumentStaffFunctionRead]
    jurisdiction_id: Optional[uuid.UUID]
    jurisdiction: Optional[JurisdictionRead]

    class Config:
        orm_mode = True
