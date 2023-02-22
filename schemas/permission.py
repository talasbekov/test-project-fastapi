import uuid
from typing import List, Optional

from pydantic import BaseModel


class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class UserPermission(BaseModel):
    user_id: uuid.UUID
    permission_ids: List[uuid.UUID]


class PermissionRead(PermissionBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True
