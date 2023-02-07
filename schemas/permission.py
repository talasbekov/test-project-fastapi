import uuid

from pydantic import BaseModel


class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
