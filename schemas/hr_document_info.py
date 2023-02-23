import datetime
import uuid
from typing import Optional

from pydantic import BaseModel

from .hr_document import HrDocumentRead
from .hr_document_step import HrDocumentStepRead
from .user import UserRead


class HrDocumentInfoBase(BaseModel):
    hr_document_step_id: uuid.UUID
    signed_by: Optional[uuid.UUID]
    comment: str
    is_signed: Optional[bool]
    hr_document_id: uuid.UUID
    signed_at: Optional[datetime.datetime]


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
    signee: Optional[UserRead]
    

    class Config:
        orm_mode = True


class HrDocumentHistoryRead(HrDocumentInfoRead):

    will_sign: Optional[UserRead]

    class Config:
        orm_mode = True
