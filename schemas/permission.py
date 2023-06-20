import uuid
from typing import List

from schemas import NamedModel, ReadNamedModel


class PermissionBase(NamedModel):
    pass


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class UserPermission(ReadNamedModel):
    user_id: uuid.UUID
    permission_ids: List[uuid.UUID]


class PermissionRead(PermissionBase, ReadNamedModel):

    class Config:
        orm_mode = True
