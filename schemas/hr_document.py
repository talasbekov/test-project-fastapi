import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import validator, Field

from schemas import (
    HrDocumentTemplateRead,
    UserRead,
    HrDocumentStatusRead,
    HrDocumentStepRead,
)
from schemas import Model, ReadModel


class HrDocumentBase(Model):
    hr_document_template_id: str
    due_date: Optional[datetime] = None
    parent_id: Optional[str] = Field(None, nullable=True)
    properties: Optional[Dict[str, Any]]
    initial_comment: Optional[str] = None

    @validator("properties")
    def properties_validator(cls, v):
        if v is None:
            return v
        if not isinstance(v, dict):
            raise ValueError("properties should be dictionary")
        keys = list(v)
        for key in keys:
            value = v[key]
            if isinstance(value, dict):
                val_keys = list(value)
                if "name" not in val_keys or "nameKZ" not in val_keys:
                    raise ValueError(f"name or nameKZ should be in {key}!")
        return v


class DraftHrDocumentCreate(HrDocumentBase):
    user_ids: Optional[List[str]]


class DraftHrDocumentInit(Model):
    document_step_users_ids: dict

    @validator("document_step_users_ids")
    def document_step_users_ids_validator(cls, v):
        if v is None:
            return v
        if not isinstance(v, dict):
            raise ValueError("document_step_users_ids should be dictionary")
        keys = list(v)

        for key in keys:
            value = v[key]
            if key == -1:
                if not isinstance(value, list):
                    raise ValueError("document_step_users_ids should be list")
                for user_id in value:
                    if not isinstance(user_id, str):
                        raise ValueError(
                            "document_step_users_ids should be str")
            elif key == 1:
                raise ValueError("Don't add initiator")
            else:
                if isinstance(value, dict):
                    continue
                value_to_uuid = str(value)
                if not isinstance(value_to_uuid, str):
                    raise ValueError(
                        "document_step_users_ids should be str")

        sorted(v, key=lambda x: keys.index(x))

        return v


class HrDocumentInit(DraftHrDocumentCreate, DraftHrDocumentInit):
    pass


class HrDocumentInitEcp(DraftHrDocumentCreate, DraftHrDocumentInit):
    certificate_blob: str

class HrDocumentSign(Model):
    comment: Optional[str]
    is_signed: bool

class HrDocumentSignEcp(HrDocumentSign):
    certificate_blob: str


class HrDocumentSignEcpWithIds(HrDocumentSignEcp):
    document_ids: List[Optional[str]]


class HrDocumentSign(Model):
    comment: Optional[str]
    is_signed: bool


class HrDocumentCreate(HrDocumentBase):
    status_id: str
    initialized_at: Optional[datetime]


class HrDocumentUpdate(HrDocumentBase):
    user_ids: List[str]
    status_id: str


class HrDocumentRead(HrDocumentBase, ReadModel):
    properties: Optional[dict]
    document_template: Optional[HrDocumentTemplateRead]
    hr_document_template_id: Optional[str]
    status_id: Optional[str]
    status: Optional[HrDocumentStatusRead]
    initialized_by_id: Optional[str]
    initialized_by: Optional[UserRead]
    due_date: Optional[datetime]
    properties: Optional[Union[dict, None]]
    can_cancel: Optional[bool]
    users: Optional[List[UserRead]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_step: Optional[HrDocumentStepRead]
    new_value: Optional[Any]
    old_history_id: Optional[str]
    children: Optional[List["HrDocumentRead"]]
    reg_number: Optional[str]

    class Config:
        orm_mode = True

class UserShortRead(Model):
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]
    iin: Optional[str]

class QrRead(Model):
    step: Optional[HrDocumentStepRead]
    user: Optional[UserShortRead]
    signed_at: Optional[datetime]
    qr_base64: Optional[str]