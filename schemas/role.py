import uuid

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: uuid.UUID

    class Config:
        orm_mode = True
