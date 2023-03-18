import datetime
import uuid
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr


class ServiceArchiveStaffFunctionTypeBase(BaseModel):
    name: str
    description: Optional[str]
    origin_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ServiceArchiveStaffFunctionTypeCreate(ServiceArchiveStaffFunctionTypeBase):
    pass


class ServiceArchiveStaffFunctionTypeUpdate(ServiceArchiveStaffFunctionTypeBase):
    pass


class ServiceArchiveStaffFunctionTypeRead(ServiceArchiveStaffFunctionTypeBase):
    id: uuid.UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
