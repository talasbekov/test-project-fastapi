import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ValidationError, validator

from models import HrDocumentStatus

from .hr_document_template import HrDocumentTemplateRead
from .user import UserRead
from .validator import hr_document_properties_validator


class HrDocumentBase(BaseModel):
    hr_document_template_id: uuid.UUID
    due_date: datetime
    properties: Dict[str, Any]

    _check_properties = validator("properties", allow_reuse=True)(hr_document_properties_validator)


class HrDocumentInit(HrDocumentBase):
    user_ids: List[uuid.UUID]


class HrDocumentSign(BaseModel):
    comment: Optional[str]
    is_signed: bool


class HrDocumentCreate(HrDocumentBase):
    status: HrDocumentStatus


class HrDocumentUpdate(HrDocumentBase):
    status: HrDocumentStatus


class HrDocumentRead(HrDocumentBase):
    id: Optional[uuid.UUID]
    properties: Optional[dict]
    document_template: Optional[HrDocumentTemplateRead]
    hr_document_template_id: Optional[uuid.UUID]
    status: Optional[HrDocumentStatus]
    due_date: Optional[datetime]
    properties: Optional[Union[dict, None]]
    can_cancel: Optional[bool]
    users: Optional[List[UserRead]]

    class Config:
        orm_mode = True
    