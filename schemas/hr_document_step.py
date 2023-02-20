import uuid
from typing import Any, List, Optional

from pydantic import BaseModel


class HrDocumentStepBase(BaseModel):
    hr_document_template_id: uuid.UUID
    previous_step_id: Optional[uuid.UUID]
    position_id: uuid.UUID
    role_id: uuid.UUID


class HrDocumentStepCreate(HrDocumentStepBase):
    pass


class HrDocumentStepUpdate(HrDocumentStepBase):
    pass


class HrDocumentStepRead(HrDocumentStepBase):
    id: Optional[uuid.UUID]
    next_step: Optional[List['HrDocumentStepRead']]
    hr_document_template_id: Optional[uuid.UUID]
    previous_step_id: Optional[uuid.UUID]
    position_id: Optional[uuid.UUID]
    role_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
