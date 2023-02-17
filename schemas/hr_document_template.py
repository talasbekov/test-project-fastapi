import uuid

from pydantic import BaseModel, validator
from typing import Dict, Union, Optional

from models import SubjectType
from .validator import validate_property


class HrDocumentTemplateBase(BaseModel):
    name: str
    path: str
    subject_type: SubjectType
    properties: Dict[str, dict]

    _check_properties = validator('properties', allow_reuse=True)(validate_property)


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
    details: Optional[Union[dict, None]]

    class Config:
        orm_mode = True
