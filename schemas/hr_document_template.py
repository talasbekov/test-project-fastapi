import uuid
from typing import Dict, Optional, Union

from pydantic import validator

from schemas import Model, NamedModel, ReadNamedModel
from models import SubjectType
from .validator import hr_document_templates_properties_validator


class SuggestCorrections(Model):
    hr_document_template_id: uuid.UUID
    text: str


class HrDocumentTemplateBase(NamedModel):
    path: Optional[str]
    pathKZ: str
    subject_type: Optional[SubjectType]
    maintainer_id: Optional[uuid.UUID]
    properties: Dict[str, dict]
    description: Optional[str]
    #description: Optional[NamedModel]
    actions: Dict[str, list]
    is_visible: bool
    is_due_date_required: Optional[bool] = False
    is_initial_comment_required: Optional[bool] = False
    is_draft: Optional[bool] = False

    _check_properties = validator("properties", allow_reuse=True)(
        hr_document_templates_properties_validator)


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

