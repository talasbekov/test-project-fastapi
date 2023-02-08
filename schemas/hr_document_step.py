import uuid

from pydantic import BaseModel
from typing import List, Dict, Any


class HrDocumentStepBase(BaseModel):
    hr_document_template_id: uuid.UUID
    position_id: uuid.UUID
    role_id: uuid.UUID


class HrDocumentStepCreate(HrDocumentStepBase):
    pass


class HrDocumentStepUpdate(HrDocumentStepBase):
    pass


class HrDocumentStepRead(HrDocumentStepBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
