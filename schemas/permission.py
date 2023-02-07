import uuid

from pydantic import BaseModel

from schemas import PositionRead


class PermissionBase(BaseModel):
    name: str


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: str

    class Config:
        orm_mode = True
