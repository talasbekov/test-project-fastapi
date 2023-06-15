import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class DocumentArchiveStaffFunctionTypeBase(BaseModel):
    name: str
    can_cancel: Optional[bool]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DocumentArchiveStaffFunctionTypeCreate(DocumentArchiveStaffFunctionTypeBase):
    origin_id: Optional[uuid.UUID]


class DocumentArchiveStaffFunctionTypeUpdate(DocumentArchiveStaffFunctionTypeBase):
    origin_id: Optional[uuid.UUID]


class NewDocumentArchiveStaffFunctionTypeCreate(DocumentArchiveStaffFunctionTypeBase):
    pass


class NewDocumentArchiveStaffFunctionTypeUpdate(DocumentArchiveStaffFunctionTypeBase):
    pass


class DocumentArchiveStaffFunctionTypeRead(DocumentArchiveStaffFunctionTypeBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
