import uuid

from pydantic import BaseModel
from typing import List, Dict, Union

from models import SubjectType


class HrDocumentTemplateBase(BaseModel):
    name: str
    path: str
    subject_type: SubjectType
    properties: Union[dict, None]
    details: Union[dict, None]


class HrDocumentTemplateCreate(HrDocumentTemplateBase):
    pass


class HrDocumentTemplateUpdate(HrDocumentTemplateBase):
    pass


class HrDocumentTemplateRead(HrDocumentTemplateBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
