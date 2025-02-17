import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import validator, Field, BaseModel
from models import SubjectType
from schemas import (
    HrDocumentTemplateRead,
    UserReadDocumentShort,
    HrDocumentStatusRead,
    HrDocumentStepRead, HrDocumentTemplateUserRead
)
from schemas import Model, ReadModel
from .validator import validate_document_property



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

class LastStepDocument(BaseModel):
    id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    hr_document_template_id: Optional[str]
    staff_function_id: Optional[str]
    staff_function: Optional[str]

    # @validator("id", "hr_document_template_id", pre=True, always=True)
    # def default_empty_string(cls, v):
    #     return v if v is not None else ""

class HrDescriptionRead(BaseModel):
    name: Optional[str]
    nameKZ: Optional[str]

    @validator("name", "nameKZ", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""
    
class StatusDocument(BaseModel):
    id: Optional[str]
    name: Optional[str]
    nameKZ: Optional[str]
    created_at: Optional[datetime] 
    updated_at: Optional[datetime]

    @validator("name", "nameKZ", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""
    
class DocumentReadForUser(BaseModel):
    id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    name: Optional[str]
    nameKZ: Optional[str]
    path: Optional[str]
    pathKZ: Optional[str]
    subject_type: Optional[SubjectType]
    properties: Optional[Union[Dict[str, Any], None]]
    actions: Optional[Union[dict, None]]
    description: Optional[HrDescriptionRead]
    maintainer_id: Optional[str]
    is_visible: Optional[bool] = True
    is_due_date_required: Optional[bool] 
    is_initial_comment_required: Optional[bool] 
    is_draft: Optional[bool] 
    is_active: Optional[bool] 
    document_template: Optional[HrDocumentTemplateUserRead]
    # users: Optional[List[UserReadDocumentShort]]
    users: Optional[List[Dict]]
    last_step: Optional[LastStepDocument] = None
    status: Optional[StatusDocument]
    new_value: Optional[List[Dict]] = []

    @validator("status", pre=True, always=True)
    def default_status(cls, v):
        if v is None:
            return StatusDocument(
                id=None,
                created_at=None,
                updated_at=None,
                name="",
                nameKZ=""            
                )
        elif isinstance(v, dict):
            return StatusDocument(**v)
        return v

    @validator("last_step", pre=True, always=True)
    def default_last_step(cls, v):
        if v is None:
            return LastStepDocument(
                id=None,
                created_at=None,
                updated_at=None,
                hr_document_template_id=None,
                staff_function=None,
                staff_function_id=None
            )
        elif isinstance(v, dict):
            return LastStepDocument(**v)
        return v

    @validator("new_value", "nameKZ", "name", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""
    
    # @validator("path", "pathKZ", pre=True, always=True)
    # def default_empty_url(cls, v):
    #     return v if v is not None else "http://any.url/"
    
    @validator("subject_type", pre=True, always=True)
    def default_subject_type(cls, v):
        return v if v is not None else SubjectType.EMPLOYEE
    
    @validator("is_draft", "is_active","is_due_date_required", "is_initial_comment_required", pre=True, always=True)
    def default_empty_bool(cls, v):
        return v if v is not None else False

    @validator("actions", pre=True, always=True)
    def default_actions(cls, v):
        return v if v is not None else {}
    
    @validator("new_value", "users", pre=True, always=True)
    def default_value(cls, v):
        return v if v is not None else []
    
    _check_properties = validator("properties", allow_reuse=True)(
        validate_document_property
    )

    # @validator("properties", pre=True, always=True)
    # def enrich_properties(cls, v: Optional[dict]) -> Optional[dict]:
    #     if v is None:
    #         return v

    #     def enrich_field(field: dict, field_name: str) -> dict:
    #         valid_data_types = {"string", "number", "date"}
    #         allowed_data_taken_values = {"manual", "auto", "dropdown"}

    #         field["alias_name"] = field.get("alias_name", "")
    #         field["alias_nameKZ"] = field.get("alias_nameKZ", "")
    #         field["field_name"] = field_name
    #         field["type"] = field.get("type", "read")
    #         field["data_taken"] = field.get("data_taken", "manual" if field["type"] == "write" else "auto")

    #         if field["data_taken"] not in allowed_data_taken_values:
    #             field["data_taken"] = "manual"

    #         field["data_type"] = field.get("data_type")
    #         if field["data_taken"] == "manual":
    #             field["data_type"] = "string" if field["data_type"] is None else field["data_type"]
    #         else:
    #             if field["data_type"] not in valid_data_types:
    #                 field["data_type"] = "string"
                
    #         field["to_tags"] = field.get("to_tags", {})
    #         field["to_tags"].setdefault("directory", "")
    #         field["to_tags"].setdefault("isHidden", False)
    #         field["to_tags"].setdefault("cases", 0)
    #         field["to_tags"].setdefault("prevWordKZ", "")  
            
    #         return field

    #     return {key: enrich_field(value, key) for key, value in v.items()}
    
    class Config:
        orm_mode = True

class HrDocumentRead(HrDocumentBase, ReadModel):
    # properties: Optional[dict]
    # properties: Optional[Union[dict, None]]
    properties: Optional[Union[Dict[str, Any], None]]
    actions: Optional[Union[dict, None]]
    is_active: Optional[bool]
    is_visible: Optional[bool]
    is_draft: Optional[bool]
    is_due_date_required: Optional[bool] = False
    is_initial_comment_required: Optional[bool] = False
    subject_type: Optional[SubjectType]
    path: Optional[str]
    pathKZ: Optional[str]
    maintainer_id: Optional[str]
    description: Optional[HrDescriptionRead]
    name: Optional[str]
    nameKZ: Optional[str]
    document_template: Optional[HrDocumentTemplateRead]
    hr_document_template_id: Optional[str]
    status_id: Optional[str]
    status: Optional[HrDocumentStatusRead]
    initialized_by_id: Optional[str]
    initialized_by: Optional[UserReadDocumentShort]
    due_date: Optional[datetime]
    # properties: Optional[Union[dict, None]]
    can_cancel: Optional[bool]
    users: Optional[List[UserReadDocumentShort]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    last_step: Optional[HrDocumentStepRead]
    new_value: Optional[Any]
    old_history_id: Optional[str]
    children: Optional[List["HrDocumentRead"]]
    reg_number: Optional[str]

    class Config:
        orm_mode = True

    @validator("description", pre=True, always=True)
    def default_description(cls, v):
        return v if v is not None else HrDescriptionRead(name="", nameKZ="")

    @validator("properties", pre=True, always=True)
    def enrich_properties(cls, v: Optional[dict]) -> Optional[dict]:
        if v is None:
            return v

        def enrich_field(field: dict, field_name: str) -> dict:
            field["alias_name"] = field.get("alias_name", "")
            field["alias_nameKZ"] = field.get("alias_nameKZ", "")
            field["field_name"] = field_name
            field["type"] = "read"
            field["data_taken"] = "auto" if field.get("auto") else "manual"
            field["data_type"] = None if field.get("auto") else "string"  
            return field

        return {key: enrich_field(value, key) for key, value in v.items()}

    @validator("is_active", "is_visible", "is_draft", "is_due_date_required", "is_initial_comment_required", pre=True, always=True)
    def default_empty_bool(cls, v):
        return v if v is not None else False
    
    @validator("subject_type", pre=True, always=True)
    def default_subject_type(cls, v):
        return v if v is not None else SubjectType.EMPLOYEE
    
    @validator("actions", pre=True, always=True)
    def default_actions(cls, v):
        return v if v is not None else {}

    @validator("name", "nameKZ", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""
    
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