from typing import List

from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class PermissionType(NamedModel):
    pass

class PermissionTypeRead(ReadNamedModel):
    pass

class PermissionBase(Model):
    type_id: str
    user_id: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class UserPermission(ReadNamedModel):
    user_id: str
    permission_ids: List[PermissionTypeRead]


class PermissionRead(PermissionBase, ReadModel):
    type: PermissionTypeRead
    
    class Config:
        orm_mode = True
