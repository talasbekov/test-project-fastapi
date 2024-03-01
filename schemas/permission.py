from typing import List, Optional

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

class UserShortRead(Model):
    id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    father_name: Optional[str]
    icon: Optional[str]

    class Config:
        orm_mode = True

class PermissionRead(PermissionBase, ReadModel):
    type: PermissionTypeRead
    user: UserShortRead
    class Config:
        orm_mode = True
        
class PermissionPaginationRead(Model):
    total: Optional[int]
    objects: Optional[List[PermissionRead]]
