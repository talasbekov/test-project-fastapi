import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import UserRead
from schemas import Model, NamedModel, ReadModel, ReadNamedModel


class ProfileBase(Model):
    user_id: uuid.UUID


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase, ReadModel):
    user_id: Optional[uuid.UUID]
    user: Optional[UserRead]

    class Config:
        orm_mode = True
