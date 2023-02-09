import uuid

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class HrDocumentInfoBase(BaseModel):
    hr_document_step_id: uuid.UUID
    signed_by: Optional[uuid.UUID]
    comment: str
    is_signed: Optional[bool]
    hr_document_id: uuid.UUID


class HrDocumentInfoCreate(HrDocumentInfoBase):
    pass


class HrDocumentInfoUpdate(HrDocumentInfoBase):
    pass


class HrDocumentInfoRead(HrDocumentInfoBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
