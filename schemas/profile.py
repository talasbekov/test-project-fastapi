import uuid
from typing import Optional

from pydantic import BaseModel

from schemas import UserRead


class ProfileBase(BaseModel):
    pass


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileRead(ProfileBase):
    id: Optional[uuid.UUID]
    user_id: Optional[uuid.UUID]
    user: Optional[UserRead]

    class Config:
        orm_mode = True
