import uuid

from pydantic import BaseModel
from typing import List, Dict, Any


class HrDocumentStepBase(BaseModel):
    hr_document_template_id: str
    position_id: str
    role_id: str


class HrDocumentStepCreate(HrDocumentStepBase):
    pass


class HrDocumentStepUpdate(HrDocumentStepBase):
    pass


class HrDocumentStepRead(HrDocumentStepBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
