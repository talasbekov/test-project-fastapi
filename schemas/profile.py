import uuid
from typing import Optional

from schemas import UserRead
from schemas import Model, ReadModel


class ProfileBase(Model):
    user_id: str


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase, ReadModel):
    user_id: Optional[str]
    user: Optional[UserRead]

    class Config:
        orm_mode = True
