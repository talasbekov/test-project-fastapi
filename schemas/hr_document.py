import uuid

from pydantic import BaseModel
from typing import List, Dict

from models import HrDocumentStatus
from .hr_document_template import HrDocumentTemplateRead


class HrDocumentBase(BaseModel):
    document_type_id: str
    status: HrDocumentStatus
    properties: dict


class HrDocumentCreate(HrDocumentBase):
    pass


class HrDocumentUpdate(HrDocumentBase):
    pass


class HrDocumentRead(HrDocumentBase):
    id: uuid.UUID
    document_type: HrDocumentTemplateRead

    class Config:
        orm_mode = True
