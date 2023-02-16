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

    @validator('properties')
    def properties_validator(cls, v):
        if v is None:
            return v
        if not isinstance(v, dict):
            raise ValueError(f'properties should be dictionary')
        keys = list(v)
        for key in keys:
            value = keys[key]
            if type(value) == dict:
                val_keys = list(value)
                if 'name' not in val_keys or 'value' not in val_keys:
                    raise ValueError(f'name or value should be in {key}!')
        return v


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
    can_cancel: Optional[bool]

    class Config:
        orm_mode = True
