import uuid

from pydantic import BaseModel
from typing import List, Dict, Union, Optional

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
    id: Optional[uuid.UUID]
    name: Optional[str]
    path: Optional[str]
    subject_type: Optional[SubjectType]
    properties: Optional[Union[dict, None]]
    details: Optional[Union[dict, None]]

    class Config:
        orm_mode = True
