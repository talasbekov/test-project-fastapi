import uuid

from pydantic import BaseModel, ValidationError, validator
from typing import List, Dict, Union, Optional

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
    id: uuid.UUID
    properties: Optional[dict]

    class Config:
        orm_mode = True
