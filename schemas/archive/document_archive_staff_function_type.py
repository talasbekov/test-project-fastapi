import datetime
import uuid
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr

class DocumentArchiveStaffFunctionTypeBase(BaseModel):
    name: str
    origin_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class DocumentArchiveStaffFunctionTypeCreate(DocumentArchiveStaffFunctionTypeBase):
    pass


class DocumentArchiveStaffFunctionTypeUpdate(DocumentArchiveStaffFunctionTypeBase):
    pass


class DocumentArchiveStaffFunctionTypeRead(DocumentArchiveStaffFunctionTypeBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
