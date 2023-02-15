import uuid
from datetime import datetime

from pydantic import BaseModel, validator, ValidationError
from typing import Any, Dict, List, Optional, Union

from models import HrDocumentStatus
from .hr_document_template import HrDocumentTemplateRead
from .validator import validate_property


class HrDocumentBase(BaseModel):
    hr_document_template_id: uuid.UUID
    status: HrDocumentStatus
    due_date: datetime
    properties: Dict[str, Any]


class HrDocumentInit(HrDocumentBase):
    user_ids: List[uuid.UUID]


class HrDocumentSign(BaseModel):
    comment: Optional[str]
    is_signed: bool


class HrDocumentCreate(HrDocumentBase):
    pass


class HrDocumentUpdate(HrDocumentBase):
    pass


class HrDocumentRead(HrDocumentBase):
    id: Optional[uuid.UUID]
    properties: Optional[dict]
    document_template: Optional[HrDocumentTemplateRead]
    hr_document_template_id: Optional[uuid.UUID]
    status: Optional[HrDocumentStatus]
    due_date: Optional[datetime]
    properties: Optional[Union[dict, None]]
    details: Optional[Union[dict, None]]

    class Config:
        orm_mode = True
