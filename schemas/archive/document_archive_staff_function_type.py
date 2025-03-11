import datetime
from typing import Optional
from schemas import Model


class DocumentArchiveStaffFunctionTypeBase(Model):
    name: str
    can_cancel: Optional[bool]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DocumentArchiveStaffFunctionTypeCreate(
        DocumentArchiveStaffFunctionTypeBase):
    origin_id: Optional[str]


class DocumentArchiveStaffFunctionTypeUpdate(
        DocumentArchiveStaffFunctionTypeBase):
    origin_id: Optional[str]


class NewDocumentArchiveStaffFunctionTypeCreate(
        DocumentArchiveStaffFunctionTypeBase):
    pass


class NewDocumentArchiveStaffFunctionTypeUpdate(
        DocumentArchiveStaffFunctionTypeBase):
    pass


class DocumentArchiveStaffFunctionTypeRead(
        DocumentArchiveStaffFunctionTypeBase):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
