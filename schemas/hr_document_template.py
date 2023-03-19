import uuid
from typing import Dict, Optional, Union

from pydantic import BaseModel, validator

from models import SubjectType
from .validator import hr_document_templates_properties_validator


class HrDocumentTemplateBase(BaseModel):
    name: str
    path: str
    subject_type: SubjectType
    properties: Dict[str, dict]

    _check_properties = validator('properties', allow_reuse=True)(hr_document_templates_properties_validator)


class HrDocumentTemplateCreate(HrDocumentTemplateBase):
    pass


class HrDocumentTemplateUpdate(HrDocumentTemplateBase):
    pass


class HrDocumentTemplateRead(HrDocumentTemplateBase):
    id: Optional[uuid.UUID]
    name: Optional[str]
    path: Optional[str]
    subject_type: Optional[SubjectType]
    properties: Optional[Union[dict, None]]

    class Config:
        orm_mode = True
