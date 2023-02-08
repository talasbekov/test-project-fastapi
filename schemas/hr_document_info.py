import uuid

from pydantic import BaseModel
from typing import List, Dict, Any


class HrDocumentInfoBase(BaseModel):
    hr_document_step_id: str
    signed_by: str
    comment: str
    is_signed: bool


class HrDocumentInfoCreate(HrDocumentInfoBase):
    pass

class HrDocumentInfoUpdate(HrDocumentInfoBase):
    pass


class HrDocumentInfoRead(HrDocumentInfoBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
