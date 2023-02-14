import uuid
from datetime import datetime

from pydantic import BaseModel
from typing import List, Dict, Union

from models import HrDocumentStatus
from .hr_document_template import HrDocumentTemplateRead


class HrDocumentBase(BaseModel):
    hr_document_template_id: uuid.UUID
    status: HrDocumentStatus
    due_date: datetime
    properties: Union[dict, None]
    details: Union[dict, None]


class HrDocumentCreate(HrDocumentBase):
    pass


class HrDocumentUpdate(HrDocumentBase):
    pass


class HrDocumentRead(HrDocumentBase):
    id: uuid.UUID
    document_type: HrDocumentTemplateRead

    class Config:
        orm_mode = True
