import uuid
from datetime import datetime

from pydantic import BaseModel
from typing import List, Dict, Union, Optional

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
    id: Optional[uuid.UUID]
    document_type: Optional[HrDocumentTemplateRead]
    hr_document_template_id: Optional[uuid.UUID]
    status: Optional[HrDocumentStatus]
    due_date: Optional[datetime]
    properties: Optional[Union[dict, None]]
    details: Optional[Union[dict, None]]

    class Config:
        orm_mode = True
