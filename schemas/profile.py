import uuid
from typing import Optional

from schemas import UserRead
from schemas import Model, ReadModel


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
