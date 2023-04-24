import uuid
from typing import Dict, Optional, Union, List

from pydantic import validator

from schemas import Model, NamedModel, ReadModel, ReadNamedModel
from models import SubjectType
from .validator import hr_document_templates_properties_validator


class HrDocumentTemplateBase(NamedModel):
    path: Optional[str]
    pathKZ: str
    subject_type: SubjectType
    properties: Dict[str, dict]
    description: Optional[str]
    actions: Dict[str, list]

    _check_properties = validator('properties', allow_reuse=True)(hr_document_templates_properties_validator)


class HrDocumentTemplateCreate(HrDocumentTemplateBase):
    pass


class HrDocumentTemplateUpdate(HrDocumentTemplateBase):
    is_active: Optional[bool]


class HrDocumentTemplateRead(HrDocumentTemplateBase, ReadNamedModel):
    path: Optional[str]
    pathKZ: Optional[str]
    subject_type: Optional[SubjectType]
    properties: Optional[Union[dict, None]]
    actions: Optional[Union[dict, None]]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
