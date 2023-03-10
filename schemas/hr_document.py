import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ValidationError, validator

from models import HrDocumentStatus

from schemas import HrDocumentTemplateRead, UserRead


class HrDocumentBase(BaseModel):
    hr_document_template_id: uuid.UUID
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
            value = v[key]
            if isinstance(value, dict):
                val_keys = list(value)
                if 'name' not in val_keys or 'value' not in val_keys:
                    raise ValueError(f'name or value should be in {key}!')
        return v


class HrDocumentInit(HrDocumentBase):
    user_ids: List[uuid.UUID]
    # list of dict, which have {int: uuid.UUID()}
    document_step_users_ids : dict

    @validator('document_step_users_ids')
    def document_step_users_ids_validator(cls, v):
        if v is None:
            return v
        if not isinstance(v, dict):
            raise ValueError(f'document_step_users_ids should be dictionary')
        keys = list(v)
        
        for key in keys:
            value = v[key]
            if key == -1:
                if not isinstance(value, list):
                    raise ValueError(f'document_step_users_ids should be list')
                for user_id in value:
                    if not isinstance(user_id, uuid.UUID):
                        raise ValueError(f'document_step_users_ids should be uuid.UUID')
            else:
                value_to_uuid = uuid.UUID(value)
                if not isinstance(value_to_uuid, uuid.UUID):
                    raise ValueError(f'document_step_users_ids should be uuid.UUID')
        
        sorted(v, key=lambda x: keys.index(x))
        
        return v
    

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
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    new_value: Optional[dict]

    class Config:
        orm_mode = True
    