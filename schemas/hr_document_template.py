import uuid
from typing import Dict, Optional, Union, List

from pydantic import validator, BaseModel

from schemas import Model, NamedModel, ReadNamedModel, CustomBaseModel
from models import SubjectType
from .validator import hr_document_templates_properties_validator


class SuggestCorrections(Model):
    hr_document_template_id: str
    text: str


class HrDocumentTemplateBase(NamedModel):
    path: Optional[str]
    pathKZ: str
    subject_type: Optional[SubjectType]
    maintainer_id: Optional[str]
    properties: Dict[str, dict]
    description: Optional[NamedModel]
    actions: Dict[str, list]
    is_visible: bool
    is_due_date_required: Optional[bool] = False
    is_initial_comment_required: Optional[bool] = False
    is_draft: Optional[bool] = False

    _check_properties = validator("properties", allow_reuse=True)(
        hr_document_templates_properties_validator
    )
    @validator("is_due_date_required", "is_initial_comment_required", "is_draft", pre=True, always=True)
    def default_empty_bool(cls, v):
        return v if v is not None else False
    
    @validator("path", "pathKZ", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""

class HrDocumentTemplateCreate(HrDocumentTemplateBase):
    pass


class HrDocumentTemplateUpdate(HrDocumentTemplateBase):
    is_active: Optional[bool]
    is_draft: Optional[bool]


class HrDocumentTemplateRead(HrDocumentTemplateBase, ReadNamedModel):
    path: Optional[str]
    pathKZ: Optional[str]
    subject_type: Optional[SubjectType]
    properties: Optional[Union[dict, None]]
    actions: Optional[Union[dict, None]]
    is_active: Optional[bool]
    is_visible: Optional[bool]
    is_draft: Optional[bool]
    
    class Config:
        orm_mode = True

    @validator("path", "pathKZ", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""
    
    @validator("is_active", "is_visible", "is_draft", pre=True, always=True)
    def default_empty_bool(cls, v):
        return v if v is not None else False
    
    @validator("subject_type", pre=True, always=True)
    def default_subject_type(cls, v):
        return v if v is not None else SubjectType.EMPLOYEE
        
class HrDocumentTemplatePaginationRead(Model):
    total: Optional[int]
    objects: Optional[List[HrDocumentTemplateRead]]


class HrUserDocumentBase(CustomBaseModel):
    id: Optional[str]
    name: Optional[str]
    nameKZ: Optional[str]
    path: Optional[str]
    pathKZ: str
    subject_type: Optional[SubjectType]
    maintainer_id: Optional[str]
    properties: Dict[str, dict]
    description: Optional[NamedModel]
    actions: Dict[str, list]
    is_visible: bool
    is_due_date_required: Optional[bool] = False
    is_initial_comment_required: Optional[bool] = False
    is_draft: Optional[bool] = False

    _check_properties = validator("properties", allow_reuse=True)(
        hr_document_templates_properties_validator
    )
    @validator("is_due_date_required", "is_initial_comment_required", "is_draft", pre=True, always=True)
    def default_empty_bool(cls, v):
        return v if v is not None else False
    
    @validator("path", "pathKZ", "name", "nameKZ", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""



class HrDocumentTemplateUserRead(HrUserDocumentBase):
    path: Optional[str]
    pathKZ: Optional[str]
    subject_type: Optional[SubjectType]
    properties: Optional[Union[dict, None]]
    actions: Optional[Union[dict, None]]
    is_active: Optional[bool]
    is_visible: Optional[bool]
    is_draft: Optional[bool]
    
    class Config:
        orm_mode = True

    @validator("path", "pathKZ", pre=True, always=True)
    def default_empty_string(cls, v):
        return v if v is not None else ""
    
    @validator("is_active", "is_visible", "is_draft", pre=True, always=True)
    def default_empty_bool(cls, v):
        return v if v is not None else False
    
    @validator("subject_type", pre=True, always=True)
    def default_subject_type(cls, v):
        return v if v is not None else SubjectType.EMPLOYEE