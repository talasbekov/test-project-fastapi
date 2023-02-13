import uuid

from pydantic import BaseModel
from typing import List, Dict

from models import SubjectType


class HrDocumentTemplateBase(BaseModel):
    name: str
    path: str
    subject_type: SubjectType
    properties: dict
    details: dict


class HrDocumentTemplateCreate(HrDocumentTemplateBase):
    pass


class HrDocumentTemplateUpdate(HrDocumentTemplateBase):
    pass


class HrDocumentTemplateRead(HrDocumentTemplateBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
