import datetime
import uuid
from typing import Optional

from schemas import HrDocumentRead, HrDocumentStepRead, UserRead
from schemas import Model, ReadModel


class HrDocumentInfoBase(Model):
    hr_document_step_id: str
    signed_by_id: Optional[str]
    assigned_to_id: Optional[str]
    comment: str
    is_signed: Optional[bool]
    hr_document_id: str
    signed_at: Optional[datetime.datetime]
    order: Optional[int] = 1

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class HrDocumentInfoCreate(HrDocumentInfoBase):
    pass


class HrDocumentInfoUpdate(HrDocumentInfoBase):
    pass


class HrDocumentInfoRead(HrDocumentInfoBase, ReadModel):
    hr_document_step_id: Optional[str]
    hr_document_step: Optional[HrDocumentStepRead]
    comment: Optional[str]
    hr_document_id: Optional[str]
    hr_document: Optional[HrDocumentRead]
    signed_by: Optional[UserRead]
    assigned_to: Optional[UserRead]


class HrDocumentHistoryRead(HrDocumentInfoRead):
    pass
