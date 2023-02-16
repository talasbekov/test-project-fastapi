import uuid

from pydantic import BaseModel
from typing import Optional


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: Optional[uuid.UUID]
    name: Optional[str]

    class Config:
        orm_mode = True
