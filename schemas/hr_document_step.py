import uuid

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


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
    id: uuid.UUID
    previous_step: Any

    class Config:
        orm_mode = True
