import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import HrDocumentRead, HrDocumentStepRead, UserRead


class HrDocumentInfoBase(BaseModel):
    hr_document_step_id: uuid.UUID
    signed_by_id: Optional[uuid.UUID]
    assigned_to_id: Optional[uuid.UUID]
    comment: str
    is_signed: Optional[bool]
    hr_document_id: uuid.UUID
    signed_at: Optional[datetime.datetime]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class HrDocumentInfoCreate(HrDocumentInfoBase):
    pass


class HrDocumentInfoUpdate(HrDocumentInfoBase):
    pass


class HrDocumentInfoRead(HrDocumentInfoBase):
    id: Optional[uuid.UUID]
    hr_document_step_id: Optional[uuid.UUID]
    hr_document_step: Optional[HrDocumentStepRead]
    comment: Optional[str]
    hr_document_id: Optional[uuid.UUID]
    hr_document: Optional[HrDocumentRead]
    signed_by: Optional[UserRead]
    assigned_to: Optional[UserRead]


class HrDocumentHistoryRead(HrDocumentInfoRead):
    pass
