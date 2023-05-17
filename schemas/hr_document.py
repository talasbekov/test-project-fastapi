import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, validator

from schemas import HrDocumentTemplateRead, UserRead, HrDocumentStatusRead, HrDocumentStepRead
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class HrDocumentBase(Model):
    hr_document_template_id: uuid.UUID
    due_date: datetime
    parent_id: Optional[uuid.UUID]
    properties: Optional[Dict[str, Any]]

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
                if 'name' not in val_keys or 'nameKZ' not in val_keys:
                    raise ValueError(f'name or nameKZ should be in {key}!')
        return v



class DraftHrDocumentCreate(HrDocumentBase):
    user_ids: Optional[List[uuid.UUID]]


class DraftHrDocumentInit(Model):
    document_step_users_ids: dict

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
            elif key == 1:
                raise ValueError(f"Don't add initiator")
            else:
                value_to_uuid = uuid.UUID(value)
                if not isinstance(value_to_uuid, uuid.UUID):
                    raise ValueError(f'document_step_users_ids should be uuid.UUID')
        
        sorted(v, key=lambda x: keys.index(x))
        
        return v


class HrDocumentInit(DraftHrDocumentCreate, DraftHrDocumentInit):
    pass
    

class HrDocumentSign(Model):
    comment: Optional[str]
    is_signed: bool


class HrDocumentCreate(HrDocumentBase):
    status_id: uuid.UUID


class HrDocumentUpdate(HrDocumentBase):
    user_ids: List[uuid.UUID]
    status_id: uuid.UUID


class HrDocumentRead(HrDocumentBase, ReadModel):
    properties: Optional[dict]
    document_template: Optional[HrDocumentTemplateRead]
    hr_document_template_id: Optional[uuid.UUID]
    status_id: Optional[uuid.UUID]
    status: Optional[HrDocumentStatusRead]
    initialized_by_id: Optional[uuid.UUID]
    initialized_by: Optional[UserRead]
    due_date: Optional[datetime]
    properties: Optional[Union[dict, None]]
    can_cancel: Optional[bool]
    users: Optional[List[UserRead]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_step: Optional[HrDocumentStepRead]
    new_value: Optional[dict]
    old_history_id: Optional[uuid.UUID]
    children: Optional[List['HrDocumentRead']]

    class Config:
        orm_mode = True
