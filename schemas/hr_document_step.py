import uuid
from typing import List, Optional

from pydantic import BaseModel

from schemas import StaffFunctionRead, StaffUnitRead


class HrDocumentStepBase(BaseModel):
    hr_document_template_id: uuid.UUID 
    staff_function_id: uuid.UUID 


class HrDocumentStepCreate(HrDocumentStepBase):
    pass


class HrDocumentStepUpdate(HrDocumentStepBase):
    pass


class HrDocumentStepRead(HrDocumentStepBase):
    id: Optional[uuid.UUID]
    next_step: Optional[List['HrDocumentStepRead']]
    hr_document_template_id: Optional[uuid.UUID]
    previous_step_id: Optional[uuid.UUID]
    staff_unit_id: Optional[uuid.UUID]
    staff_function_id: Optional[uuid.UUID]
    staff_function: Optional[StaffFunctionRead]
    staff_unit: Optional[StaffUnitRead]
    jurisdiction_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
